## 一、基于HTTP流式传输的MCP服务器开发流程
- 创建项目文件：
```bash
# cd /root/autodl-tmp/MCP
uv init mcp-weather-http
cd mcp-weather-http
# 创建虚拟环境
uv venv
# 激活虚拟环境
source .venv/bin/activate
uv add mcp httpx
```

## 代码解释
如果你传的是 --port 3000，访问路径就是 http://localhost:3000/mcp

## 修改配置文件pyproject.toml：
- 参考:
```bash
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mcp-weather-http"
version = "1.1.0"
description = "输入OpenWeather-API-KEY，获取天气信息。"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "httpx>=0.28.1",
    "mcp>=1.8.0",
]

[project.scripts]
mcp-weather-http = "mcp_weather_http:main"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

## 二、HTTP流式传输MCP服务器开启与测试
- 在创建完server.py后，我们可以开启服务并进行测试。需要注意的是，我们需要先开启流式HTTP MCP服务器，然后再开启Inspector：
### 开启流式HTTP MCP服务器
```bash
# 回到项目主目录
# cd /root/autodl-tmp/MCP/mcp-weather-http

uv run ./src/mcp_weather_http/mysql_server.py --port 3001 --api-key YOUR_KEY
```
### 开启Inspector
```bash
# 回到项目主目录
# cd /root/autodl-tmp/MCP/mcp-weather-http
# source .venv/bin/activate

npx -y @modelcontextprotocol/inspector
```
访问: MCP Inspector is up and running at http://127.0.0.1:6274
进入inspector界面:
- Transport Type选择“Streamable HTTP”
- URL设置 http://localhost:3001/mcp
- connect连接成功

##  三、流式HTTP MCP服务器异地调用
- 接下来即可在异地环境（也可以是本地）通过HTTP方式调用MCP服务了。
- 这里以本地安装的Cherry Studio为例，进行调用演示。
- 此处需要保持远程流式HTTP MCP服务器处于开启状态，然后配置即可。

## 四、流式HTTP MCP服务器发布流程
- 测试完成后，即可上线发布。这里仍然考虑发布到pypi平台，并使用cherry studio进行本地调用测试。

### 打包上传：
```bash
# 回到项目主目录
# cd xx/MCP/mcp-http-streamable

uv pip install build twine
python -m build
python -m twine upload dist/*

# View at: https://pypi.org/project/mcp-http-streamable-ysx-test/0.1.0/
```

### 下载运行
- pip install mcp-http-streamable-ysx-test
- 开启服务：uv run mcp-http-streamable-ysx-test --port 3002 --api-key YOUR_API_KEY
- 使用Inspector连接测试


