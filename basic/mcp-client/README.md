## 创建MCP客户端
### 1. 创建项目目录
```bash
uv init mcp-client
cd mcp-client
```

### 2. 创建MCP客户端虚拟环境
```bash
# 创建虚拟环境
uv venv
# 激活虚拟环境
source .venv/bin/activate
```
- 相比pip，uv会自动识别当前项目主目录并创建虚拟环境
- 通过add方法在虚拟环境中安装相关的库
```bash
# 安装 MCP SDK
uv add mcp
```

### 3. 编写基础 MCP 客户端
- 在当前项目主目录中**创建 client.py **
- 基本代码结构
以下是client.py 代码详解，代码核心功能：
- 初始化 MCP 客户端
- *提供一个命令行交互界面
- 模拟 MCP 服务器连接
- 支持用户输入查询并返回「模拟回复」
- 支持安全退出
- asyncio：Python 内置的异步编程库，让 MCP 可以非阻塞地执行任务（比如聊天、查询）。
- mcp.ClientSession：用于管理 MCP 客户端会话（但目前我们先不连接 MCP 服务器）。
- AsyncExitStack：自动管理资源，确保程序退出时正确关闭 MCP 连接。

### 4. 运行 MCP 客户端
然后尝试运行这个极简的MCP客户端：
```bash
uv run client.py
```

### 5. MCP客户端接入OpenAI在线大模型流程
#### (1)安装库
```bash
uv add mcp openai python-dotenv
```

#### (2)创建.env文件
BASE_URL=https://api.deepseek.com
MODEL=deepseek-chat      
OPENAI_API_KEY="DeepSeek API-Key"

#### (3) 修改client.py代码, 引入大模型 -> clint-llm.py
- messages：创建对话上下文，让 OpenAI 知道如何回答问题：
  - system 角色：设定 AI 角色（如“你是一个智能助手”）。
  - user 角色：存储用户输入。
- openai.ChatCompletion.create(...)
  - model="gpt-4"：使用 OpenAI 的 GPT-4 进行对话。
  - messages=messages：提供聊天记录，让 AI 生成回答。
  - max_tokens=1000：限制 AI 生成的最大字数。
  - temperature=0.7：控制 AI 回答的随机性（越高越随机）。
- **run_in_executor(...)：**
  - 因为 OpenAI API 是同步的，但我们用的是异步代码
  - 这里用 **asyncio.get_event_loop().run_in_executor(...)** 将 OpenAI API 变成异步任务，防止程序卡顿。

### 6. MCP客户端接入本地ollama、vLLM模型流程
- 接下来，我们继续尝试将ollama、vLLM等模型调度框架接入MCP的client。
- 由于ollama和vLLM均支持OpenAI API风格调用方法，因此上述client.py并不需要进行任何修改，
- 我们只需要启动响应的调度框架服务，然后修改.env文件即可。

#### (1)MCP客户端接入本地ollama
- ollama start
- ollama list
- ollama run PetrosStav/gemma3-tools:4b
- 修改.env
  BASE_URL=http://localhost:11434/v1/
  MODEL=PetrosStav/gemma3-tools:4b 
  OPENAI_API_KEY=ollama