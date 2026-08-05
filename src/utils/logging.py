from src import *


class loggercls:
    def __init__(self):
        self.guihandler = None


    def push(self, level, source, msg):
        print(f'[{level}] ({source}) {msg}')

        if self.guihandler:
            try:
                self.guihandler(level, source, msg)

            except Exception:
                pass


    def success(self, msg, source='app'):
        self.push('OK', source, msg)


    def error(self, msg, source='app'):
        self.push('ERR', source, msg)


    def warning(self, msg, source='app'):
        self.push('WARN', source, msg)


    def info(self, msg, source='app'):
        self.push('INFO', source, msg)


    def ratelimit(self, msg, source='app'):
        self.push('RL', source, msg)


    def captcha(self, msg, source='app'):
        self.push('CAPTCHA', source, msg)


    def debug(self, msg, source='app'):
        self.push('DBG', source, msg)


logger = loggercls()
