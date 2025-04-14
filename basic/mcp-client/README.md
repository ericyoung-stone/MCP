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

### 5. MCP客户端接入OpenAI
#### (1)安装库
```bash
uv add mcp openai python-dotenv
```

#### (2)创建.env文件

