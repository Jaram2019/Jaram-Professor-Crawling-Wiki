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

# Params
# position = config.POSITION

# Crawling Data
sp_adjunct_data = sp.get_adjunct()
sp_prof_data = sp.get_prof()
sp_honor_data = sp.get_honor()

ip_adjunct_data = ip.get_adjunct()
ip_prof_data = ip.get_prof()


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
    # name_dict = config.SOFTWARE_PROFESSOR_NAME
    # key_name = find_in_dict(name_dict, name, f="key")

    # Params
    ko_name = "Ko Name"
    en_name = "En Name"
    status = "Status"
    location = "Location"
    email = "Email"

    # Find the position
    prof_list = None
    if name in sp_adjunct_data[0]:
        prof_list = sp_adjunct_data
    elif name in sp_prof_data[0]:
        prof_list = sp_prof_data
    elif name in sp_honor_data[0]:
        prof_list = sp_honor_data

    # Count the number
    prof_count = 0
    for i in range(len(prof_list[0])):
        if name == prof_list[0][i]:
            prof_count = i

    # Put data to variable
    for i in range(len(prof_list)):
        if i == 0:
            ko_name = prof_list[i][prof_count]
        elif i == 1:
            en_name = prof_list[i][prof_count]
        elif i == 2:
            status = prof_list[i][prof_count]
        elif i == 3:
            location = prof_list[i][prof_count]
        elif i == 4:
            email = prof_list[i][prof_count]

    prof_data = {"ko_name": ko_name,
                 "en_name": en_name,
                 "status": status,
                 "location": location,
                 "email": email}

    return render_template("professor_info.html", prof_data=prof_data)


@app.route("/ict_professor/<name>")
def render_ict_professor_controller(name):
    # name_dict = config.SOFTWARE_PROFESSOR_NAME
    # key_name = find_in_dict(name_dict, name, f="key")

    # Params
    ko_name = "Ko Name"
    en_name = "En Name"
    status = "Status"
    location = "Location"
    phone = "Phone"
    email = "Email"

    # Find the position
    prof_list = None
    if name in ip_adjunct_data[0]:
        prof_list = ip_adjunct_data
    elif name in ip_prof_data[0]:
        prof_list = ip_prof_data

    # Count the number
    prof_count = 0
    for i in range(len(prof_list[0])):
        if name == prof_list[0][i]:
            prof_count = i

    # Put data to variable
    for i in range(len(prof_list)):
        if i == 0:
            ko_name = prof_list[i][prof_count]
        elif i == 1:
            en_name = prof_list[i][prof_count]
        elif i == 2:
            status = prof_list[i][prof_count]
        elif i == 3:
            location = prof_list[i][prof_count]
        elif i == 4:
            phone = prof_list[i][prof_count]
        elif i == 5:
            email = prof_list[i][prof_count]

    prof_data = {"ko_name": ko_name,
                 "en_name": en_name,
                 "status": status,
                 "location": location,
                 "phone": phone,
                 "email": email}

    return render_template("professor_info.html", prof_data=prof_data)


if __name__ == "__main__":
    app.run(debug=True, port=9999)
