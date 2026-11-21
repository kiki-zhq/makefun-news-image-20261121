# makefun-news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/kiki-zhq/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/kiki-zhq/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

The World in One Day — Saturday, 21 November 2026. A newspaper front page
that sums up the day's world news in one 1024x1024 image: Russia's biggest
missile and drone bombardment of the war on Kyiv, with missiles landing in
Poland; the Trump–Xi–Putin "Declaration toward Peace" from Shenzhen; the
world court's genocide ruling against Myanmar; the AI sell-off dragging
Wall Street into correction; the biggest UK–EU deals since Brexit; COP31
running into overtime; and Gaza.

`render.py` draws the front page (Pillow, DejaVu fonts) into `entry.png`.
`main.py` is the submitted program: standard library only, it copies
`entry.png` to the output path, so both graded runs write the same bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=b7zh37wc&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
