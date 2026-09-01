"""清洗 songs_data.json 中的歌词。

输出文件：cleaned_songs_data.json
将原始 lyric 复制到 lyric_raw，并将 lyric 替换为清洗后的歌词，同时增加：
    lyric_clean  清洗后的歌词正文
    lyric_status valid / empty / invalid / instrumental

本脚本只负责歌词清洗，不负责中文分词和词频统计。
"""

import ast
import json
import re
import unicodedata
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "songs_data.json"
OUTPUT_FILE = Path(__file__).resolve().parent / "cleaned_songs_data.json"


# 歌词开头常见的制作人员信息。这里删除整行，而不是删除歌词中的普通文字。
METADATA_RE = re.compile(
    r"^(词|曲|编曲|制作人|制作|监制|作词|作曲|演唱|合声|合声编写|和声|和声编写|"
    r"吉他|贝斯|鼓|弦乐|口琴|录音|录音助理|录音工程|混音|混音工程|母带|统筹|"
    r"出品|发行|企划|OP|SP|Music|Lyric|"
    r"Written|Composed|Arranged|Produced|Vocal|Chorus|Guitar|Bass|Drums)"
    r"(?:\s*[:：]|\s+)"
    r"|^歌词来源[:：]",
    re.IGNORECASE,
)

PLACEHOLDER_RE = re.compile(r"^(纯音乐|暂无歌词|暂无此歌词|没有歌词|该歌曲暂无歌词|伴奏)$")
NON_LYRICAL_HINTS = ("纯音乐", "该歌曲为DJ舞曲", "此歌曲为DJ舞曲", "暂无歌词", "没有歌词", "电影原声", "原声带")


def parse_lyric(raw):
    """把原始 lyric 转成歌词行列表。解析失败返回 None。"""
    if raw is None or raw == "":
        return None

    if isinstance(raw, list):
        data = raw
    elif isinstance(raw, str):
        try:
            # 当前数据是字符串形式的 Python 列表，单引号也能处理。
            data = ast.literal_eval(raw)
        except (ValueError, SyntaxError):
            try:
                data = json.loads(raw)
            except (TypeError, ValueError, json.JSONDecodeError):
                return None
    else:
        return None

    if not isinstance(data, list):
        return None

    lines = []
    for item in data:
        if isinstance(item, dict):
            text = item.get("lineLyric", "")
            if text is not None:
                lines.append(str(text))
        elif isinstance(item, str):
            lines.append(item)
    return lines


def normalize_line(line):
    """统一全角字符、时间标记、HTML 和空白字符。"""
    line = unicodedata.normalize("NFKC", line)
    line = re.sub(r"\[[0-9:.]+\]", "", line)       # [00:12.34]
    line = re.sub(r"\([^)]*\)|（[^）]*）", "", line)  # 括号中的演唱提示
    line = re.sub(r"<[^>]+>", "", line)             # HTML 标签
    line = re.sub(r"\s+", " ", line).strip()
    return line


def clean_lyric(raw, song_name="", artist_name=""):
    """返回 (clean_text, status)。保留副歌重复，不擅自去重。"""
    lines = parse_lyric(raw)
    if not lines:
        return "", "empty"

    cleaned = []
    for line in lines:
        line = normalize_line(line)
        if not line:
            continue
        # 部分无歌词记录会返回“该歌曲为纯音乐请欣赏”等完整提示语。
        if any(hint in line for hint in NON_LYRICAL_HINTS):
            continue
        if METADATA_RE.search(line):
            continue
        if PLACEHOLDER_RE.fullmatch(line):
            continue

        # 删除歌词第一行常见的“歌名 - 歌手”标题。
        if not cleaned and song_name:
            title = normalize_line(song_name)
            artist = normalize_line(artist_name)
            title_artist = re.escape(title) + r"\s*[-–—]?\s*" + re.escape(artist)
            compact_line = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]", "", line).lower()
            compact_title = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]", "", title).lower()
            compact_artist = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]", "", artist).lower()
            if (
                line == title
                or line.startswith(title + " -")
                or line.startswith(title + "–")
                or (artist and re.fullmatch(title_artist, line, flags=re.IGNORECASE))
                or (line.startswith(title) and any(x in line for x in ("电影原声", "原声带", "纯音乐")))
                or (compact_title and compact_line.startswith(compact_title) and compact_artist in compact_line)
            ):
                continue
        cleaned.append(line)

    # 对词频分析保留中文、英文和数字；标点只作为分隔符去掉。
    text = "\n".join(cleaned)
    text = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return "", "instrumental"
    return text, "valid"


def main():
    songs = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    valid = empty = invalid = instrumental = 0

    for song in songs:
        song["lyric_raw"] = song.get("lyric")
        cleaned, status = clean_lyric(
            song.get("lyric"),
            song.get("song_name", ""),
            song.get("artist_name", ""),
        )
        song["lyric"] = cleaned
        song["lyric_clean"] = cleaned
        song["lyric_status"] = status
        if status == "valid":
            valid += 1
        elif status == "empty":
            empty += 1
        elif status == "invalid":
            invalid += 1
        else:
            instrumental += 1

    OUTPUT_FILE.write_text(
        json.dumps(songs, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"共处理 {len(songs)} 首歌曲")
    print(f"有效歌词：{valid}")
    print(f"空歌词：{empty}")
    print(f"纯音乐或无正文：{instrumental}")
    print(f"解析失败：{invalid}")
    print(f"输出文件：{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
