"""Build title/description/tags in the NuNu-style format (research/10): song first, #shorts, CTA, links to our Shorts,
Spanish hashtags, fixed channel paragraph, Spanish + English tags.

    from meta_template import build
    m = build(song="¡Rojito cambia de color!", summary="...", topic_tags=["camión de bomberos"], hashtags=["#AprendeLosColores"])
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHANNEL = ("En Cantilandia hacemos canciones infantiles en español con animación 3D: Tito el elefantito, Mamá Elefanta y "
           "Rojito el camioncito de bomberos. Cada canción cuenta una pequeña historia con un hábito, un color o una aventura, "
           "para que los peques de 1 a 4 años canten, aprendan y se diviertan en familia.")
BASE_TAGS = ["canciones infantiles", "canciones para niños", "canciones infantiles en español", "música infantil",
             "videos para niños", "videos educativos", "preescolar", "spanish kids songs", "nursery rhymes spanish",
             "kids songs", "Cantilandia"]


def links(exclude=None, n=3):
    reg = json.loads((HERE.parent / "registry.json").read_text())
    pub = [r for r in reversed(reg) if r.get("youtube_id") and "unlisted" not in r.get("status", "") and r["id"] != exclude]
    return [f"https://youtube.com/shorts/{r['youtube_id']}" for r in pub[:n]]


def build(song, summary, topic_tags, hashtags, exclude=None, short=True):
    title = f"{song} | #shorts | Canciones Para Niños | Cantilandia" if short else f"{song} | Canciones Para Niños | Cantilandia"
    more = "\n".join(f"{i + 1}. {u}" for i, u in enumerate(links(exclude)))
    tags_line = " ".join(["#cancionesinfantiles", "#preescolar", "#aprendizajeinfantil"] + hashtags + (["#shorts"] if short else []))
    desc = (f"🔔 ¡No olvides DAR LIKE y SUSCRIBIRTE para más canciones y videos divertidos! 🎵💕\n"
            f"https://www.youtube.com/@cantilandiatv\n\n{summary}\n\n📢 Mira más videos aquí:\n{more}\n\n{tags_line}\n\n"
            f"Canciones infantiles de Cantilandia ►\n{CHANNEL}")
    tags = list(dict.fromkeys(topic_tags + [song.strip("¡!¿? ")] + BASE_TAGS))[:30]
    return {"title": title[:100], "description": desc[:4900], "tags": tags}
