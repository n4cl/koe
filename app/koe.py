import sys
import time
import datetime
import sqlite3
import configparser
from logging import getLogger, StreamHandler, DEBUG
import requests
from bs4 import BeautifulSoup

class Koe:
    def __init__(self):
        self._init_file = "koe.ini"
        self._config = self._read_init_file(self._init_file)
        self._url = self._config["URL"]
        self.logger = self._setup_logger()
        self.storage_path = "/usr/local/storage/"
        self.connect = sqlite3.connect(self.storage_path + 'koe.db', isolation_level=None)

    def _setup_logger(self):
        logger = getLogger(__name__)
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        logger.setLevel(DEBUG)
        logger.addHandler(handler)
        logger.propagate = False
        return logger

    def _read_init_file(self, _file_name):
        config = configparser.ConfigParser()
        config.read(_file_name)
        return config["DEFAULT"]

    def fetch_user(self, _key: str, _page: int = 0, _limit_page: int = 10) -> list:

        ref = set()
        is_next_page = False

        res = requests.get(self._url + "/search.php?word=%s&g=1&m=1&p=%s" % (_key, _page))
        bs = BeautifulSoup(res.text, "html.parser")
        a_tags = bs.find_all("a")
        for _a in a_tags:
            _href = _a["href"]
            if _href[:10] == "detail.php":
                ref.add(_a["href"])
            elif _a.string == "Next":
                is_next_page = True

        for _path in ref:
            self.fetch_content(_path)

        if _page >= _limit_page:
            self.logger.info("Suspended because _limit_page has been reached")
            return

        if is_next_page:
            time.sleep(2)
            self.fetch_user(_key, _page+1)

        return

    def fetch_content(self, path: str):
        res = requests.get(self._url + "/%s" % path)
        bs = BeautifulSoup(res.text, "html.parser")
        _id = path.split("=")[-1]
        _title = bs.find("h2").text
        _audio = bs.find("audio")
        _src = _audio.find("source")["src"]
        _text = bs.find("div", id="text")
        _user_text, length_date  = _text.find_all("p")[:2]
        length, created_date = length_date.text.split("@")
        _p = _user_text.text.find(":")
        _user = _user_text.text[:_p-1]
        _body_text = _user_text.text[_p+1:]
        clap = bs.find("div", id="clap-inner")
        _views = clap.text.split(":")[-1][1:-1]
        _file_path = ""

        autio_data = requests.get("https:" + _src)
        _file_path = self.storage_path + _src.split("/")[-1]
        with open(_file_path, "wb") as save_file:
            save_file.write(autio_data.content)

        self.insert_content(_id, _user, _title, _body_text, _file_path, length[:-2], _views, 0, created_date)

    def insert_content(self, _id, _user, _title, _body, _file, _play_time, _view, _fav, created_date):
        try:
            self.connect.execute("BEGIN")
            self.connect.execute("INSERT INTO content VALUES (:id,:user,:title,:body,:file,:play_time,:fav,:view,:created_date,:updated_date)",
                                                             (_id, _user, _title, _body, _file, _play_time, _view, _fav, created_date, datetime.datetime.now()))
            self.connect.execute("COMMIT")
        except Exception as e:
            self.connect.execute("ROLLBACK")
            raise e


if __name__ == "__main__":
    koe = Koe()
    print(koe.fetch_user("a", 1))
