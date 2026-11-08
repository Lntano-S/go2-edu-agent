import os

# 清掉所有代理环境变量。
# 这台机器上除了 http_proxy，还有一组 socks5 的：WS_PROXY / WSS_PROXY / ws_proxy / wss_proxy，
# 少清一个，httpx 就会撞上 "Using SOCKS proxy" 那个错。
# 访问本机（127.0.0.1）的服务不需要任何代理，全清最省心。
for _k in list(os.environ):
    if "proxy" in _k.lower():
        os.environ.pop(_k, None)

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY", "sk-no-key"),
    base_url=os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:18777/v1"),
)

model = os.environ.get("MODEL", "qwen3")

user_input = input("你: ")

response = client.chat.completions.create(
    model=model,
    max_tokens=1000,
    messages=[{"role": "user", "content": user_input}],
)

answer = response.choices[0].message.content
print(f"[Agent回答]: {answer}\n")
