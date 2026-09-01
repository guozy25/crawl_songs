"""统计歌曲标题词频，并绘制频率最高的 20 个词。"""

import csv
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from xml.sax.saxutils import escape

import jieba


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "songs_data.json"
DATA_DIR = Path(__file__).resolve().parent
CSV_FILE = DATA_DIR / "song_title_frequency_top20.csv"
SVG_FILE = DATA_DIR / "song_title_frequency_top20.svg"


# 这些内容属于版本、音源或演唱形式，不属于歌曲主题名称。
VERSION_RE = re.compile(
    r"[（(][^）)]*(?:feat\.?|ft\.?|version|\bver\.?\b|\bdj\b|remix|live|"
    r"现场|演唱会|伴奏|纯音乐|完整版|正式版|试听版|demo|版|片段|track|"
    r"instrumental|explicit|from the first take)[^）)]*[）)]"
    r"|\[[^\]]*(?:feat\.?|version|ver\.?|dj|remix|live|版)[^\]]*\]"
    r"|\b(?:DJ版|DJ|Remix|Live|伴奏|纯音乐|完整版|正式版|试听版|Demo)\b",
    re.IGNORECASE,
)


def clean_title(title):
    title = unicodedata.normalize("NFKC", str(title or ""))
    title = VERSION_RE.sub(" ", title)
    title = re.sub(r"<[^>]*>", " ", title)
    title = re.sub(r"\s+(?:feat\.?|ft\.?)\s+.*$", " ", title, flags=re.IGNORECASE)
    title = re.sub(r"\bDJ\b", " ", title, flags=re.IGNORECASE)
    title = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]+", " ", title)
    return re.sub(r"\s+", " ", title).strip()


def draw_svg(top20):
    width, height = 1000, 780
    left, right, top, bottom = 150, 80, 90, 55
    chart_width = width - left - right
    row_height = (height - top - bottom) / len(top20)
    max_count = max(count for _, count in top20)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;fill:#1f2937}.grid{stroke:#dbe3ef;stroke-dasharray:4 4}.bar{fill:#10b981}.label{font-size:15px}.value{font-size:13px}.title{font-size:22px;font-weight:600}</style>',
        f'<text x="{width/2}" y="42" text-anchor="middle" class="title">歌曲标题中词频最高的20个词</text>',
    ]

    for i in range(5):
        x = left + chart_width * i / 4
        value = max_count * i / 4
        lines.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height-bottom}" class="grid"/>')
        lines.append(f'<text x="{x:.1f}" y="{height-bottom+25}" text-anchor="middle" class="value">{value:,.0f}</text>')

    for index, (word, count) in enumerate(reversed(top20)):
        y = top + index * row_height + row_height * 0.2
        bar_height = row_height * 0.6
        bar_width = chart_width * count / max_count
        lines.append(f'<text x="{left-14}" y="{y + bar_height * 0.72:.1f}" text-anchor="end" class="label">{escape(word)}</text>')
        lines.append(f'<rect x="{left}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_height:.1f}" rx="2" class="bar"/>')
        lines.append(f'<text x="{left + bar_width + 8:.1f}" y="{y + bar_height * 0.72:.1f}" class="value">{count:,}</text>')

    lines.extend([
        f'<text x="{width/2}" y="{height-8}" text-anchor="middle" class="value">总词频（歌曲标题去重音源版本后）</text>',
        '</svg>',
    ])
    SVG_FILE.write_text("\n".join(lines), encoding="utf-8")


def main():
    songs = json.loads(INPUT_FILE.read_text(encoding="utf-8"))

    # 同一 song_id 只统计一次，避免重复爬取记录放大词频。
    unique_songs = {}
    for song in songs:
        unique_songs.setdefault(song.get("song_id"), song)

    counter = Counter()
    valid_titles = 0
    for song in unique_songs.values():
        title = clean_title(song.get("song_name", ""))
        words = [word.strip() for word in jieba.lcut(title) if word.strip()]
        words = [word for word in words if re.search(r"[\u4e00-\u9fffA-Za-z0-9]", word)]
        if words:
            valid_titles += 1
            counter.update(words)

    top20 = counter.most_common(20)
    with CSV_FILE.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["排名", "词语", "总词频"])
        writer.writerows((rank, word, count) for rank, (word, count) in enumerate(top20, 1))

    draw_svg(top20)
    print(f"原始记录数：{len(songs)}")
    print(f"去重后歌曲数：{len(unique_songs)}")
    print(f"有效标题数：{valid_titles}")
    print("Top 20 歌曲标题词频：")
    for rank, (word, count) in enumerate(top20, 1):
        print(f"{rank:>2}. {word}: {count}")
    print(f"总词频：{sum(counter.values())}")
    print(f"不同词语数：{len(counter)}")
    print(f"词频明细：{CSV_FILE}")
    print(f"条形图：{SVG_FILE}")


if __name__ == "__main__":
    main()
