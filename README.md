# go2-edu-agent

手搓一个小 Agent：自己写 loop、tools、executor，接本地 LLM。

不套 LangChain 那类框架——框架替你做的那些事，正是要学的东西。

## 当前阶段

阶段②。眼下只跑通「一句话进，一句话出」的最小闭环；工具和循环随后加。

## 结构

| 文件 | 职责 |
|---|---|
| `main.py` | 入口，最小可跑的对话 |
| `llm.py` | LLM 接入层，只负责调 OpenAI 兼容接口 |
| `tools/` | 工具注册表，`@tool` 装饰器 + 各个工具 |
| `executor.py` | 裁决者：工具存在吗？参数合法吗？当前状态允许吗？ |
| `loop.py` | Agent Loop，带最大轮数保护 |
| `trace.py` | 每一轮 prompt / tool call / 结果落盘 |
| `skills/` | 流程知识，用 markdown 写，可加载 |
| `tests/` | 离线测试，mock LLM + mock 工具，不接服务器也能验 |

## 快速开始

```bash
uv sync                    # 建环境、装依赖
cp .env.example .env       # 填地址（本地服务不需要真 key）
uv run python main.py
```

## 配置

`.env` 三个变量：

| 变量 | 说明 |
|---|---|
| `OPENAI_BASE_URL` | llama-server 的地址，**必须以 `/v1` 结尾** |
| `OPENAI_API_KEY` | 本地服务不校验，填占位符即可 |
| `MODEL` | `curl $OPENAI_BASE_URL/models` 里报出来的名字 |

## 一个容易踩的坑：服务在远端

llama-server 默认只监听服务器的 `127.0.0.1`，笔记本**直接连不到**。两种做法：

```bash
# A. SSH 端口转发：本地 18080 打通到服务器的 18080
#    <port> <user> <host> 换成你自己的服务器信息（这类信息不进仓库）
ssh -N -L 18080:127.0.0.1:18080 -p <port> <user>@<host>
# 这样 .env 里写 http://127.0.0.1:18080/v1 就对

# B. 让服务监听所有网卡（需注意这会把端口暴露到公网）
#    llama-server ... --host 0.0.0.0
```
