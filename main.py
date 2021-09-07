# -*- coding:UTF-8 -*-
"""
@see: 入口
@author: 孙留平
"""

import uvicorn

from src import init_app


app, Config = init_app('dev')


def main():
    uvicorn.run(app="main:app", host=Config.FASTAPI_HOST, port=Config.FASTAPI_PORT, log_level=Config.LOG_LEVEL.lower(), reload=True, debug=True)


if __name__ == "__main__":
    main()
