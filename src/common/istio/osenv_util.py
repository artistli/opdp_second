import os


class OsEnvUtil(object):
    def __init__(self):
        pass

    def get_env(self, key, default):
        value = os.environ.get(key)
        if value:
            return value

        if default is not None:
            return default

        return None


os_env_util = OsEnvUtil()
