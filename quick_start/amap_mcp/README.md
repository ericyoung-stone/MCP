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

## 测试
测试问题，可参考如下:                                
- (1)这个118.79815,32.01112经纬度对应的地方是哪里                           
- (2)夫子庙的经纬度坐标是多少                  
- (3)112.10.22.229这个IP所在位置                   
- (4)上海的天气如何      
- (5)我要从苏州的虎丘区骑行到相城区，帮我规划下路径            
- (6)我要从苏州的虎丘区步行到相城区，帮我规划下路径            
- (7)我要从苏州的虎丘区驾车到相城区，帮我规划下路径              
- (8)我要从苏州的虎丘区坐公共交通到相城区，帮我规划下               
- (9)测量下从苏州的虎丘区到相城区驾车距离是多少               
- (10)在苏州虎丘区中石化的加油站有哪些，需要有POI的ID                
- (11)POI为B020016GPH的详细信息                
- (12)在苏州乐园周围10公里的中石化的加油站     