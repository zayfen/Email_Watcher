# db目录

## 1，目录的作用
存放指定发件人发送到`config.json`中指定地址的邮件，指定发件人通过白名单列表设置

## 2，DB文件名和路径
email.db 可以通过 `config.json`进行配置

## 3，Table名字
t_email

## 4, 字段

| 字段 | 类型 | 描述 |
|id | Integer | t_email的id，也是主键|
|date| TEXT | email 的日期 |
|from_ | TEXT | email的来源（谁发的）|
| to | TEXT | email的目的地(发给谁) |
| subject | TEXT | email的主题 |
|content | TEXT | email 的内容 |

> date, from_, to, subject, content 所存的内容都是base64编码的





