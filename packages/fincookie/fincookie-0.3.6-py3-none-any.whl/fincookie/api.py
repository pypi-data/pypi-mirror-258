import requests
import socket
from typing import *

hwy_hwy_api = f"http://10.55.3.250/cookieService/"
hwy_local_api = "http://hive.finchina.local/api/hwy/cookieService/"
local_local_api = "http://10.17.106.68/"
dev_api = "http://10.17.214.105/"
gao_api = "http://10.10.13.43/"

IP = socket.gethostbyname(socket.gethostname())
if IP.startswith('10.55'):
    server_api = hwy_local_api
elif IP.startswith('10.10'):
    server_api = gao_api
elif IP == '10.17.214.105':
    server_api = dev_api
elif IP.startswith('10.17'):  # '10.17'
    server_api = local_local_api
else:
    raise ValueError(f'IP地址{IP}不在预设范围内')

MODE = 'USER'


def set_dev(dev: bool = True):
    global MODE
    if dev is True:
        MODE = 'DEVELOPER'
    else:
        MODE = "USER"


def get_cookies(appid: str,
                get_last: int = 0,
                block_timeout: int = 0,
                proxy: str = None,
                url: str = None,
                url_timeout: int = None,
                script: str = None,
                wait_for: str = None,
                wait_timeout: int = None,
                selector: str = None,
                state: str = None,
                action: str = None,
                type_string: str = None,
                renew_interval: int = None,
                channel: str = None,
                ) -> dict:
    """
    :param appid: 程序ID
    :param get_last: int, 若为`0`通过操作浏览器获取结果，若为`1` 不进行浏览器操作，直接返回appid的上次cookies结果，如果没有则重新获取(其他并发的get_last为1或者2的线程等待)，若为`2`清除并重新获取历史结果，其他get_last为1或者2的线程等待结果获取完成之后直接使用，避免多线程重复操作浏览器。默认为`0`。
    :param block_timeout: int, 同appid的多个请求同时操作浏览器时浏览器的阻塞时间(ms)，如果为`0`则不阻塞，若浏览器正在使用直接返回`浏览器繁忙`错误，默认为`0`
    :param proxy: str, 手动传入代理地址，或者使用"zhima"芝麻代理,"auto"根据服务器随机选择代理，默认为None，即使用浏览器默认代理
    :param url: 需要用来获取cookies的URL
    :param url_timeout: int, 用户请求网址的超时时间（ms），如果在该时间内浏览器未完成请求，则请求失败，默认值: 30,000。注:如果网址响应时间过长，可以将该值设置为较大的值，避免网址未响应完全
    :param script:  string, 用户需要在浏览器中执行的JavaScript代码，如果用户需要执行JavaScript代码，可传入该参数
    :param wait_for:  string, 用户需要等待的操作，`timeout`等待一定时间, `selector`等待元素选择器出现响应
    :param wait_timeout: int, `wait_for`等待的时间（ms），结合wait_for参数使用, 默认值: 30,000。
    :param selector: string, wait_for参数值为`selector`时对应的元素CSS选择器或者XPath，用于选择需要等待或获取的元素
    :param state: string, wait_for参数为selector时对应的元素等待状态，`visible`: 等待元素在页面中可见 `hidden`: 等待元素在页面中隐藏;`attached`: 等待选择器附加到 DOM 上;`detached`: 等待选择器从 DOM 上分离
    :param action: string, 等待元素之后对元素进行的操作,`click`: 单击，`dblclick`: 双击，`type`: 输入文字或按键
    :param type_string:  string, `action`为`type`时输入的字符
    :param renew_interval: int, appid对应浏览器的保留时间（ms），在保留时间内appid相同的请求会由同一浏览器继续执行后返回，每次请求后刷新, 默认值：3000
    :param channel: str, 浏览器类型，可选['chromium', 'firefox']，默认为chromium
    :return Dict 包含cookies，user-agent，proxy的字典
    """
    data = {k: v for k, v in locals().items() if isinstance(v, (int, str))}
    api = dev_api if MODE == 'DEVELOPER' else server_api
    json_data = requests.post(api, data=data).json()
    return json_data


def get_loads() -> Dict:
    loads = {}
    if MODE == 'DEVELOPER':
        apis = [dev_api]
    else:
        apis = [server_api]
    for api in apis:
        api += "get_loads"
        loads.update(requests.get(api, timeout=2).json())
    return loads


def cookie_format(cookies: dict or str) -> Union[str, Dict]:
    if cookies is None:
        return ''
    if isinstance(cookies, dict):
        return "; ".join([f"{key}={value}" for key, value in cookies.items()])
    else:
        return dict([(item.split("=", 1)[0].strip(), item.split("=", 1)[1].strip()) for item in cookies.split(";")])


# 重构请求头
def build_headers(raw_headers: str = "", cookies_return: Dict = None, other: Dict = None, **kwargs) -> Dict:
    """
    将get_cookies请求到的cookie信息放到headers字典中
    :param raw_headers: 原始headers字符串
    :param cookies_return: get_cookies函数返回值
    :param other: 其他请求头参数
    :return: 请求头
    """
    if cookies_return is None:
        cookies_return = {}
    raw_kv = [item.strip().split(": ", 1) for item in raw_headers.strip().split("\n") if ": " in item]
    headers = dict(raw_kv) if raw_kv else {}
    if cookies_return.get('cookies'):
        headers['Cookie'] = cookie_format(cookies_return.get('cookies'))
    if cookies_return.get('user-agent'):
        headers['User-Agent'] = cookies_return.get('user-agent')
    if other:
        headers.update(other)
    headers.update(kwargs)
    return headers


def proxy_format(proxy: str) -> Dict:
    return {"http": proxy, "https": proxy}


def build_request(
        appid: str,
        block_timeout: int = 0,
        proxy: str = None,
        url: str = None,
        url_timeout: int = None,
        script: str = None,
        wait_for: str = None,
        wait_timeout: int = None,
        selector: str = None,
        state: str = None,
        action: str = None,
        type_string: str = None,
        renew_interval: int = None,
        channel: str = None,
        request_url: str = None,
        headers_str: str = None,
        headers_dict: Dict = None,
        success_codes: List = None,
        success_chars: List = None,
        retry_times: int = 3,
        verbose: bool = False,
        logger=None,
        **request_params
) -> requests.Response:
    """
    使用get_cookies获取cookies之后使用cookies、UA和代理自动请求网址
    :param appid: 程序ID
    :param block_timeout: int, 同appid的多个请求同时操作浏览器时浏览器的阻塞时间(ms)，如果为`0`则不阻塞，若浏览器正在使用直接返回`浏览器繁忙`错误，默认为`0`
    :param proxy: str, 手动传入代理地址，或者使用"zhima"芝麻代理,"auto"根据服务器随机选择代理，默认为None，即使用浏览器默认代理
    :param url: 需要用来获取cookies的URL
    :param url_timeout: int, 用户请求网址的超时时间（ms），如果在该时间内浏览器未完成请求，则请求失败，默认值: 30,000。注:如果网址响应时间过长，可以将该值设置为较大的值，避免网址未响应完全
    :param script:  string, 用户需要在浏览器中执行的JavaScript代码，如果用户需要执行JavaScript代码，可传入该参数
    :param wait_for:  string, 用户需要等待的操作，`timeout`等待一定时间, `selector`等待元素选择器出现响应
    :param wait_timeout: int, `wait_for`等待的时间（ms），结合wait_for参数使用, 默认值: 30,000。
    :param selector: string, wait_for参数值为`selector`时对应的元素CSS选择器或者XPath，用于选择需要等待或获取的元素
    :param state: string, wait_for参数为selector时对应的元素等待状态，`visible`: 等待元素在页面中可见 `hidden`: 等待元素在页面中隐藏 `attached`: 等待选择器附加到 DOM 上  `detached`:等待选择器从 DOM 上分离
    :param action: string, 等待元素之后对元素进行的操作,`click`: 单击，`dblclick`: 双击，`type`: 输入文字或按键
    :param type_string:  string, `action`为`type`时输入的字符
    :param renew_interval: int, appid对应浏览器的保留时间（ms），在保留时间内appid相同的请求会由同一浏览器继续执行后返回，每次请求后刷新, 默认值：3000
    :param channel: str, 浏览器类型，可选['chromium', 'firefox']，默认为chromium
    :param request_url: 需要请求数据的地址,如果为空则默认为url
    :param headers_str: 字符串类型的headers
    :param headers_dict: 字典类型的headers
    :param success_codes: 表示请求正确的状态码列表，默认[200]
    :param success_chars: 表示请求正确返回的数据中包含的字符串，默认['']
    :param retry_times: 最大失败次数，默认3
    :param verbose: 是否输出日志，默认False
    :param logger: 请求日志输出对象，需要有.info, .warning, .error方法，默认None通过print打印
    :param request_params: 其他用于请求数据的 requests.get or requests.post 的参数, 如data, timeout, verify等参数
    :return: 获取cookies时响应正确时输出requests.Response，否则输出None
    """

    def print_log(msg, level='info'):
        if verbose or logger is not None:
            if logger is None:
                print(msg)
            else:
                getattr(logger, level)(msg)
        else:
            ...

    if headers_str is None:
        headers_str = ""
    if success_chars is None:
        success_chars = ['']
    if success_codes is None:
        success_codes = [200]
    if request_url is None and url is not None:
        request_url = url
    cookie_failed = 0
    request_failed = 0
    response = None
    while cookie_failed + request_failed < retry_times:
        cookies_json = get_cookies(
            appid=appid,
            get_last=1 if cookie_failed == 0 and request_failed == 0 else 2,
            block_timeout=block_timeout,
            proxy=proxy,
            url=url,
            url_timeout=url_timeout,
            script=script,
            wait_for=wait_for,
            wait_timeout=wait_timeout,
            selector=selector,
            state=state,
            action=action,
            type_string=type_string,
            renew_interval=renew_interval,
            channel=channel,
        )
        if cookies_json['message'] != 'success':
            print_log(f"第{cookie_failed + request_failed + 1}次请求：cookies请求失败（{cookies_json['message']}）", level='error')
            cookie_failed += 1
        else:
            print_log(f"第{cookie_failed + request_failed + 1}次请求：cookies请求成功")
            headers = build_headers(raw_headers=headers_str, cookies_return=cookies_json, other=headers_dict)
            print_log(f"第{cookie_failed + request_failed + 1}次请求：请求头构建成功：{headers}")
            if 'data' in request_params:
                response = requests.post(request_url, headers=headers, proxies=proxy_format(cookies_json['proxy']), **request_params)
            else:
                response = requests.get(request_url, headers=headers, proxies=proxy_format(cookies_json['proxy']), **request_params)
            response.encoding = response.apparent_encoding
            if response.status_code not in success_codes:
                print_log(f'第{cookie_failed + request_failed + 1}次请求：网址请求失败，状态码不正确（{response.status_code}）', level='error')
                request_failed += 1
                response = None
            else:
                for char in success_chars:
                    if char not in response.text:
                        print_log(f'第{cookie_failed + request_failed + 1}次请求：网址请求失败，响应内容不正确（"{char}" not in response.text）', level='error')
                        request_failed += 1
                        response = None
                        break
                else:
                    print_log(f'第{cookie_failed + request_failed + 1}次请求：网址请求成功（{response.status_code}）')
                    response.__setattr__('cookies_return', cookies_json)
                    response.__setattr__('headers', headers)
                    break
    return response


def get_dynamic_proxy():
    ip = socket.gethostbyname(socket.gethostname())
    api = hwy_hwy_api if ip[:5] == '10.55' else hwy_local_api
    proxy_res = requests.get(api + 'get_dynamic_proxy')
    return proxy_res.json()


def set_dynamic_proxy(proxy, timeout=300):
    ip = socket.gethostbyname(socket.gethostname())
    api = hwy_hwy_api if ip[:5] == '10.55' else hwy_local_api
    proxy_res = requests.get(api + 'set_dynamic_proxy', params={'proxy': proxy, 'timeout': timeout})
    return proxy_res.json()


if __name__ == '__main__':
    # set_dev()
    cookies_url = 'http://www.lanzhou.gov.cn/col/col15334/index.html'
    res = build_request(
        appid=f"test-sitename",
        url='https://www.baidu.com',
        proxy='10.17.206.27:808',
        wait_for='timeout',
        wait_timeout=3000,
        url_timeout=60000,
        block_timeout=300000,
        renew_interval=300000,
        channel='firefox',
        request_url='https://www.baidu.com',
        verbose=True
    )
    print(res)
    print(res.status_code)
    print(res.text)
