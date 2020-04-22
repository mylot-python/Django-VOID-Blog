# Django-VOID-Blog

使用Django+VOID开箱即用博客

## 开发环境

**系统:** ubuntu 18.04

**python:** 3.6.8

**前端:** https://github.com/AlanDecode/Typecho-Theme-VOID/releases

**后台:** 默认使用原生后台, 推荐使用 -> https://simpleui.88cto.com/simpleui/ (自行安装)

**依赖:** 项目根目录 `pip install -r requirements.txt`

## 前言

目前使用Django替代了原主题的PHP, 自己完成的逻辑, 目前配置里只使用了sqlite, 如希望其他数据库可以自行修改, 项目内只需修改部分固定写死的参数外, 目前测试均可直接启动.

## 步骤

1. 执行`migrate`: 由于我已经准备好了`makemigrations`, 如模型没修改直接运行即可

2. 执行`createsuperuser`创建超级管理员

3. 修改settings邮箱设置部分: 评论采取邮箱回复提醒

   ```python
   EMAIL_USE_SSL = True
   EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
   EMAIL_PORT = 465
   EMAIL_HOST_USER = '1@1.com'  # 帐号
   EMAIL_HOST_PASSWORD = 'skndlkfdlklkb'  # 授权码（****）
   DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
   ```

4. utils.ExSearch.py: 替换路径

   ```python
   import json, os, logging, mistune
   logger = logging.getLogger('django')
   
   article_url = 'https://你的路径/article/'
   tags_url = 'https:/你的路径/tag/'
   category_url = 'https://你的路径/category/'
   
   tree = {
       "posts": [
       ],
       "pages": [
           {
               "title": "观影",
               "date": "2019-10-10T10:10:00+10:00",
               "path": "你的路径",
               "text": ""
           },
           ..........
       ]
   }
   ```

5. base.html:

   ```python
   文件内搜索定位
   1.searchBase: 搜索索引链接
   2.home: 主页链接
   3.buildTime: 建站时间
   4.breezed | 无风清响: 站内关联词
   5.links: 自己的新浪微博/github等	  
   6.踪迹: 自己的新浪微博/github等	  
   7.<footer></footer>: 内的备案号版本号相关
   8.DoubanAPI/DoubanAPI2: 对应movie和book的json获取链接
   ```

6. send_email.html: 修改href对应链接

7. index.html: banner区文字

**目前修改部分暂且发现这么多, 准备好以后就可以直接运行进入后台操作了**

## 关于缓存优化

目前我自己站点基本静态文件都存储在第三方oss存储里, 或者你喜欢可以用cdn, 我目前没有做缓存优化, 因为打开的速度1秒左右(服务器1核2G内存1M带宽), 已经很快了, 所以优化起来感觉不起效果, 毕竟只是个小站.

## 后台追番/观影/阅读/音乐等使用

- 追番: 

  目前对应添加的是https://bangumi.tv/的数据, 由于页面结构会出现少许不同, 导致少数添加时会出现失败的问题, 这个要修改`utils.CrawlBangumi.py`这个文件增加对应方案, 要遇到问题才能添加优化, 如今大部分可以正常使用.

  番名: 番号名

  番号id: 链接后面的数字就是番号id => bangumi.tv/subject/番号id

- 观影/阅读

  这两者都是对应的豆瓣的数据, 同样也会出现页面结构的问题, 大部分都正常使用, 如有遇到失败的则修改`utils.CrawlDB.py`文件增加对应方案

  剧名/书名: 对应名字

  书/剧id: 链接后面的数字就是书/剧id => douban.com/subject/书/剧id

- 音乐

  使用的是https://github.com/metowolf/MetingJS这款音乐插件, 具体兼容请看链接介绍, 我这里默认使用的网易云, 输入多组每次打开随机选取, 如使用网易云以外的需要修改部分逻辑

## 展示

- 首页

![](https://img.breezed.cn/Django_VOID展示1.png)

- 追番

![](https://img.breezed.cn/Django_VOID展示2.png)

- 观影

![](https://img.breezed.cn/Django_VOID展示3.png)

- 阅读

![](https://img.breezed.cn/Django_VOID展示4.png)

- 音乐

![](https://img.breezed.cn/Django_VOID展示7.png)

- 友链

![](https://img.breezed.cn/Django_VOID展示5.png)

- 归档

![](https://img.breezed.cn/Django_VOID展示6.png)

