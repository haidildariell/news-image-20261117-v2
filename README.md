# The World Today — 17 November 2026 in One Image

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/haidildariell/news-image-20261117-v2/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/haidildariell/news-image-20261117-v2/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

Bounty: https://make.fun/bounty/news-image-20261117

This entry sums up the world news of Monday 17 November 2026 in a single 1024×1024 image: a newspaper front page, "The World Today", with a lead story on Ukraine's second-day strike on the Crimean Bridge and further stories from the Gulf, business (Nvidia's record quarter), the Shenzhen APEC summit, Japan, and the West Bank, plus an "Also Today" ticker covering migration, US chip curbs, and Jericho. The image was made with a deterministic Pillow program (`build_image.py`) that draws the whole page — masthead, flat illustrations, headlines, and sublines — using real fonts (DejaVu Serif and Liberation Sans), measured and wrapped so every word fits its panel and stays legible at small sizes. `build_image.py` runs at build time to produce `entry.png`; the entrypoint `main.py` is a stdlib-only copy program that copies `entry.png` to the output directory, so repeated runs write byte-identical bytes.

## Run

```sh
python3 main.py            # writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)
python3 build_image.py     # regenerates entry.png (requires Pillow)
```
