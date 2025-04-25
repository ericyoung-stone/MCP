## 一 创建MCP客户端
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

## 二. MCP天气查询服务器server与使用
1. MCP服务器概念介绍
        根据MCP协议定义，Server可以提供三种类型的标准能力，Resources、Tools、Prompts，每个Server可同时提供者三种类型能力或其中一种。
- **Resources：**资源，类似于文件数据读取，可以是文件资源或是API响应返回的内容。
- **Tools：**工具，第三方服务、功能函数，通过此可控制LLM可调用哪些函数。
- **Prompts：**提示词，为用户预先定义好的完成特定任务的模板。

2. MCP服务器通讯机制
Model Context Protocol（MCP）是一种由 Anthropic 开源的协议，旨在将大型语言模型直接连接至数据源，实现无缝集成。
根据 MCP 的规范，当前支持两种传输方式：标准输入输出（stdio）和基于 HTTP 的服务器推送事件（SSE）。
而近期，开发者在 MCP 的 GitHub 仓库中提交了一项提案，建议采用“可流式传输的 HTTP”来替代现有的 HTTP+SSE 方案。
此举旨在解决当前远程 MCP 传输方式的关键限制，同时保留其优势。 
HTTP 和 SSE（服务器推送事件）在数据传输方式上存在明显区别：
- 通信方式：
  - HTTP：采用请求-响应模式，客户端发送请求，服务器返回响应，每次请求都是独立的。
  - SSE：允许服务器通过单个持久的 HTTP 连接，持续向客户端推送数据，实现实时更新。
- 连接特性：
  - HTTP：每次请求通常建立新的连接，虽然在 HTTP/1.1 中引入了持久连接，但默认情况下仍是短连接。
  - SSE：基于长连接，客户端与服务器之间保持持续的连接，服务器可以在任意时间推送数据。
- 适用场景：
  - HTTP：适用于传统的请求-响应场景，如网页加载、表单提交等。
  - SSE：适用于需要服务器主动向客户端推送数据的场景，如实时通知、股票行情更新等。 
- 可流式传输的 HTTP PR：https://github.com/modelcontextprotocol/specification/pull/206


MCP定义了Client与Server进行通讯的协议与消息格式，其支持两种类型通讯机制：标准输入输出通讯、基于SSE的HTTP通讯，分别对应着本地与远程通讯。Client与Server间使用JSON-RPC 2.0格式进行消息传输。
- 本地通讯：使用了stdio传输数据，具体流程Client启动Server程序作为子进程，其消息通讯是通过stdin/stdout进行的，消息格式为JSON-RPC 2.0。
- 远程通讯：Client与Server可以部署在任何地方，Client使用SSE与Server进行通讯，消息的格式为JSON-RPC 2.0，Server定义了/see与/messages接口用于推送与接收数据。

### 天气查询服务器Server创建流程
- 创建一个天气查询的服务器。通过使用OpenWeather API，创建一个能够实时查询天气的服务器（server），并使用stdio方式进行通信。
- OpenWeather官网：https://openweathermap.org/
- 参考注册:https://zhuanlan.zhihu.com/p/656012235
测试:
```bash
curl -s "https://api.openweathermap.org/data/2.5/weather?q=Beijing&appid='3939846a293abe02652360373f4f0118'&units=metric&lang=zh_cn"
```

#### (1)服务器依赖安装
当前虚拟环境中添加如下依赖
uv add mcp httpx

#### (2)服务器代码编写(server_weather.py)
代码解释如下：
1. Part 1. 异步获取天气数据
- 函数 fetch_weather(city: str)
  - 使用 httpx.AsyncClient() 发送异步 GET 请求到 OpenWeather API。
  - 如果请求成功，则调用 response.json() 返回一个字典。
  - 出现异常时，返回包含错误信息的字典。
2. Part 2. 格式化天气数据
- 函数 format_weather(data: dict | str)
  - 首先检查传入的数据是否为字符串，如果是，则使用 json.loads 将其转换为字典。
  - 检查数据中是否包含 "error" 字段，如果有，直接返回错误提示。
  - 使用 .get() 方法提取 name、sys.country、main.temp、main.humidity、wind.speed 和 weather[0].description 等数据，并为可能缺失的字段提供默认值。
  - 将提取的信息拼接成一个格式化字符串，方便阅读。
3. Part 3. MCP 工具 query_weather(city: str)
- 函数 query_weather
  - 通过 @mcp.tool() 装饰器注册为 MCP 服务器的工具，使其能够被客户端调用。
  - 调用 fetch_weather(city) 获取天气数据，然后用 format_weather(data) 将数据格式化为易读文本，最后返回该字符串。
4. Part 4. 运行服务器
- if __name__ == "__main__": 块
- 调用 mcp.run(transport='stdio') 启动 MCP 服务器，采用标准 I/O 通信方式，等待客户端调用。


此外，上述代码有两个注意事项，
1. query_weather函数的函数说明至关重要，相当于是此后客户端对函数进行识别的基本依据，因此需要谨慎编写；
2. 当指定 transport='stdio' 运行 MCP 服务器时，客户端必须在启动时同时启动当前这个脚本，否则无法顺利通信。这是因为 stdio 模式是一种本地进程间通信（IPC，Inter-Process Communication）方式，它需要服务器作为子进程运行，并通过标准输入输出（stdin/stdout）进行数据交换。
因此，当我们编写完服务器后，并不能直接调用这个服务器，而是需要创建一个对应的能够进行stdio的客户端，才能顺利进行通信。

### 天气查询客户端client创建流程(client_weather.py)
- 运行两个py文件:
```bash
uv run client_weather.py server_weather.py
```
- 提问:
请问北京今天天气如何？


#### 代码解释
1. 导入必要库
  - asyncio：支持异步编程
  - os / json：读取环境变量、解析 JSON
  - typing.Optional：类型提示
  - contextlib.AsyncExitStack：用于安全管理异步资源（如 MCP 连接）
  - openai.OpenAI：你的自定义 OpenAI Client 类
  - dotenv.load_dotenv：从 .env 文件加载环境变量（如 API Key）
  - MCP 相关：mcp.ClientSession, mcp.client.stdio, StdioServerParameters
2. self.exit_stack = AsyncExitStack()
  - 用于 统一管理异步上下文（如 MCP 连接）的生命周期。
  - 可以在退出（cleanup）时自动关闭。

3. 从mcp服务器获取工具列表,构建可用工具数据结构
- list_tools()：向 MCP 服务器请求所有已注册的工具（用 @mcp.tool() 标记）。
- 打印工具列表，例如 ["get_forecast", "query_db", ...]。
- 获取服务器上的工具，再转换成 available_tools 的格式。
- 这里你自定义了一个结构：每个工具对应一个 {"type": "function", "function": {...}} 的字典。
- 方便后面发给 OpenAI，告诉它：可以调用这些工具。
- tools=available_tools：让模型知道有哪些可调用的「函数」。这是你自定义的**“Function Calling”**协议（非官方 JSON schema）。

4. 工具响应
   1. if content.finish_reason == "tool_calls":
      - 如果模型的输出表示「想调用工具」，它会在 content.message.tool_calls 列表中声明要用哪个函数、参数是什么。
      - 这是你自定义的一种函数调用机制，和官方 function_call 格式略有不同，但逻辑相似。
   2. 取出工具名 tool_name 和参数 tool_args，再调用 self.session.call_tool(tool_name, tool_args) 执行 MCP 工具。
   3. 把工具调用结果以「role=tool」的形式写入 messages。这样相当于把“函数调用结果”再喂给模型。
   4. 再次调用 OpenAI，让模型阅读到这个新上下文，产出最终回答。
   5. 如果没有要调用工具，直接返回 content.message.content（模型的文本回答）。

#### 代码总结如下：
1. MCPClient 的主要职责：
  - 启动 MCP 服务器（通过 StdioServerParameters）
  - 建立 MCP 会话，列出可用工具
  - 处理用户输入，将其发送给 OpenAI 模型
  - 如果模型想调用 MCP 工具（Function Calling），就执行 call_tool
  - 将结果重新发给模型，并返回最终回答
2. Function Calling 逻辑（你的自定义版）：
  - tools=available_tools：在 completions.create 时告诉模型有哪些工具可用。
  - 模型返回 finish_reason=="tool_calls" → 说明它想用工具。
  - 解析 tool_calls[0]，执行 MCP 工具 → 再次发给模型 → 返回最终答案。
3. 为什么要两次请求？
  - 第一次：模型根据你的指令，决定要不要用工具
  - 如果需要用工具 → 返回工具名称和参数 → 执行工具 → 把结果作为新的上下文发给模型
  - 第二次：模型基于工具结果给出最终回答