"""对清洗后的歌词进行中文分词。

输入：data_analysis/cleaned_songs_data.json
输出：data_analysis/tokenized_songs_data.json

每首歌曲新增：
    lyric_tokens：完整分词结果
    lyric_tokens_filtered：去除常见功能词后的分词结果，供词语热度分析使用
"""

import json
import re
from pathlib import Path

import jieba


DATA_DIR = Path(__file__).resolve().parent
INPUT_FILE = DATA_DIR / "cleaned_songs_data.json"
OUTPUT_FILE = DATA_DIR / "tokenized_songs_data.json"


# 这些词在歌词中出现很多，但通常不能反映主题；完整结果仍保留在 lyric_tokens 中。
STOPWORDS = {
    "我", "你", "他", "她", "它", "我们", "你们", "他们", "她们",
    "的", "了", "着", "过", "是", "在", "有", "和", "与", "跟", "也",
    "都", "还", "就", "才", "又", "很", "更", "最", "不", "没", "没有",
    "到", "从", "把", "被", "让", "给", "为", "因", "因为", "如果", "而",
    "但", "却", "或", "吗", "呢", "吧", "啊", "呀", "哦", "啦", "这", "那",
    "一个", "一起", "自己", "什么", "怎么", "这样", "那样",
    # 歌曲中的哼唱、唱名，不作为主题词统计
    "Do", "Re", "Mi", "Fa", "So", "La", "Si",
}


def tokenize(text):
    """分词并过滤空白、纯符号和过长的异常片段。"""
    if not text:
        return []
    words = []
    for word in jieba.lcut(text, HMM=True):
        word = word.strip()
        if not word or not re.search(r"[\u4e00-\u9fffA-Za-z0-9]", word):
            continue
        words.append(word)
    return words


def main():
    songs = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    valid_count = 0

    for song in songs:
        words = tokenize(song.get("lyric_clean", ""))
        song["lyric_tokens"] = words
        song["lyric_tokens_filtered"] = [word for word in words if word not in STOPWORDS]
        if words:
            valid_count += 1

    OUTPUT_FILE.write_text(
        json.dumps(songs, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"共处理 {len(songs)} 首歌曲")
    print(f"成功分词：{valid_count} 首")
    print(f"无有效歌词：{len(songs) - valid_count} 首")
    print(f"输出文件：{OUTPUT_FILE}")

    for song in songs:
        if song.get("lyric_tokens"):
            print(f"示例：{song['song_name']} / {' / '.join(song['lyric_tokens'][:30])}")
            break


if __name__ == "__main__":
    main()
