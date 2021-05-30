import sys
import configparser
import requests
from bs4 import BeautifulSoup

class Koe:
    def __init__(self):
        self._init_file = "koe.ini"
        self._config = self._read_init_file(self._init_file)
        self._url = self._config["URL"]

    def _read_init_file(self, _file_name):
        config = configparser.ConfigParser()
        config.read(_file_name)
        return config["DEFAULT"]

    def fetch_user(self, _key) -> list:
        ref = []
        if not _key:
            return ref

        res = requests.get(self._url + "/search.php?word=%s&g=1&m=1" % _key)
        bs = BeautifulSoup(res.text, "html.parser")
        a_tags = bs.find_all("a")
        for _a in a_tags:
            _href = _a["href"]
            if _href[:10] == "detail.php":
                ref.append(_a["href"])
        return ref


if __name__ == "__main__":
    koe = Koe()
    print(koe.fetch_user("a"))
