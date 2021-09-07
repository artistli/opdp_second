import copy

from src.common.istio.osenv_util import os_env_util
from src.client.base import HttpClientBase
from src.common.utils.response_data import class_to_dict


def get_first_python_api_hostname():
    return os_env_util.get_env("first_python_api_host", "localhost")


def get_first_python_api_port():
    return os_env_util.get_env("first_python_api_port", 9908)


def get_first_python_api_service_domain():
    return os_env_util.get_env("first_python_api_service_domain", "")


def get_first_python_api():
    return {
        "name": "http://{0}{1}:{2}".format(get_first_python_api_hostname(), get_first_python_api_service_domain(),
                                           get_first_python_api_port()),
        "endpoint": "api/v1/opdp_fastapi_first",
        "children": []
    }


class firstPythonClient(HttpClientBase):

    def __init__(self, endpoint=get_first_python_api().get("name")):
        super(firstPythonClient, self).__init__(endpoint=endpoint)
        self.headers = {"Content-Type": "application/json; charset=UTF-8",
                        "Accept": "*/*",
                        "Accept-Encoding": "deflate"}

    def get_full_url(self, url):
        return "%s/%s%s" % (self.endpoint, get_first_python_api().get("endpoint"), url)

    def add(self, param):
        url = "/call_python/add"
        final_param = copy.deepcopy(class_to_dict(param))
        print(final_param, "type", type(param))
        result = self.post(self.get_full_url(url), body=final_param, headers=self.headers)
        print("add result:", result)
        return result

    def delete_by_id(self, id):
        url = "/call_python/delete/%s" % id
        result = self.delete(self.get_full_url(url), headers=self.headers)
        print("delete result:", result)
        return result

    def get_by_id(self, id):
        url = "/call_python/%s" % id
        result = self.get(self.get_full_url(url))
        print(result)
        return result


first_python_client = firstPythonClient()
