class CodeMessageException(Exception):
    def __init__(self, code, message, info=None):
        self.code = code
        self.message = message
        self.info = info

    def __str__(self):
        return repr(self.message)
