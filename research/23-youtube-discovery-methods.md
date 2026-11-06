# YouTube discovery: what moved the Halloween episode + methods to test (06.11.2026)

## Our data (Data API, 06.11)
| video | uploaded | how | views | note |
|---|---|---|---|---|
| Halloween episode 4UZCDJT4MHI | 04.11 17:35 UTC private → public 20:37 | keyword file name, audio es-419 | **84** in ~2 days | the deleted old copy Eo_PHQrLDs0 had 12 views in 12 days |
| Broccoli episode Vc6VhVsETKM | 04.11 17:26 UTC, public straight away | file name `tito_brocoli.mp4`, new SEO metadata | **1** | |
| Broccoli Short 267EcZ452Mc | 02.11 | public | 1 | |
| Dance Short _6ztnDmAFyg | 25.10 | public | 18 | links to the Halloween episode |

- **Caveat: 3 variables changed at once** on Halloween (private→public, file name, es-419). The Short's link also points at it, and the topic is seasonal.
- YouTube Analytics (traffic sources, countries) lags 2–3 days and is still empty. Re-check on 08.11 to see whether the views came from search, browse, suggested or YouTube Kids.
- The API shows `publishedAt` = the moment it went public. A private-first upload therefore launches as a fresh, fully processed video (HD, made-for-kids checks done) at a time we choose.
- Our earlier API uploads had **no file name at all** (`fileDetails.fileName` = None). Fixed: yt.py now sends a Slug header.

## What the research says (sources are mostly third-party; no official YouTube statement)
1. **Private → public:** no evidence of an algorithmic "boost" from the toggle itself. YouTube-support-quoted answers say it is neutral and that distribution starts at the public moment. The real value: launch fully processed, at a planned hour, with the first impressions landing on a ready video.
2. **File name:** no official confirmation. SEO blogs call it small but harmless. Keep doing it; it costs nothing.
3. **Made for kids (official help, support.google.com/youtube/answer/9632097):** no comments, no bell notifications, no end screens or cards, no autoplay on home, no miniplayer.
   - Subscribers are NOT notified, so discovery depends on search, browse/suggested next to other kids' videos, and the YouTube Kids app.
   - Consequence: titles, thumbnails and the first seconds carry everything.
4. **TV viewing and compilations:** over half of kids watch YouTube on a TV (Feb 2026 report). Among 2–5-year-olds, nursery rhymes are 41% of viewing. The most-viewed nursery-rhyme video ever is a 54-minute compilation (LittleBabyBum). Our own research/22: Hugo el burrito's compilations reached 11.2M vs 4.3M for his best single.
5. **Timing:** no solid LatAm kids data. Best available: weekends and early evening (5–8 PM local), Mexico City time.

## Methods to test (cheap first)
| # | method | cost | test |
|---|---|---|---|
| A | Private-first + keyword file name + public at a planned hour | 0 | replicate on broccoli (one recipe, second video) |
| B | Publish hour: Saturday 09:00 or 18:00 Mexico City (15:00 / 00:00 UTC) | 0 | broccoli at Sat 18:00 CDMX |
| C | **Compilation 10–15 min with chapters** from our existing episodes (Buenos días, Halloween, Dormir, Brócoli, Manos, Mesa, Basura…) | 0 cr (edit only) | 1 upload; watch time and TV sessions |
| D | Thumbnails: big face + one object, bright, no text or ≤2 words | 0 (frame grab + edit) | A/B on the next 2 uploads (YouTube "Test & Compare") |
| E | Playlist per series ("Tito: hábitos", "Tito: canciones para dormir") on the channel page | 0 | already partly done (series playlists) |
| F | Short → long: every Short's description links its episode (already); pin the episode on the channel home | 0 | |
| G | Re-upload old weak videos? Only the recent ones with <20 views; never delete videos that carry history | 0 | case by case, with Roy's OK |
