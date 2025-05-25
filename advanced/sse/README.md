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

## 启动和配置mysql数据库, 建表,连接mysql
- 启动docker
- 打开docker命令行终端，进入到mysql_config/docker-compose.yaml文件所在的目录，运行指令 docker-compose up -d                
- 启动成功后，通过数据库客户端软件连接到本地数据库，并将students_info.sql和students_score.sql文件导入到数据库中作为测试数据表
- ![img.png](img.png)

## 运行client.py 和 server.py
- cd 到sse目录
- 运行python server.py
- 运行python client.py

### 开发debug模式(使用inspector)
- cd 到sse目录
- mcp dev server.py


## 测试集
测试问题，可参考如下:                                
- (1)有哪些表可以使用                                             
- (2)查询学生信息表中数据                                                   
- (3)查询学生成绩表中数据                                               
- (4)查询学生成绩表中分数最高的                                              
- (5)对学生信息表和学生成绩表进行联表查询，生成每个学生姓名、成绩                     
- (6)将学生姓名为张三的改为钱八，并获取最新的信息表