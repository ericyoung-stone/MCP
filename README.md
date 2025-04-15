# MCP

## 创建MCP客户端(mcp-client)
https://kq4b3vgg5b.feishu.cn/wiki/HhPmwc7TSikFpSkpUFDcGZ8PnCf

- **运行inspector(监控mcp服务)**
```bash
conda activate mcp
cd ./mcp-client
source .venv/bin/activate
npx -v
npx -y @modelcontextprotocol/inspector uv run server_weather.py
```