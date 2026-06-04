"""
generate.py —— 用 DeepSeek 批量生成营销/课程文案(运营提效)。

业务场景:运营每天要为多个课程/活动写朋友圈、短视频、海报文案,耗时且风格不稳定。
用大模型按统一要求批量生成,人工只做挑选与微调,效率成倍提升。

运行:  python generate.py
需要:复用 06 的 real-rag-system/.env 里的 DEEPSEEK_API_KEY。
若未配置 key,会自动降级为离线模板,保证可演示。
"""

import os
import sys

# 复用 06 的 .env
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
_ENV = os.path.join(_ROOT, "06-ai-development", "real-rag-system", ".env")

# 要批量生成文案的主题
TOPICS = [
    "Python 零基础入门训练营",
    "AI 安全实战公开课",
    "周末亲子编程体验课",
]
STYLE = "小红书风格,30字以内,带 1-2 个 emoji,突出卖点和紧迫感"


def _load_key():
    try:
        from dotenv import load_dotenv
        load_dotenv(_ENV)
    except Exception:
        pass
    return os.environ.get("DEEPSEEK_API_KEY")


def gen_with_deepseek(client, topic):
    prompt = f"为课程『{topic}』写 3 条{STYLE}的推广文案,每条一行,不要编号。"
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
    )
    return resp.choices[0].message.content.strip()


def gen_offline(topic):
    """离线降级模板(无 key 时仍可演示)。"""
    return "\n".join([
        f"🔥 {topic},名额有限,手慢无!",
        f"✨ 0 基础也能学会的{topic},今天报名立减 50",
        f"⏰ {topic}本周开课,错过再等一个月~",
    ])


def main():
    key = _load_key()
    use_api = bool(key)
    client = None
    if use_api:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
        except Exception as e:
            print(f"(初始化 DeepSeek 失败,降级离线模板:{e})")
            use_api = False

    print("=" * 60)
    print("DeepSeek 批量文案生成(运营提效)")
    print(f"模式: {'DeepSeek 在线生成' if use_api else '离线模板(未检测到 API Key)'}")
    print("=" * 60)

    for topic in TOPICS:
        print(f"\n## {topic}")
        try:
            text = gen_with_deepseek(client, topic) if use_api else gen_offline(topic)
        except Exception as e:
            print(f"(在线生成失败,降级离线:{e})")
            text = gen_offline(topic)
        for ln in [l for l in text.splitlines() if l.strip()]:
            print("  -", ln.strip())

    print("\n" + "-" * 60)
    print(f"一次生成 {len(TOPICS)} 个主题 × 3 条文案,运营从'写'变成'挑',效率成倍提升。")


if __name__ == "__main__":
    main()
