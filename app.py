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

# Crawling Data
ip_adjunct_data = ip.get_adjunct()
ip_prof_data = ip.get_prof()

sp_adjunct_data = sp.get_adjunct()
sp_prof_data = sp.get_prof()
sp_honor_data = sp.get_honor()


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
    soft_prof_list = sp_prof_data[0]
    soft_honor_list = sp_honor_data[0]
    soft_adjunct_list = sp_adjunct_data[0]

    ict_adjunct_list = ip_adjunct_data[0]
    ict_prof_list = ip_prof_data[0]

    return render_template("index.html",
                           soft_prof_list=soft_prof_list,
                           soft_honor_list=soft_honor_list,
                           soft_adjunct_list=soft_adjunct_list,
                           ict_adjunct_list=ict_adjunct_list,
                           ict_prof_list=ict_prof_list)


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
