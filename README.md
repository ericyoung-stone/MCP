# MCP

## (1)创建MCP客户端(mcp-client)
https://kq4b3vgg5b.feishu.cn/wiki/HhPmwc7TSikFpSkpUFDcGZ8PnCf

- **运行inspector(监控mcp服务)**
```bash
conda activate mcp
cd ./mcp-client
source .venv/bin/activate
npx -v
npx -y @modelcontextprotocol/inspector uv run server_weather.py
```


## (2)30行代码实现 MCP SSE
参考:https://www.bilibili.com/video/BV1PYdBYcEg9/?spm_id_from=333.788.top_right_bar_window_custom_collection.content.click&vd_source=543b2dcf5d331a68c9841120068cfd8b
代码:https://github.com/owenliang/mcp-sse-python
