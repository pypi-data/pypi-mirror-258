# 大智慧远程cookies获取集群接口(fincookie)

## 介绍

* 基于Playwright的远程获取cookies集群，创建可以访问集群的接口，用户可通过调用接口函数创建和操作浏览器，然后获取浏览器Cookies和UA等信息
* 浏览器集群源码地址：https://gitee.com/yl153977/finchina-remote-cookies
* fincookie当前版本：**0.3.4**
* fincookie安装：`pip install fincookie -i http://10.55.3.250:8081/repository/pypi-public/simple --trusted-host 10.55.3.250`
* <font color='orange'>请将使用最新版本，升级命令：</font>`pip install fincookie --upgrade -i http://10.55.3.250:8081/repository/pypi-public/simple --trusted-host 10.55.3.250`


## 版本更新

* 0.2.3: 增加channel参数用于指定浏览器，当前可选chromium、firefox，默认chromium，如需扩增chrome,msedge,webkit请联系
* 0.2.4:
  * 本地浏览器集群已经部署，cookies和proxy自动匹配，无需match_proxy参数
  * 删除fincookie中的get_logs函数，用户可通过下面地址随时刷新日志
  * 日志查看增加随时刷新功能, 具体参考： [get_logs](#get_logs)
* 0.2.5
  * 新增 build_headers 方法，方便构造新的请求头，具体参考 [build_headers](#build_headers)
* 0.2.6
  * 兼容python3.7，去除使用`:=`
* 0.3.1
  * 新增 build_request 方法, 方便用户在cookies更新时无需再重新构造请求，具体参考 [build_request](#build_request)
* 0.3.2
  * 修改 build_request 方法，只有在正确响应cookies且状态码和指定内容都正确的情况下才返回响应 requests.Response，否则返回None
* 0.3.3
  * 修改一些bug
* 0.3.4
  * 函数参数类型声明时使用param: List[int] = None 在Python3.9版本之前不可用，将其修改
* 0.3.4（2024-01-29）
  * 添加提取网页内容功能，可通过将wait_for参数设置为xpath、re、json进行匹配，匹配字符为selector字段，如此设置返回值会有一个match字段的列表为匹配到的字符串
* 0.3.5（2024-02-18）
  * 添加动态代理10.55.7.57:8081,该代理仅华为云服务器可用，每5分钟变化一次，也可人为改变
  * 添加get_dynamic_proxy函数，获取当前动态代理，也可请求GET:http://10.55.3.41/get_dynamic_proxy 获取当前动态代理
  * 添加函数set_dynamic_proxy(proxy, timeout=300)，设置动态代理，proxy为代理地址，timeout为超时时间，单位为秒，改时间过后自动更换，也可通过请求GET:http://10.55.3.41/set_dynamic_proxy?proxy=xxx&timeout=xxx 设置动态代理

## APIs

### get_cookies

通过该接口创建和操作集群浏览器，返回Cookies、User-Agent、Proxy等信息  
**Parameters**:

* **appid:** string(required), 用户自定义的浏览器标识,服务器根据该参数为请求分配浏览器，结合renew_interval参数，同一appid的请求在renew_interval时限内会在同一浏览器上继续操作，直到renew_interval过期后关闭该appid的浏览器

* **get_last:** int, 若为`0`通过操作浏览器获取结果，若为`1` 不进行浏览器操作，直接返回appid的上次cookies结果，如果没有则重新获取(其他并发的get_last为1或者2的线程等待)，若为`2`
  清除并重新获取历史结果，其他get_last为1或者2的线程等待结果获取完成之后直接使用，避免多线程重复操作浏览器。默认为`0`。

* **block_timeout:** int, 同appid的多个请求同时操作浏览器时浏览器的阻塞时间(ms)，如果为`0`则不阻塞，若浏览器正在使用直接返回`浏览器繁忙`错误，默认为`0`

* **proxy:** str, 手动传入代理地址，"auto"根据服务器可选代理列表随机选择代理, 
  * 本地可选代理列表为['10.17.206.27:808', '10.17.206.28:808', '10.17.205.91:808']
  * 华为云可选代理列表为['10.55.7.39:808', '10.55.9.250:808', '10.55.9.67:808']

* **url:** string, 用户请求网址，如果用户需要请求网址，可传入该参数

* **url_timeout:** int, 用户请求网址的超时时间（ms），如果在该时间内浏览器未完成请求，则请求失败，默认值: 30,000。注:如果网址响应时间过长，可以将该值设置为较大的值，避免网址未响应完全

* **script:** string, 用户需要在浏览器中执行的JavaScript代码，如果用户需要执行JavaScript代码，可传入该参数

* **wait_for:** string, 用户需要等待的操作，
  * `timeout`等待一定时间 
  * `selector`等待元素选择器出现响应

* **wait_timeout:** int, `wait_for`等待的时间（ms），结合wait_for参数使用, 默认值: 30,000。

* **selector:** string, 
  * wait_for参数值为`selector`时对应的元素CSS选择器或者XPath，用于选择需要等待或获取的元素
  * wait_for参数值为`xpath`时对应的元素XPath，用于提取网页内容
  * wait_for参数值为`re`时对应的元素正则表达式，用于提取网页内容
  * wait_for参数值为`json`时对应的元素json key，用于提取网页内容,如`@data@rows`,也可以提取列表如`@data@rows@0`提取@data@rows的第一个元素

* **state:** string, wait_for参数为selector时对应的元素等待状态，`visible`: 等待元素在页面中可见 `hidden`: 等待元素在页面中隐藏 `attached`: 等待选择器附加到 DOM 上  `detached`:
  等待选择器从 DOM 上分离

* **action:** string, 等待元素之后对元素进行的操作,
  * `click`: 单击，
  * `dblclick`: 双击，
  * `type`: 输入文字或按键
  * `xpath`结合selector使用xpath提取网页内容
  * `re`结合selector使用正则提取网页内容
  * `json`结合selector使用json key提取网页内容，

* **type_string:** string, 
  * `action`为`type`时输入的字符
  * `action`参数值为`xpath`时对应的元素XPath，用于提取网页内容
  * `action`参数值为`re`时对应的元素正则表达式，用于提取网页内容
  * `action`参数值为`json`时对应的元素json key，用于提取网页内容，如`@data@rows`,也可以提取列表如`@data@rows@0`提取@data@rows的第一个元素

* **renew_interval:** int, appid对应浏览器的保留时间（ms），在保留时间内appid相同的请求会由同一浏览器继续执行后返回，每次请求后刷新, 默认值：3000

* **channel:** str, 浏览器类型，['chromium', 'firefox']，默认为chromium

**Returns:** -> Dict

* `appid`: string, 用户指定的appid
* `request_id`: string, 用户发起请求的唯一标识
* `message`: string, 响应消息，请求成功时该字段为`success`, 请求失败时，该字段为失败或者错误原因
* `cookies`: dict, 请求成功时浏览器的cookies信息
* `user-agent`: string, 请求成功时浏览器的UA信息
* `proxy`: string, 浏览器当前代理
* `server_ip`: string, 响应请求的服务器IP
* `match`: list[str] 当wait_for或者action为`xpath``re``json`时匹配的内容

**返回消息的一些解释**
* 浏览器操作错误：在进行浏览器操作时出现的错误，如请求地址或者等待指令超时，浏览器被意外关闭、代理连接失败等
* 服务器负载已满：浏览器集群服务器内存占用超过95%时无法进行浏览器操作
* 历史响应等待超时：get_last参数为1/2时，相同appid的其他请求超时，该请求无法及时获取响应


**Examples:**

* 示例一: 简单请求一个网址

```python
from fincookie import get_cookies
from pprint import pprint

cookie_data = get_cookies(
    appid="3016993217496905",  # appid
    url="https://www.zjzwfw.gov.cn/zjservice/matter/punishment/searchallpunishlist.do?pageNo=1&areacode=331000",  # 请求网址
)
pprint(cookie_data)
```

响应内容为：

```text
{'appid': '3016993217496905',
 'cookies': {'ZJZWFWSESSIONID': '5c7877b4-fb18-4850-a68d-28bb67c7e6da',
             'acw_tc': 'ac11000117049401068818049e4b1015eebb3daaa1a9f9875d242ab6bb358c',
             'aliyungf_tc': '0300863b975d634626dd98f8a35404c866131c34b3f7ee4a32b04844b4309b3a',
             'ssxmod_itna': 'QqfhYKGK4GhDkDRDl31I50=jeYveTnTI9poDs5eTDSxGKidDqxBneC4DtQTrh=gRCf2DQmzCfuvW5NPWYwTlADB3DEx06xWR=xiinDCeDIDWeDiDGb7DX2K0OD7qiOD7gQDLDWHCDLxYQjtMDDCOD4Oi=DI4GMj4DuDGtP1gNDYktDmMQDY8tDju3DKkUPcqD27rT9DYPc7DDl77FKmhxtdwaFXLrYvjbQynRQ6ST=OZm9GwUuDYojepicWFUg76veto+eI7fUYYpxtYvN77G5BFmt7BGxRODbSoqoDO1t0AklOiD===',
             'ssxmod_itna2': '7qIxnD2i0=qYqxBa3+FD7QGCQHnPDvhx034G9taDfxGXcpPGaecmOkvx8x2r92cDOSjrBbLzqrDbKxeYH=n2QvYZEq7uwYiYpG9FQgrZgteK8/Q3r0HVFZ+bO8ix7jwDFqG7HeD=',
             'zh_choose_undefined': 's'},
 'message': 'success',
 'proxy': '10.17.206.27:808',
 'request_id': '4983300581',
 'server_ip': '10.17.106.68',
 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
               '(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
```

* 示例二: 多线程情况下建议使用get_last=1，共用历史的cookies，当cookie过期时需要获取新的历史cookies时设置get_last=2，避免重复操作浏览器导致响应冲突

```python
# 多个线程共用cookies
from fincookie import get_cookies
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

def thread_func():
    pprint(get_cookies(
        appid="3016993217496905",  # appid
        get_last=1,  # 使用历史cookies
        url="https://www.zjzwfw.gov.cn/zjservice/matter/punishment/searchallpunishlist.do?pageNo=1&areacode=331000",  # 请求百度网址
    ))
    
with ThreadPoolExecutor(max_workers=20) as executor:
    for _ in range(20):
        executor.submit(thread_func)
executor.shutdown()
```
```python
# cookies过期时
from fincookie import get_cookies
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

def thread_func():
    pprint(get_cookies(
        appid="3016993217496905",  # appid
        get_last=2,  # 使用历史cookies
        url="https://www.zjzwfw.gov.cn/zjservice/matter/punishment/searchallpunishlist.do?pageNo=1&areacode=331000",  # 请求百度网址
    ))
    
with ThreadPoolExecutor(max_workers=20) as executor:
    for _ in range(20):
        executor.submit(thread_func)
executor.shutdown()
```

* 示例三: 设置代理 proxy

```python
from fincookie import get_cookies
from pprint import pprint

cookie_data = get_cookies(
    appid="3016993217496905",  # appid
    url="https://www.zjzwfw.gov.cn/zjservice/matter/punishment/searchallpunishlist.do?pageNo=1&areacode=331000",  # 请求百度网址
    proxy='10.17.205.91:808'  # 设置代理  'auto', 'zhima'
)
pprint(cookie_data)
```

* 示例四: 设置等待条件，防止网址加载不完全  wait_for、selector、state

```python
from fincookie import get_cookies
from pprint import pprint

cookie_data = get_cookies(
    appid='3016993217496905',  # appid
    url="https://www.zjzwfw.gov.cn/zjservice/matter/punishment/searchallpunishlist.do?pageNo=1&areacode=331000",  # 请求B站网址
    wait_for="selector",  # 等待id为'xzcf_1'的元素在页面中显示，等待时间为2,000 ms, 'timeout'
    selector="#xzcf_1",
    state="visible",
    wait_timeout=2000,
)
pprint(cookie_data)
```

* 示例五: 等待元素后进行元素操作  action， type_string

```python
from fincookie import get_cookies
from pprint import pprint

cookie_data = get_cookies(
    appid='3016993217496905',  # appid
    url="https://www.zjzwfw.gov.cn/zjservice/matter/punishment/index.do?webId=83&jurisCode=331001",  # 请求百度网址
    wait_for="selector",  # 等待id为'image3'的元素在页面中显示, 并进行点击
    selector="#image3",
    state="visible",
    wait_timeout=2000,
    action='click',
    renew_interval=10000,
)
pprint(cookie_data)
```

* 示例六: 执行JavaScript代码

```python
from fincookie import get_cookies
from pprint import pprint

cookie_data = get_cookies(
    appid='3016993217496905',  # appid
    url="https://www.bilibili.com",  # 请求B站网址
    # 使用js设置cookie
    script="document.cookie = 'username=fincookie; expires=' + new Date(new Date().getTime() + 24 * 60 * 60 * 1000).toUTCString();",
    wait_for='timeout',
    wait_timeout=5000,
    renew_interval=30000,
)
pprint(cookie_data)
```

* 示例七: 使用firefox浏览器  channel

```python
from fincookie import get_cookies
from pprint import pprint

cookie_data = get_cookies(
    appid="3016993217496905",
    url="https://www.baidu.com", 
    channel='firefox' # 使用firefox浏览器
)
pprint(cookie_data)
```

* 示例八: 响应完成后保留浏览器，进行后续操作  renew_interval

```python
from fincookie import get_cookies
from pprint import pprint

get_cookies(
    appid='3016993217496905',  # appid
    url="https://fzgg.gansu.gov.cn/fzgg/c106220/list.shtml",  # 请求列表页
    renew_interval=30000  # 浏览器为该appid保留30,000 ms
)
cookie_data = get_cookies(
    appid='3016993217496905',  # appid
    url="https://fzgg.gansu.gov.cn/fzgg/zcfbjgzdt/202309/173765630.shtml",  # 请求详情页
    renew_interval=30000  # 浏览器为该appid保留30,000 ms
)
pprint(cookie_data)
```


### build_request
使用get_cookies获取cookies之后使用cookies、UA和代理自动请求网址
* **appid:** 程序ID
* **block_timeout:** int, 同appid的多个请求同时操作浏览器时浏览器的阻塞时间(ms)，如果为`0`则不阻塞，若浏览器正在使用直接返回`浏览器繁忙`错误，默认为`0`
* **proxy:** str, 手动传入代理地址，或者使用"zhima"芝麻代理,"auto"根据服务器随机选择代理，默认为None，即使用浏览器默认代理
* **url:** 需要用来获取cookies的URL
* **url_timeout:** int, 用户请求网址的超时时间（ms），如果在该时间内浏览器未完成请求，则请求失败，默认值: 30,000。注:如果网址响应时间过长，可以将该值设置为较大的值，避免网址未响应完全
* **script:**  string, 用户需要在浏览器中执行的JavaScript代码，如果用户需要执行JavaScript代码，可传入该参数
* **wait_for:**  string, 用户需要等待的操作，`timeout`等待一定时间, `selector`等待元素选择器出现响应
* **wait_timeout:** int, `wait_for`等待的时间（ms），结合wait_for参数使用, 默认值: 30,000。
* **selector:** string, wait_for参数值为`selector`时对应的元素CSS选择器或者XPath，用于选择需要等待或获取的元素
* **state:** string, wait_for参数为selector时对应的元素等待状态，`visible`: 等待元素在页面中可见 `hidden`: 等待元素在页面中隐藏 `attached`: 等待选择器附加到 DOM 上  `detached`:等待选择器从 DOM 上分离
* **action:** string, 等待元素之后对元素进行的操作,`click`: 单击，`dblclick`: 双击，`type`: 输入文字或按键
* **type_string:**  string, `action`为`type`时输入的字符
* **renew_interval:** int, appid对应浏览器的保留时间（ms），在保留时间内appid相同的请求会由同一浏览器继续执行后返回，每次请求后刷新, 默认值：3000
* **channel:** str, 浏览器类型，可选['chromium', 'firefox']，默认为chromium
* **request_url:** string 需要请求数据的地址, 可选，如果为空则默认为url
* **headers_str:** string 字符串类型的headers 可选
* **headers_dict:** dict 字典类型的headers 可选
* **success_codes:** list 表示请求正确的状态码列表，默认[200]
* **success_chars:** list 表示请求正确返回的数据中应当包含的字符串列表，默认[""]
* **retry_times:** int 请求最大失败次数，默认3
* **verbose:** bool 是否输出日志，默认False
* **\*\*request_params:** 其他用于请求数据的 requests.get or requests.post 的参数, 如data, timeout, verify等参数
**return:**   
* 获取cookies时响应正确并且request_url请求状态码正确并且内容正确时输出requests.Response，否则输出None

**Examples:**


```python
from fincookie import build_request

url = "https://www.gansu.gov.cn/common/search/5ad7f285c40d4f478a7b43b9fcd67d70?_isAgg=false&_isJson=true&_pageSize=10&_template=index&_rangeTimeGte=&_channelName=&page=1"
response = build_request(
    appid="3016993217496905",
    url=url,
    wait_for='timeout',
    wait_timeout=1000,
    renew_interval=20000,
    request_url=url,  # 如果请求cookie的url和数据api一样，可以省略
    success_codes=[200],
    success_chars=['rows'],
    retry_times=5,
    verbose=True
)
print(response)
print(response.text)
```
**Outputs:**
```
第1次请求：cookies请求成功
第1次请求：请求头构建成功：{'Cookie': 'ZJZWFWSESSIONID=5c...
第1次请求：网址请求失败，状态码不正确（412）
第2次请求：cookies请求成功
第2次请求：请求头构建成功：{'Cookie': '4hP44ZykCTt5O=60YJ.ZOIAjCVS5tUXtVsM9AZJ6...
第2次请求：网址请求成功（200）

<Response [200]>
{"data":{"page":1,"rows":10,"channelId":"5ad7f285c40d4f478
...
```


### build_headers
将请求头字符串、get_cookies返回的cookies和UA信息以及其他请求头内容合并到一个请求头字典中

**Parameters:**

* raw_headers: str, 原始的请求头字符串，request_plugin中的headers
* cookies_return: dict, get_cookies返回的内容
* other: dict, 其他的请求头信息
* \*\*kwargs: 其他的请求头信息  

**Returns:**

* headers: dict, 合并后的请求头字典

**Examples:**

```python
from fincookie import build_headers
from pprint import pprint

raw_headers = """
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cache-Control: no-cache
Connection: keep-alive
"""
cookies_return = {
    'appid': '3016993217496905',
    'request_id': '2413245512',
    'message': 'success',
    'cookies': {
        '__cfduid': 'd2168d779184356788888',
        '__ddg1': '1',
        '__ddg2': '1'
    },
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'proxy': '10.17.205.96:808',
}
other = {'Referer': 'https://www.zjzwfw.gov.cn/zjservice/matter/punishment/index.do?webId=48&jurisCode=330501'}
headers = build_headers(raw_headers, cookies_return, other)
pprint(headers)
```
输出：
```text
{'Accept': '*/*',
 'Accept-Encoding': 'gzip, deflate, br',
 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
 'Cache-Control': 'no-cache',
 'Connection': 'keep-alive',
 'Cookie': '__cfduid=d2168d779184356788888; __ddg1=1; __ddg2=1',
 'Referer': 'https://www.zjzwfw.gov.cn/zjservice/matter/punishment/index.do?webId=48&jurisCode=330501',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
               '(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
```

### get_logs
远程Cookies获取集群日志实时获取  
使用浏览器访问URL: http://10.17.106.68/get_logs)  
进入页面之后可选查看本地或者华为云端的日志

**Examples**

* 实例1:实时获取本地端appid为3016993217496905当天的日志
    http://10.17.106.68/get_logs



### cookie_format
将字符串键值对形式cookies转为Python字典，或将Python字典类型cookies转为字符串键值对形式cookies
**Parameters:**
* cookies (dict or str or None): 
    * str: 字符串键值对形式cookies，返回Python字典类型cookies
    * dict: Python字典类型cookies，返回字符串键值对形式cookies
    * None: 返回空字符串

**Examples:**
```python
from fincookie import cookie_format
# 字典转字符串
print(cookie_format({
    "BAIDUID": "E2AA931DBCBF43DB6FB4FC952AB0FEBE:FG=1",
    "BAIDUID_BFESS": "E2AA931DBCBF43DB6FB4FC952AB0FEBE:FG=1",
    "BA_HECTOR": "0k8k85040184a48h042h00a71incpcl1q"
}))
```
```text
BAIDUID=E2AA931DBCBF43DB6FB4FC952AB0FEBE:FG=1; BAIDUID_BFESS=E2AA931DBCBF43DB6FB4FC952AB0FEBE:FG=1; BA_HECTOR=0k8k85040184a48h042h00a71incpcl1q
```
__________________________________
```python
from fincookie import cookie_format
# 字符串转字典
print(cookie_format("BAIDUID=E2AA931DBCBF43DB6FB4FC952AB0FEBE:FG=1; BAIDUID_BFESS=E2AA931DBCBF43DB6FB4FC952AB0FEBE:FG=1; BA_HECTOR=0k8k85040184a48h042h00a71incpcl1q"))
```
```json
{
  "BAIDUID": "E2AA931DBCBF43DB6FB4FC952AB0FEBE:FG=1",
  "BAIDUID_BFESS": "E2AA931DBCBF43DB6FB4FC952AB0FEBE:FG=1",
  "BA_HECTOR": "0k8k85040184a48h042h00a71incpcl1q"
}
```

### proxy_format
**Examples:**
```python
from fincookie import proxy_format
print(proxy_format("10.17.206.27:808"))
```
```text
{'http': '10.17.206.27:808', 'https': '10.17.206.27:808'}
```


## Contributors:
* **胡永乐  huyl3@finchina.com**