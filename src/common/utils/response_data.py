import json
from fastapi.responses import JSONResponse
from fastapi import Request

def class_to_dict(obj):
    """把对象(支持单个对象、list、set)转换成字典"""
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__
    if is_list or is_set:
        obj_arr = []
        for o in obj:
            # 把Object对象转换成Dict对象
            if '_sa_instance_state' in o.__dict__:
                o.__dict__.pop('_sa_instance_state')
            dict = {}
            dict.update(o.__dict__)
            obj_arr.append(dict)
        return obj_arr
    else:
        if '_sa_instance_state' in obj.__dict__:
            obj.__dict__.pop('_sa_instance_state')
        dict = {}
        dict.update(obj.__dict__)
        return dict


class UnicornException(Exception):
    def __init__(self, result=False, code=500, data=None, err_msg='服务器内部错误', total=0):
        if data is None:
            data = {}
        self.result = result
        self.code = code
        self.data = data
        self.message = err_msg
        self.total = total

    def __str__(self):
        str_msg = {each_key: each_value for (each_key, each_value) in self.__dict__.items()}
        return str_msg


class ResponseDataModel(UnicornException):
    def __init__(self, result=False, code=200, data=None, err_msg='', total=0):
        if data and not isinstance(data, (dict, list)):
            data = class_to_dict(data)
        super(ResponseDataModel, self).__init__(result, code, data, err_msg, total)


class ResponseData(object):
    @staticmethod
    def get_response_data(response_data):
        try:
            response_data_object = json.loads(response_data)
            return response_data_object
        except Exception as e:
            return {}

    @staticmethod
    def get_successful_response(data=None, total=0):
        return ResponseDataModel(result=True, data=data, total=total)

    @staticmethod
    def get_error_response(code=500, err_msg='服务器内部错误'):
        return ResponseDataModel(code=code, data={}, err_msg=err_msg)


def register_exception(app):
    @app.exception_handler(UnicornException)
    def unicorn_exception_handler(request: Request, exc: UnicornException):
        return JSONResponse(status_code=200, content={"code": exc.code, "message": exc.message,
                                                      "result": exc.result, "data": exc.data, "total": exc.total})
