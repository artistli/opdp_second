HTTP_500_INTERNAL_SERVER_ERROR = 500
HTTP_400_BAD_REQUEST = 400


class Error(Exception):
    http_code = None
    message_format = ""

    def __init__(self, message=None, **kwargs):
        try:
            message = self._build_message(message, **kwargs)
        except KeyError:
            message = self.message_format

        super(Error, self).__init__(message)

    def _build_message(self, message, **kwargs):

        if message:
            return message
        return self.message_format % kwargs


class UnexceptedError(Error):
    http_code = HTTP_500_INTERNAL_SERVER_ERROR
    message_format = "An unexcepted error happened in your request, error:%(exception)s"
    def _build_message(self, message, **kwargs):
        kwargs.setdefault("exception", "")
        return super(UnexceptedError, self)._build_message(message, **kwargs)


class WetestError(Error):
    http_code = HTTP_400_BAD_REQUEST
    message_format = ""
