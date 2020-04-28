### sublime 快捷键
 1. Ctrl+L 选择整行（按住-继续选择下行）

 2. Ctrl+KK 从光标处删除至行尾
 3. Ctrl+Shift+K 删除整行
 4. Ctrl+Shift+D 复制光标所在整行，插入在该行之前
 5. Ctrl+J 合并行（已选择需要合并的多行时）
 6. Ctrl+KU 改为大写
 7. Ctrl+KL 改为小写
 8. Ctrl+D 选词 （按住-继续选择下个相同的字符串）
 9. Ctrl+M 光标移动至括号内开始或结束的位置
10. Ctrl+Shift+M 选择括号内的内容（按住-继续选择父括号）
11. Ctrl+/ 注释整行（如已选择内容，同“Ctrl+Shift+/”效果）
12. Ctrl+Shift+/ 注释已选择内容
13. Ctrl+Z 撤销
14. Ctrl+Y 恢复撤销
15. Ctrl+M 光标跳至对应的括号
16. Alt+. 闭合当前标签
17. Ctrl+Shift+A 选择光标位置父标签对儿
18. Ctrl+Shift+[ 折叠代码
19. Ctrl+Shift+] 展开代码
20. Ctrl+KT 折叠属性
21. Ctrl+K0 展开所有
22. Ctrl+U 软撤销
23. Ctrl+T 词互换
24. Tab 缩进 自动完成
25. Shift+Tab 去除缩进
26. Ctrl+Shift+↑ 与上行互换
27. Ctrl+Shift+↓ 与下行互换
28. Ctrl+K Backspace 从光标处删除至行首
29. Ctrl+Enter 光标后插入行
30. Ctrl+Shift+Enter 光标前插入行
31. Ctrl+F2 设置书签
32. F2 下一个书签
33. Shift+F2 上一个书签
34. Ctrl+Alt+↑/↓ 设置光标扩展
35. Ctrl+↑ 数字加一
36. Ctrl+↓ 数字减一

### 离线下载、安装python包
```
python -m pip install -U pip
mkdir package && cd package
pip freeze > requirements.txt
pip download -r requirements.txt
pip install --no-index --find-links=package -r requirements.txt

```

### pipenv 常用命令 
1. pip install --user --upgrade pipenv # 用户安装pipenv 

2. pipenv --three # 会使用当前系统的Python3创建环境 
3. pipenv --two # 使用python2创建 
4. pipenv --python 3.6 指定某一Python版本创建环境 
5. pipenv run python 文件名 pipenv run pip ...# 运行pip 
6. pipenv shell 激活虚拟环境 
7. pipenv --where 显示目录信息 
8. pipenv --venv 显示虚拟环境信息 
9. pipenv --py 显示Python解释器信息 
10. pipenv install requests 安装相关模块并加入到Pipfile 
11. pipenv install django==1.11 安装固定版本模块并加入到Pipfile 
12. pipenv graph # 显示依赖图 
13. pipenv check #检查安全漏洞 
14. pipenv lock # 生成lockfile
15. pipenv update # 更新所有的包
16. pipenv --rm # 删除虚拟环境
17. pipenv uninstall requests # 卸载包并从Pipfile中移除 
18. pipenv uninstall --all # 卸载全部包
19. pipenv update --outdated  # 列出所有需要更新的包
20. pipenv update  # 更新所有包
21. pipenv update <包名>  # 更新指定包
22. pipenv install -r path/requirements.txt  # 安装requirements包
23. pipenv run python --version  # 不想启动shell 直接在虚拟环境中执行命令
24. pipenv lock -r  # 将Pipfile和Pipfile.lock里面的包导出为requirements.txt
25. pipenv lock -r --dev  # 导出开发环境的包


### pip国内源
- https://pypi.tuna.tsinghua.edu.cn/simple

- http://mirrors.aliyun.com/pypi/simple/
- http://pypi.douban.com/simple/
- http://pypi.mirrors.ustc.edu.cn/simple/
- http://pypi.hustunique.com/

### 永久修改pip源
```
vim ~/.pip/pip.conf

[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn
```

### http 常用状态码
status | description | method | explanation
-|-|-|-|
200 | OK | [GET] | 服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。
201 | CREATED | [POST/PUT/PATCH] | 用户新建或修改数据成功。
202 | Accepted | [*]| 表示一个请求已经进入后台排队（异步任务）
204 | NO CONTENT | [DELETE] | 用户删除数据成功。
400 | INVALID REQUEST | [POST/PUT/PATCH] | 用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
401 | Unauthorized | [*] | 表示用户没有权限（令牌、用户名、密码错误）。
403 | Forbidden | [*] | 表示用户得到授权（与401错误相对），但是访问是被禁止的。
404 | NOT FOUND | [*] | 用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
406 | Not Acceptable | [GET] | 用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
410 | Gone | [GET] | 用户请求的资源被永久删除，且不会再得到的。
422 | Unprocesable entity | [POST/PUT/PATCH] | 当创建一个对象时，发生一个验证错误。
500 | INTERNAL SERVER ERROR | [*] | 服务器发生错误，用户将无法判断发出的请求是否成功


### django models orm 常用字段方法
method | explanation
-|-|
__isnull=True/False | 是否为null
__in                | 在其中
__startswith        | 以…开头
__istartswith       | 以…开头 忽略大小写
__endswith          | 以…结尾
__iendswith         | 以…结尾，忽略大小写
__range             | 在…范围内
__year              | 日期字段的年份
__month             | 日期字段的月份
__day               | 日期字段的日
__exact             | 精确等于 like 'aaa'
__iexact            | 精确等于 忽略大小写 ilike 'aaa'
__contains          | 包含 like '%aaa%'
__icontains         | 包含 忽略大小写 ilike '%aaa%'，但是对于sqlite来说，contains的作用效果等同于icontains。
filter()            | 过滤查询对象。
exclude()           | 排除满足条件的对象
annotate()          | 使用聚合函数
order_by()          | 对查询集进行排序
reverse()           | 反向排序
distinct()          | 对查询集去重
values()            | 返回包含对象具体值的字典的QuerySet
values_list()       | 与values()类似，只是返回的是元组而不是字典。
dates()             | 根据日期获取查询集
datetimes()         | 根据时间获取查询集
none()              | 创建空的查询集
all()               | 获取所有的对象
union()             | 并集
intersection()      | 交集
difference()        | 差集
select_related()    | 附带查询关联对象
prefetch_related()  | 预先查询
extra()             | 附加SQL查询
defer()             | 不加载指定字段
only()              | 只加载指定的字段
using()             | 选择数据库
select_for_update() | 锁住选择的对象，直到事务结束。
raw()               | 接收一个原始的SQL查询

### django orm 竞争避免（加行锁）
```python
from django.db import transaction
with transaction.atomic():
    product = (
        Product.objects
        .select_for_update()
        .get(id=1)
    )
    product.inventory -= 1
    product.save()
```

### django orm 创建或更新
```python
obj, created = Person.objects.update_or_create(
    first_name='John', last_name='Lennon',
    defaults={'first_name': 'Bob'},
)  
# 根据first_name和last_name在数据库中查找匹配的对象，找到则更新defaults中的内容，找不到则创建新的对象
```


### django 使用相关
#### 单词理解 
word | explanation
-|-
urls | 链接
view | 视图
shortcuts | 捷径
contrib | 构建
decorators | 装饰
core | 核心
uploadedfile | 上传文件

#### 组件理解
<!-- from Django.conf import settings -->
1. urls相关操作
```python
from django.urls import path, re_path, include
from django.urls import reverse  
# 注意reverse 和另一个reversed区别。前者要明确导入通过名称解析出地址，后者是built-in内置不用导入；两者功能也不一。
```
2. HttpResponse生成
```python
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse 
# 响应一个content-type：text/json 返回一个json响应报文,相应的浏览器端也不用在对json反解
return JsonResponse(
    {'name':'sgt','password':'1888888'},
    json_dumps_params={'ensure_ascii':False}
   ) 
# json_dumps_params={'ensure_ascii':False}这个的作用是，将Django默认转码功能取消，这样就能显示汉字了
```
3. 认证组件auth
```python
from django.contrib import auth  # contrib 意味：构件
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
```
4. 表单组件forms
```python
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError  
# django的异常定义都在django.core.exceptions模块中，该异常用于自定义钩子。
from django.forms import ModelForm  
# 如果一个form的字段数据是被用映射到一个django models.那么一个ModelForm可以帮助你节约很多开发时间。因为它将构建一个form实例，连同构建适当的field和field attributes，利用这些构建信息，都来自一个Model class. 
```
5. 邮件组件
```python
from django.core.mail import send_mail
```
6. model组件
```python
from django.db import models
from django.db.models import F, Q
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import transaction  # 利用model做数据库的事务操作
```
7. 分页器相关
```python
from django.core import paginator
```
8. django admin site相关
```python
from django.contrib import admin
from django.contrib.admin import ModelAdmin
```
9. view 相关
```python
from django.view import View  # 用于media访问内置视图
```
10. 中间件
```python
from django.utils.deprecation import MiddlewareMixin
```
11. template模版相关
```python
from django import template  
# 自定义tag和filter需要用到settings.py文件中有一个TEMPLATES配置，DIRS列表中存放所有的模板路径，在视图中使用render或者是render_to_string渲染模板时会在这个列表的路径中查找模板。APP_DIRS默认为True，会在INSTALLED_APPS中注册了的app下面的templates文件夹中查找。查找顺序：render("index.html")，会先在DIRS这个列表中依次查找路径下有没有这个模板，如果有就返回，如果在DIRS列表中没有找到模板，那么会先检查当前视图所属的app是否在INSTALLED_APPS中注册了，如果已注册首先会在当前app下面的templates文件夹下查找，如果还没找到就会在其他已经注册了的app下面的templates文件夹下寻找，最后还没找到就会抛出TempalateDontExist异常。
```
12. 工具
```python
from django.utils.module_loading import autodiscover_modules 
# 自动发现项目下所有注册app的指定模块并将其加载导入执行。
from django.utils.safestring import mark_safe 
# 由于django的模版引擎 出于安全原因，在生成html字符串时，会将与html相关的特殊字符进行转义。这时如果是我们后台自己要输出html字符，那么就需要提前将字符通过mark_safe处理一下，再用于模版解析中就不会出现 html标签也展示在页面上的情况了。
from django.core.files.uploadedfile import SimpleUploadedFile
# 上传文件
```

### python3 str to bytes
```python
bytes(s, encoding = "utf8")
str.encode(s)
```

### python3 bytes to str
```python
str(b, encoding = "utf-8")
bytes.decode(b)
```

<!-- vars() 函数返回对象object的属性和属性值的字典对象。 -->

### requests常用方法
- get(url, params=None, **kwargs)

- post(url, data=None, json=None, **kwargs)
- r.status_code 响应状态码
- r.raw 原始响应体，使用r.raw.read()读取
- r.content 字节方式的响应体，需要进行解码
- r.text 字符串方式的响应体，会自动更具响应头部的字符编码进行解码
- r.headers 以字典对象储存服务器响应头，但是这个字典比较特殊，字典键不区分大小写，若键不存在，则返回None
- r.json() request中内置的json解码器
- r.raise_for_status() 请求失败(非200响应)，抛出异常
- r.url 获取请求的url
- r.cookies 获取请求后的cookies
- r.encoding 获取编码格式

### python时间转换 
1. 字符串转对象
```python
import datetime
first_time = "2019-09-10 16:59:34"
datetime.datetime.strptime(first_time, '%Y-%m-%d %H:%M:%S')
```

2. 对象转字符串
```python
import datetime
first_time = datetime.datetime.now()
datetime.datetime.strftime(first_time, '%Y-%m-%d %H:%M:%S')
```

### 解决git ignore不生效
```
git rm -r --cached .
git add .
git commit -m 'update .gitignore'
```