import copy
import os

from src import exception
from src.client.base import HttpClientBase
from src.common.utils.log.log import OPDP_Logger
from src.common.utils.response_data import UnicornException
from src.settings import global_config

case_pool_param = {
    "autoOwnerId": None,
    "caseNumber": "",
    "creatorId": None,
    "customer": "",
    "isCollect": "",
    "number": "",
    "page": 1,
    "productLineIds": None,
    "productLineName": "",
    "rows": 200,
    "searchName": None,
    "testOwnerId": None,
    "type": None,
    "userId": None
}

add_module_param = {
    # 需要传
    "casePoolId": None,
    "username": None,
    "memo": "",
    # 需要
    "name": None,
    # 需要传
    "parentSuiteId": None
}

full_fields = "name,setup,step,expectResult,memo,subFeature,resGroup,subTestType,priority,testType,requirement,feature,childFeature,product,auto,scriptId,scriptName,scriptStep,scriptCheck,tags,ciAuto,autoScriptTags,ciScriptId,interactive,relationCase,scope"
empty_fields = ""

approve_params = {
    "noList": [],
    "description": "请审批",
    "isAuto": '0',
    "username": None
}


def get_response_list(response, list_key=None):
    """
    :param response: 容器云返回结果
    :param list_key: 待取的列表字段
    :return  返回响应实体的result的list字段
    """
    response_list = response.get("result", [])
    return response_list


def get_response_object(response, object_key="result"):
    """
    :param response: 容器云返回结果
    :param object_key:待取的字段
    :return  返回响应实体的result字段
    """
    response_object = response.get(object_key, {})
    return response_object


class WetestClient(HttpClientBase):

    def __init__(self, user, pwd, request_user, endpoint=global_config.WETEST_ENDPOINT):
        super(WetestClient, self).__init__(endpoint=endpoint)
        self.user = user
        self.pwd = pwd
        self.userId = None
        self.headers = {"Content-Type": "application/json; charset=UTF-8",
                        "Accept": "*/*",
                        "Accept-Encoding": "deflate"}

        self.token = None

        self.get_token()

        self.request_user = request_user

    def get_full_url(self, url):
        return "%s%s" % (global_config.WETEST_PATH_PREFIX, url)

    def get_token(self):
        url = "/testcloud-uac/api/login/token"
        body = {
            "username": self.user,
            "password": self.pwd
        }

        try:
            response = self.http_obj.request("POST", url, body=body)
        except Exception as e:
            OPDP_Logger.error("连接wetest获取token失败，异常信息:%s" % str(e))
            raise UnicornException(err_msg="无法连接wetest地址:%s" % self.endpoint)
        OPDP_Logger.debug("登录信息:%s" % response)
        self.response_checker(response, extra_message="获取Wetest Token错误")
        token = response["result"]
        token_final = {"Authorization": token}
        self.update_headers(token_final)
        return token

    def response_checker(self, response, extra_message=""):
        if "success" in response:
            success = response["success"]
            message = response["errMsg"]
        else:
            success = response["code"] == 200
            message = response["message"]

        if not success:
            raise exception.WetestError("和wetest交互发生错误, 错误信息:%s --> %s" % (extra_message, message))

    def get_headers(self):
        pass

    def update_headers(self, headers):
        self.headers.update(headers)

    def auth_request(self):
        # url = "/testcloud-uac/api/login/token"
        if (not self.token or not self.userId):
            token = self.get_token()
        else:
            token = self.token

        token_final = {"Authorization": token}
        self.update_headers(token_final)
        return token_final

    def auth_user_id(self):
        url = self.get_full_url("/testcloud-uac/uac/user/loginId/%s" % self.user)
        response = self.http_obj.request("GET", url, headers=self.headers)
        self.response_checker(response, extra_message="获取用户id失败")
        self.userId = response['result']['id']
        return self.userId

    def test_case_pool_list(self):
        url = self.get_full_url("/v1/casePool/info?username=%s" % self.request_user)
        case_pool_param_final = copy.deepcopy(case_pool_param)
        case_pool_param_final['userId'] = self.userId
        response = self.get(url, headers=self.headers)
        self.response_checker(response, extra_message="获取用例池信息失败")
        case_pool_list = response['result']
        OPDP_Logger.debug("用例池信息:%s" % case_pool_list)
        return case_pool_list

    def suite_tree(self, case_pool_id):
        OPDP_Logger.debug("获取用例池的树结构:%s" % case_pool_id)
        url = self.get_full_url("/v1/suiteTree/%s?username=%s" % (case_pool_id, self.request_user))
        response = self.get(url, headers=self.headers)
        self.response_checker(response)
        suite_tree_list = get_response_list(response)
        OPDP_Logger.debug("用例池结构为:%s" % suite_tree_list)
        return suite_tree_list

    def add_module(self, casepool_id, parent_model_id, model):
        OPDP_Logger.debug("为用例池:%s的模块:%s添加子模块:%s" % (casepool_id, parent_model_id, model))
        url = self.get_full_url("/v1/testSuite")
        params = copy.deepcopy(add_module_param)
        params['username'] = self.request_user
        params['casePoolId'] = casepool_id
        params['parentSuiteId'] = parent_model_id
        params['name'] = model
        params['memo'] = 'opdp自动添加'
        response = self.post(url, body=params, headers=self.headers)
        self.response_checker(response)
        return params

    def make_upload_post_data(self, file_path):
        return []

    def upload_case(self, case_pool_id, model_id, case_file):
        url = self.get_full_url(
            "/v1/testCase?suiteId=%s&username=%s&fields=%s" % (model_id, self.request_user, full_fields))
        post_content_file = self.make_upload_post_data(case_file)

        self_headers = copy.deepcopy(self.headers)
        boundary = "----WebKitFormBoundarym1YKP59YgikABK1f"
        self_headers['Content-Type'] = "multipart/form-data;boundary=%s" % boundary

        files = {"file": (
            os.path.basename(case_file), open(case_file, "rb"),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", {})}

        with open(case_file, "rb") as fp:
            file_data = fp.read()

        OPDP_Logger.debug("data：%s" % file_data)
        params = {
            "file": (
                os.path.basename(case_file), file_data,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        }

        response = self.post(url, headers=self_headers, fields=params, multipart_boundary=boundary)
        OPDP_Logger.debug("response:%s " % response)
        self.response_checker(response)
        return get_response_list(response)

    def create_approve(self, case_ids):
        OPDP_Logger.debug("用例:%s创建审批" % case_ids)
        url = self.get_full_url("/v1/testCase")
        params = copy.deepcopy(approve_params)
        params['noList'] = case_ids
        params['username'] = self.request_user
        params['isAuto'] = '0'
        params['description'] = '用户[%s]在opdp自动上传的用例，请审批,谢谢' % self.request_user

        response = self.put(url, body=params, headers=self.headers)
        OPDP_Logger.debug(" 审批用例结果：%s" % response)
        self.response_checker(response)
        return {}

    def upload_case_list(self, case_pool_id, model_id, case_list):
        OPDP_Logger.debug("给用例池：%s的模块：%s上传测试用例:%s" % (case_pool_id, model_id, case_list))
        return {}

    def delete_case(self, case_list):
        url = self.get_full_url("/v1/testCase")
        body = {
            "noList": case_list,
            "username": self.request_user
        }

        OPDP_Logger.debug("删除用例参数:%s" % body)
        response = self.delete(url=url, headers=self.headers, body=body)

        self.response_checker(response, "删除用例接口调用失败")
        OPDP_Logger.debug("删除用例结果为:%s" % response)
        return response
