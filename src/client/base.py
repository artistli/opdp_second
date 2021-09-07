import json
from urllib.parse import urljoin

import urllib3


class HttpObject(urllib3.poolmanager.PoolManager):
    _encode_url_methods = {'DELETE', 'GET', 'HEAD', 'OPTIONS'}

    def __init__(self, endpoint="", **kwargs):
        super(HttpObject, self).__init__(**kwargs)
        self.endpoint = endpoint

    def request(self, method, url, body=None, headers=None, fields=None, auth_token=None, **kwargs):
        _headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        request_kw = {}

        if headers is None:
            headers = _headers

        if body is not None:
            body = json.dumps(body)
            request_kw["body"] = body

        if fields is not None:
            if method not in self._encode_url_methods and "body" in request_kw:
                raise Exception("post and put request got values for both 'fields' and 'body', can only specify one.")
            request_kw["fields"] = fields

        if auth_token is not None:
            headers.update(auth_token)

        req_url = urljoin(self.endpoint, url)
        res = super(HttpObject, self).request(method, req_url, headers=headers, **request_kw, **kwargs)

        try:
            return json.loads(res.data)
        except json.decoder.JSONDecodeError:
            raise Exception("http response json decode error, error response:%s" % res.data)


class HttpClientBase:

    def __init__(self, endpoint="", **kwargs):
        self.endpoint = endpoint
        self.http_obj = HttpObject(endpoint=self.endpoint, **kwargs)

    def auth_request(self):
        """认证请求. 用以描述token获取的过程, 子类client获取的方式可能不一样需要各自进行重写, 然后通过字典的形式组装返回.
        :return: dict {"token_key": "token_value"}
        """
        return {}

    def response_checker(self, response, extra_message=""):
        """响应体检查. 子类client的请求响应体可能不一样所以需要各自进行重写, 后续可以通过参数进行扩展比如返回体schema校验."""
        pass

    def request(self, method, url, body=None, headers=None, fields=None, **kwargs):
        # 如果有token, 将token更新到request headers
        auth_token = self.auth_request()
        response = self.http_obj.request(method, url, headers=headers, body=body, fields=fields,
                                         auth_token=auth_token, **kwargs)

        return response

    def post(self, url, headers=None, body=None, fields=None, **kwargs):
        return self.request('POST', url, headers=headers, body=body, fields=fields, **kwargs)

    def get(self, url, headers=None, body=None, fields=None, **kwargs):
        return self.request('GET', url, headers=headers, body=body, fields=fields, **kwargs)

    def delete(self, url, headers=None, body=None, fields=None, **kwargs):
        return self.request('DELETE', url, headers=headers, body=body, fields=fields, **kwargs)

    def put(self, url, headers=None, body=None, fields=None, **kwargs):
        return self.request('PUT', url, headers=headers, body=body, fields=fields, **kwargs)


def request():
    import requests

    requests.Session.post()
