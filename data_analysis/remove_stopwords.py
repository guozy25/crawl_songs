"""从分词结果中去除停用词。

输入：tokenized_songs_data.json
输出：stopwords_removed_songs_data.json

保留 lyric_tokens，并新增：
    lyric_tokens_no_stopwords：去除停用词后的词语列表
    lyric_text_no_stopwords：用空格连接后的词语文本
"""

import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent
INPUT_FILE = DATA_DIR / "tokenized_songs_data.json"
OUTPUT_FILE = DATA_DIR / "stopwords_removed_songs_data.json"


STOPWORDS = {
    "我", "你", "他", "她", "它", "我们", "你们", "他们", "她们",
    "的", "了", "着", "过", "是", "在", "有", "和", "与", "跟", "也",
    "都", "还", "就", "才", "又", "很", "更", "最", "不", "没", "没有",
    "到", "从", "把", "被", "让", "给", "为", "因", "因为", "如果", "而",
    "但", "却", "或", "吗", "呢", "吧", "啊", "呀", "哦", "啦", "这", "那",
    "一个", "一起", "自己", "什么", "怎么", "这样", "那样",
    "Do", "Re", "Mi", "Fa", "So", "La", "Si",
}


def main():
    songs = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    total_before = 0
    total_after = 0

    for song in songs:
        words = song.get("lyric_tokens", [])
        filtered_words = [word for word in words if word not in STOPWORDS]
        song["lyric_tokens_no_stopwords"] = filtered_words
        song["lyric_text_no_stopwords"] = " ".join(filtered_words)
        total_before += len(words)
        total_after += len(filtered_words)

    OUTPUT_FILE.write_text(
        json.dumps(songs, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"共处理 {len(songs)} 首歌曲")
    print(f"去停用词前词语数：{total_before}")
    print(f"去停用词后词语数：{total_after}")
    print(f"移除词语数：{total_before - total_after}")
    print(f"输出文件：{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
