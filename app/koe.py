import sys
import time
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

    def fetch_user(self, _key, _page) -> list:
        ref = []
        is_next_page = False

        res = requests.get(self._url + "/search.php?word=%s&g=1&m=1&p=%s" % (_key, _page))
        bs = BeautifulSoup(res.text, "html.parser")
        a_tags = bs.find_all("a")
        for _a in a_tags:
            _href = _a["href"]
            if _href[:10] == "detail.php":
                ref.append(_a["href"])
            elif _a.string == "Next":
                is_next_page = True

        if is_next_page:
            time.sleep(2)
            self.fetch_user(_key, _page+1)

        return ref

    def fetch_content(self, path: str):
        res = requests.get(self._url + "/%s" % path)
        bs = BeautifulSoup(res.text, "html.parser")
        # TODO: store
        _title = bs.find("h2").text
        _audio = bs.find("audio")
        _src = _audio.find("source")["src"]
        _text = bs.find("div", id="text")
        _user_text, length_date  = _text.find_all("p")[:2]
        length, created_date = length_date.text.split("@")
        _p = _user_text.text.find(":")
        _user = _user_text.text[:_p-1]
        _body_text = _user_text.text[_p+1:]
        print(_title, _user, _body_text, length[:-2], created_date)

if __name__ == "__main__":
    koe = Koe()
    print(koe.fetch_user("a", 1))
