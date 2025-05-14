from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
import uvicorn
import httpx

mcpserver=FastMCP(name='website fetcher') # handle session 逻辑层, 维护session_id与sse的映射表;tools
sse_transport=SseServerTransport('/messages/') # handle io(sse连接, post请求) io层,做转发

# 实现一个tool,功能是根据传的参数url去抓取网页的内容,然后返回
@mcpserver.tool(name='fetch',description='Fetches a website and returns its content')
async def fetch_website(url: str):
    print('fetching....')
    if not url.startswith('http://') and not url.startswith('https://'):
        url='https://'+url
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response=await client.get(url)
        if response.status_code != 200:
            return f'Error fetching {url}: {response.status_code}'
        return response.text

# 将http请求转换成mcp_server的sse长连接
async def sse_handler(request):
    async with sse_transport.connect_sse(request.scope,request.receive,request._send) as streams:
        await mcpserver._mcp_server.run(streams[0],streams[1],mcpserver._mcp_server.create_initialization_options()) # run and keep sse session, 入参:发送,接收,mcp_server的初始化上下文


if __name__ == '__main__':
    app=Starlette(
        debug=True,
        routes=[
            Route('/sse',endpoint=sse_handler), # 第一次请求握手, 通过sse_handler转换成sse长连接,
            Mount('/messages/',app=sse_transport.handle_post_message)  # 调用tool的请求,携带session_id,去找到对应的sse长连接,然后将结果sse推送给用户
        ]
    )
    uvicorn.run(app,host='0.0.0.0',port=8000)