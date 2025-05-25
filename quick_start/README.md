## 安装环境依赖
- pip install --upgrade mcp(需要>=1.8.0)
- pip install -U 'mcp[cli]' (用于debug, 执行mcp dev server.py进入调试工具)
- pip install requests==2.32.3
- pip install mysql-connector-python==9.3.0
- pip install fastapi==0.115.12
- pip install starlette==0.46.2
- pip install sse-starlette==2.3.4
- pip install uvicorn==0.34.2

## 配置.env
- 将env.template修改为.env

## 运行client.py 和 server.py
- cd 到quick_start目录
- 运行python amap_server.py
- 客户端见advanced中


### 开发debug模式(使用inspector)
- cd 到quick_start目录
- mcp dev amap_server.py
