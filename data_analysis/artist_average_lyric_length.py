"""统计每位歌手的平均歌词长度，并绘制最长/最短歌手条形图。"""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape


DATA_DIR = Path(__file__).resolve().parent
INPUT_FILE = DATA_DIR / "cleaned_songs_data.json"
CSV_FILE = DATA_DIR / "artist_average_lyric_length.csv"
SVG_FILE = DATA_DIR / "artist_average_lyric_length_top10.svg"


def lyric_length(text):
    """只统计中文、英文和数字，不把空格计入歌词长度。"""
    return len(re.findall(r"[\u4e00-\u9fffA-Za-z0-9]", text or ""))


def draw_svg(longest, shortest):
    width, height = 1100, 1120
    left, right, top, bottom = 250, 100, 105, 65
    panel_gap = 55
    panel_width = width - left - right
    panel_height = (height - top - bottom - panel_gap) / 2
    max_count = max(max(x[1] for x in longest), max(x[1] for x in shortest))
    max_count = max_count * 1.12
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;fill:#1f2937}.grid{stroke:#dbe3ef;stroke-dasharray:4 4}.bar-long{fill:#f97316}.bar-short{fill:#8b5cf6}.label{font-size:14px}.value{font-size:12px}.title{font-size:22px;font-weight:600}.panel-title{font-size:16px;font-weight:600}</style>',
        f'<text x="{width/2}" y="38" text-anchor="middle" class="title">歌手平均歌词长度 Top 10</text>',
    ]

    for panel_index, (title, values, bar_class) in enumerate([
        ("平均歌词最长的10位歌手", longest, "bar-long"),
        ("平均歌词最短的10位歌手", shortest, "bar-short"),
    ]):
        x0 = left
        y0 = top + panel_index * (panel_height + panel_gap)
        row_height = panel_height / len(values)
        lines.append(f'<text x="{x0 + panel_width/2:.1f}" y="{y0-25}" text-anchor="middle" class="panel-title">{title}</text>')
        for i in range(5):
            x = x0 + panel_width * i / 4
            value = max_count * i / 4
            lines.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0+panel_height:.1f}" class="grid"/>')
            lines.append(f'<text x="{x:.1f}" y="{y0+panel_height+22:.1f}" text-anchor="middle" class="value">{value:,.0f}</text>')
        for index, (artist, average, songs_count) in enumerate(values):
            y = y0 + index * row_height + row_height * 0.2
            bar_height = row_height * 0.58
            bar_width = panel_width * average / max_count
            lines.append(f'<text x="{x0-12}" y="{y + bar_height * 0.72:.1f}" text-anchor="end" class="label">{escape(artist)}</text>')
            lines.append(f'<rect x="{x0}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_height:.1f}" rx="2" class="{bar_class}"/>')
            lines.append(f'<text x="{x0 + bar_width + 7:.1f}" y="{y + bar_height * 0.72:.1f}" class="value">{average:.1f}（{songs_count}首）</text>')

    lines.extend([
        f'<text x="{width/2}" y="{height-8}" text-anchor="middle" class="value">平均歌词长度（字符数，不含空格；仅统计有效歌词）</text>',
        '</svg>',
    ])
    SVG_FILE.write_text("\n".join(lines), encoding="utf-8")


def main():
    songs = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    unique_songs = {}
    for song in songs:
        unique_songs.setdefault(song.get("song_id"), song)

    artist_lengths = defaultdict(list)
    for song in unique_songs.values():
        if song.get("lyric_status") != "valid":
            continue
        length = lyric_length(song.get("lyric", ""))
        if length > 0:
            artist_lengths[song.get("artist_name", "未知歌手")].append(length)

    averages = [
        (artist, sum(lengths) / len(lengths), len(lengths), sum(lengths))
        for artist, lengths in artist_lengths.items()
    ]
    averages.sort(key=lambda x: x[1], reverse=True)
    longest = [(artist, average, count) for artist, average, count, _ in averages[:10]]
    shortest = [(artist, average, count) for artist, average, count, _ in sorted(averages, key=lambda x: x[1])[:10]]

    with CSV_FILE.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["类别", "歌手", "歌曲数", "平均歌词长度", "歌词总字符数"])
        for category, values in [("最长10位", longest), ("最短10位", shortest)]:
            for artist, average, count in values:
                total = round(average * count)
                writer.writerow([category, artist, count, round(average, 2), total])

    draw_svg(longest, shortest)
    print(f"去重后歌曲数：{len(unique_songs)}")
    print(f"参与统计的歌手数：{len(averages)}")
    print("平均歌词最长 Top 10：")
    for i, (artist, average, count) in enumerate(longest, 1):
        print(f"{i:>2}. {artist}: {average:.2f} 字符（{count} 首）")
    print("平均歌词最短 Top 10：")
    for i, (artist, average, count) in enumerate(shortest, 1):
        print(f"{i:>2}. {artist}: {average:.2f} 字符（{count} 首）")
    print(f"明细：{CSV_FILE}")
    print(f"图表：{SVG_FILE}")


if __name__ == "__main__":
    main()
