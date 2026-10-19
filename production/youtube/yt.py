"""YouTube channel tool: OAuth (manual loopback), channel info, upload.

    python production/youtube/yt.py auth-url            # prints a Google sign-in link
    python production/youtube/yt.py auth-finish '<URL>' # paste the full localhost URL the browser ended on
    python production/youtube/yt.py whoami              # channel name, id, upload permission check
    python production/youtube/yt.py upload <meta.json>  # uploads video (+ captions if meta has "captions"); prints id + link

Secrets: OAuth client id/secret come from env (Client_ID_google / Client_secret_google), never from
the repo. The user token is stored at ~/.config/yt-kids/token.json (chmod 600), outside the repo.
Scopes: youtube.upload (upload) + youtube.readonly (read channel info). Nothing is ever published
publicly by this tool unless meta.json says so explicitly.
"""
import json
import os
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtube.force-ssl",  # force-ssl: captions.insert, privacy updates
          "https://www.googleapis.com/auth/yt-analytics.readonly"]  # Analytics API: retention, watch time
REDIRECT = "http://localhost:8765/"
HOME = Path(os.environ.get("YT_KIDS_HOME", Path.home() / ".config" / "yt-kids"))
TOKEN = HOME / "token.json"
PENDING = HOME / "pending_flow.json"


def client_config():
    cid, sec = os.environ.get("Client_ID_google"), os.environ.get("Client_secret_google")
    if not cid or not sec:
        sys.exit("Missing Client_ID_google / Client_secret_google in the environment")
    return {"installed": {"client_id": cid, "client_secret": sec, "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                          "token_uri": "https://oauth2.googleapis.com/token", "redirect_uris": [REDIRECT]}}


def secure_write(path, text):
    HOME.mkdir(parents=True, exist_ok=True)
    os.chmod(HOME, 0o700)
    path.write_text(text)
    os.chmod(path, 0o600)


def auth_url():
    flow = Flow.from_client_config(client_config(), scopes=SCOPES, redirect_uri=REDIRECT, autogenerate_code_verifier=True)
    url, state = flow.authorization_url(access_type="offline", prompt="consent", include_granted_scopes="true")
    secure_write(PENDING, json.dumps({"state": state, "code_verifier": flow.code_verifier}))
    print(url)


def auth_finish(redirect_url):
    pend = json.loads(PENDING.read_text())
    flow = Flow.from_client_config(client_config(), scopes=SCOPES, redirect_uri=REDIRECT, state=pend["state"])
    flow.code_verifier = pend["code_verifier"]
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # loopback redirect is plain http by design
    flow.fetch_token(authorization_response=redirect_url.strip())
    secure_write(TOKEN, flow.credentials.to_json())
    PENDING.unlink(missing_ok=True)
    print("token saved")


def env_find(pattern):
    """First environment variable whose NAME matches pattern (case-insensitive). Values are never printed."""
    import re
    for k, v in os.environ.items():
        if re.search(pattern, k, re.I) and v.strip():
            return k, v.strip()
    return None, None


def creds_from_env():
    """Persistent secrets survive container resets. Priority:
    1) a full token JSON (env name containing TOKEN_JSON / YT_TOKEN), 2) a refresh token (name containing REFRESH),
    3) a pending consent redirect URL (value contains 'localhost:8765' and 'code=') -> completes auth-finish once."""
    cfg = client_config()["installed"]
    k, v = env_find(r"token_json|yt_token|youtube_token")
    if v and v.startswith("{"):
        return Credentials.from_authorized_user_info(json.loads(v))
    k, v = env_find(r"refresh")
    if v:
        c = Credentials(None, refresh_token=v, client_id=cfg["client_id"], client_secret=cfg["client_secret"],
                        token_uri=cfg["token_uri"])
        c.refresh(Request())
        return c
    for name, val in os.environ.items():
        if "localhost:8765" in val and "code=" in val and PENDING.exists():
            try:
                auth_finish(val)
            except Exception as e:  # code expired or flow mismatch: re-consent needed
                print(f"env redirect URL in {name} could not be used: {type(e).__name__}", file=sys.stderr)
            break
    return None


def creds():
    c = creds_from_env()
    if c:
        return c
    if not TOKEN.exists():
        sys.exit("Not authorized: set a refresh token secret in the environment, or run auth-url / auth-finish")
    c = Credentials.from_authorized_user_file(str(TOKEN))  # use whatever scopes were granted
    if not c.valid and c.refresh_token:
        c.refresh(Request())
        secure_write(TOKEN, c.to_json())
    return c


def whoami():
    yt = build("youtube", "v3", credentials=creds())
    r = yt.channels().list(part="snippet,status,statistics,contentDetails", mine=True).execute()
    items = r.get("items", [])
    if not items:
        print(json.dumps({"channel": None, "note": "This Google account has no YouTube channel"}))
        return
    ch = items[0]
    c = creds()
    print(json.dumps({
        "title": ch["snippet"]["title"], "id": ch["id"], "customUrl": ch["snippet"].get("customUrl"),
        "country": ch["snippet"].get("country"),
        "madeForKids_default": ch.get("status", {}).get("madeForKids"),
        "longUploadsStatus": ch.get("status", {}).get("longUploadsStatus"),
        "privacyStatus": ch.get("status", {}).get("privacyStatus"),
        "subscribers": ch.get("statistics", {}).get("subscriberCount"),
        "videos": ch.get("statistics", {}).get("videoCount"),
        "granted_scopes": sorted(c.scopes or []),
        "can_upload": "https://www.googleapis.com/auth/youtube.upload" in (c.scopes or []),
    }, ensure_ascii=False, indent=1))


def add_captions(yt, vid, srt_file, lang, name):
    """Upload a separate closed-caption track (CC). The video picture stays clean."""
    media = MediaFileUpload(srt_file, mimetype="application/octet-stream", resumable=False)
    r = yt.captions().insert(part="snippet", body={"snippet": {"videoId": vid, "language": lang, "name": name, "isDraft": False}},
                             media_body=media).execute()
    print(json.dumps({"captionId": r["id"], "language": lang, "track": name}, ensure_ascii=False))


def captions_cmd(video_id, srt_file, lang="es"):
    add_captions(build("youtube", "v3", credentials=creds()), video_id, srt_file, lang, "Español")


def upload(meta_file):
    m = json.loads(Path(meta_file).read_text())
    yt = build("youtube", "v3", credentials=creds())
    body = {
        "snippet": {"title": m["title"], "description": m["description"], "tags": m.get("tags", []),
                    "categoryId": m.get("categoryId", "10"), "defaultLanguage": m.get("language", "es"),
                    "defaultAudioLanguage": m.get("language", "es")},
        "status": {"privacyStatus": m.get("privacyStatus", "private"), "selfDeclaredMadeForKids": bool(m.get("madeForKids", True)),
                   "embeddable": True, "license": "youtube", "containsSyntheticMedia": bool(m.get("containsSyntheticMedia", False))},
    }
    media = MediaFileUpload(m["file"], mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"uploaded {int(status.progress() * 100)}%", flush=True)
    vid = resp["id"]
    if m.get("captions"):
        add_captions(yt, vid, m["captions"], m.get("language", "es"), m.get("captionName", "Español"))
    check = yt.videos().list(part="status,snippet,processingDetails", id=vid).execute()["items"]
    st = check[0]["status"] if check else {}
    print(json.dumps({"videoId": vid, "watch": f"https://www.youtube.com/watch?v={vid}", "shorts": f"https://youtube.com/shorts/{vid}",
                      "privacyStatus": st.get("privacyStatus"), "uploadStatus": st.get("uploadStatus"),
                      "madeForKids": st.get("madeForKids"), "selfDeclaredMadeForKids": st.get("selfDeclaredMadeForKids")},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    {"auth-url": auth_url, "auth-finish": auth_finish, "whoami": whoami, "upload": upload, "captions": captions_cmd}[cmd](*args)
