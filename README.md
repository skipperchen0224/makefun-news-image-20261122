# makefun-news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/skipperchen0224/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/skipperchen0224/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A newspaper front page that sums up the world's news of Sunday,
22 November 2026, in one 1024×1024 image (`entry.png`).

Made for the [news-image-20261122 bounty](https://make.fun/bounty/news-image-20261122)
on [make.fun](https://make.fun) — one image, the whole day.

![The World Today — 22 November 2026](entry.png)

## The day's stories

- **Lead — Antalya:** COP31 collapses with no deal as the fossil-fuel
  rift splits the summit; the EU and island states reject a final text
  that never names fossil fuels (AFP, AP).
- **Washington:** Democrats win their biggest House majority since 1992 —
  a North Carolina recount hands them their 258th seat as Chuck Hubbard
  beats Virginia Foxx by 330 votes (AP, CNN).
- **Caracas:** the US and Venezuela sign a deal to reestablish military
  ties as the US defence chief visits Caracas (AP).
- **Libya:** a suspected sea drone hits the Russian corvette Merkury at
  its Benghazi naval base, setting it ablaze (AP).
- **Sudan:** drone attacks blamed on the RSF kill four around Khartoum
  and damage a United Nations building (AFP).
- **Ukraine:** Zelenskyy urges the US to release Patriot missiles as
  Russian strikes leave 14 missing in the Kyiv region (AP).
- **Mexico:** cartel boss "El Chapo Isidro" is captured in a Sinaloa
  gun battle that leaves 11 dead (AP).
- Also: a Baltic cargo ship ablaze after a drone strike; French protests
  enter a sixth weekend; a Brazil storm kills four.

## Run it

```sh
python3 draw_image.py   # redraw the front page (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png (1024x1024 PNG, deterministic bytes)
```

`main.ts` (Node 22, standard library only) copies the pre-drawn
`entry.png` to the output directory. The image itself is drawn by
`draw_image.py` (Pillow, in this repo). Every fact was checked against
live reporting on 22 November 2026. The script is deterministic — same
input, same bytes.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
