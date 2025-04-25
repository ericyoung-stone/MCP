import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client


async def main():
    while True:
        # 等待用户输入
        url = await asyncio.get_event_loop().run_in_executor(None, input, 'URL:')

        try:
            # 建立sse连接
            async with sse_client('http://localhost:8000/sse') as streams:
                async with ClientSession(*streams) as session:
                    await session.initialize()
                    # 调用mcp的tool, session中包含session_id, 等带SSE流推送结果
                    result = await session.call_tool('fetch', {'url': url})
                    print(result)  # 注意代理问题
        except Exception as e:
            print('can not connect to mcpserver')

if "__main__" == __name__:
    asyncio.run(main())