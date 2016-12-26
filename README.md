## 运行环境
**python 3.5**

## Email Watcher

> 这是一个接收邮件的工具，它能够通过配置，接收指定的邮箱的指定的人发过来的邮件，
并解析出来的邮件信息，这些解析处理的信息可以存在指定的db文件中，还可以以文件的形式存放在指定的目录中。

### 目录结构


### 工具类 `Utils`
* 路径: `utils.py` 
* 目的: 提供项目中需要的一些公用工具
```python
# e.g.
Utils.removeDQuotes(string) # 去除string中的双引号
```
### 配置
* 路径: `config.py`
* 目的: 解析config/config.json中的配置

### 邮件DB
* 路径：`email_db.py`
* 目的：提供存取邮件的 Sqlite3 的db操作

### 邮件接收
* 路径：`email_receiver.py`
* 目的：登录邮箱，接收邮件

### 元进程
* 路径：`meta_process.py`
* 目的：使用db，邮件服务等去制造自己的工具。
* 描述：这里的作用是定时检查邮箱，获取想要的邮件，存储到db中，
并把内容写到一个以邮件标题为文件名的文件中。

### 服务进程
* 路径：`server_process.py`
* 目的：这里主要是跑 meta_process的

### Animals protecting （极其重要文件，禁止删除）
* 路径：`code_protection.txt`




    
