# Daily Brief — news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Phsxe/makefun-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Phsxe/makefun-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A program that turns a verified list of 25 news stories from
Thursday, November 26, 2026 into a single 1024x1024 daily news brief
image: three headlines, eight short cards, fourteen more stories, a
UTC timeline, a markets numbers bar, a region count bar, and a
DATE CHECK box for the stories whose date depends on the time zone.

The entry point is `main.py`. It reads nothing but the constants in
the file itself and writes `out/entry.png` (1024x1024 PNG, under 1 MiB).

Run it with Python 3 and Pillow, standard library plus Pillow only,
no network:

```
python3 main.py
```

Run it twice and the output is byte-identical.

## What is on the page

- Masthead: THE DAILY BRIEF, Thursday, November 26, 2026, 25 stories
  from 6 regions.
- Numbers bar: Kospi +1.8%, Nasdaq 100 -0.6%, WTI $84.05, gold $3,572,
  Bitcoin $60,636.
- Headlines: the US tariff plan for 14 economies, the Ukrainian strike
  on Savasleyka air base, and the Houthi missile intercepts over Riyadh.
- Eight cards: North Korea's tactical nuclear push, the Nasdaq 100
  bear market, the delayed Macy's parade, the Cairo tanker crash, the
  Bank of Korea hike, Andy Taylor's death, the EU budget summit, and
  BepiColombo reaching Mercury.
- ALSO IN THE NEWS: fourteen more stories, from the Murmansk governor's
  detention to Mitsui's $125bn shake-up.
- Timeline (UTC): six timed items from 00:17 to 02:12 UTC.
- Region bar: Asia-Pacific 6, Europe 6, Middle East 3, Americas 6,
  Africa 3, Markets 1 — 25 stories in total.
- DATE CHECK: the US tariff announcement (Washington, late Nov 25;
  reported in Asia Nov 26) and the Macy's parade delay (announced late
  Nov 25; parade day was Thanksgiving, Nov 26), plus the stories
  excluded because they are not Nov 26 in their local date.

## How the stories were checked

Every story was checked against its original source (Reuters, AP,
Bloomberg, Kyodo and others) and dated by the local date at the place
of the event. Aggregator dates were not trusted: an aggregator can
stamp a story with the wrong day, and a result labelled "November 26"
in one time zone can be a November 25 evening event in another. The
stories that failed that check — the Shenzhou-24 docking, the Horn
Island crash, the Hodeidah strike, the Champions League results — were
left out and are named in the DATE CHECK box.

## Reproduce it

```
git clone https://github.com/Phsxe/makefun-news-image-20261126
cd makefun-news-image-20261126
python3 main.py
```

The program writes `out/entry.png`. All glyphs are rendered at run
time from the DejaVu fonts on the machine; no font table is stored in
the repository.

## Licence

MIT.
