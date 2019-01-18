# -*- coding: utf-8 -*-

"""
 Created by IntelliJ IDEA.
 Project: Jaram-Professor-Crawler
 ===========================================
 User: ByeongGil Jung
 Date: 2019-01-17
 Time: 오후 4:08
"""

import config
from crawler.ict import ict_professor as ip
from crawler.soft import soft_professor as sp

from flask import Flask, render_template

app = Flask(__name__)


def find_in_dict(dict_, find_value, f="key"):
    if f == "key":
        for key, value in dict_.items():
            if find_value == value:
                return key
    elif f == "value":
        for key, value in dict_.items():
            if find_value == key:
                return value

    return "No Value"


@app.route("/")
def root():
    prof_list = ["김나연", "박창선", "정병길", "정회성"]
    honor_list = ["a", "b", "c", "d"]

    # sp.get_adjunct()
    # sp.get_prof()
    # sp.get_honor()
    #
    # ip.get_prof()
    # ip.get_adjunct()
    return render_template("index.html", prof_list=prof_list, honor_list=honor_list)


@app.route("/software_professor/<name>")
def render_software_professor_controller(name):
    name_dict = config.SOFTWARE_PROFESSOR_NAME
    key_name = find_in_dict(name_dict, name, f="key")

    # Crawler .py
    ko_name = ["ㄱㄴㄷ", "ㅂㅈㄷ", "ㅋㅌㅊㅍ"]
    en_name = ["abc", "wer", "dge"]
    status = ["교수", "명예교수", "조교수"]
    email = ["이메일1", "이메일2", "이메일3"]

    posts = [{"ko_name": ko_name, "en_name": en_name, "status": status, "email": email}]

    return render_template("professor_info.html", posts=posts)


@app.route("/ict_professor/<name>")
def render_ict_professor_controller(name):
    name_dict = config.SOFTWARE_PROFESSOR_NAME
    key_name = find_in_dict(name_dict, name, f="key")
    template = render_template("professor_info.html")

    # Crawler .py
    ko_name = None
    en_name = None
    status = None
    email = None

    return key_name


if __name__ == "__main__":
    app.run(debug=True, port=9999)
