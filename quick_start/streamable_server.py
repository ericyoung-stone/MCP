import logging
import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# 创建日志记录器，命名为当前模块名
logger = logging.getLogger(__name__)

# 从环境变量获取主机地址，HOST默认为"0.0.0.0"（监听所有网络接口）,PORT默认为8000
load_dotenv()
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Stateful server (maintains session state)
# mcp = FastMCP("StatefulServer")

# Stateless server (no session persistence)
# mcp = FastMCP("StatelessServer", stateless_http=True)

# Stateless server (no session persistence, no sse stream with supported client)
mcp = FastMCP("StatelessServer", stateless_http=True, json_response=True, host=HOST, port=PORT, log_level="INFO")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Run server with streamable_http transport
mcp.run(transport="streamable-http", mount_path='/mcp')