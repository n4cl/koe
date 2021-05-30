import sys
import configparser
import requests

class Koe:
    def __init__(self):
        self._init_file = "koe.ini"
        self._config = self._read_init_file(self._init_file)
        self._url = self._config["URL"]

    def _read_init_file(self, _file_name):
        config = configparser.ConfigParser()
        config.read(_file_name)
        return config["DEFAULT"]

    def fetch_user(self):
        print(self.get_function_name())

    def get_function_name(self):
        return sys._getframe().f_code.co_name

if __name__ == "__main__":
    koe = Koe()
    koe.fetch_user()
