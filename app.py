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
import json
from crawler.ict import ict_professor as ip
from crawler.soft import soft_professor as sp

from flask import Flask, render_template, request, Response

app = Flask(__name__)

# Params
# position = config.POSITION

# Crawling Data
sp_adjunct_data = sp.get_adjunct()
sp_prof_data = sp.get_prof()
sp_honor_data = sp.get_honor()

ip_adjunct_data = ip.get_adjunct()
ip_prof_data = ip.get_prof()


def get_prof_data(switch, name):
    prof_data = dict()

    if switch == "soft":
        # Params
        ko_name = "Ko Name"
        en_name = "En Name"
        status = "Status"
        location = "Location"
        email = "Email"
        photo = "Photo"

        # Find the position
        prof_dict = None
        if name in sp_adjunct_data["name_kor"]:
            prof_dict = sp_adjunct_data
        elif name in sp_prof_data["name_kor"]:
            prof_dict = sp_prof_data
        elif name in sp_honor_data["name_kor"]:
            prof_dict = sp_honor_data

        # Count the number
        prof_count = 0
        for i in range(len(prof_dict["name_kor"])):
            if name == prof_dict["name_kor"][i]:
                prof_count = i

        # Put data to variable
        if "name_kor" in prof_dict:
            ko_name = prof_dict["name_kor"][prof_count]
        if "name_eng" in prof_dict:
            en_name = prof_dict["name_eng"][prof_count]
        if "position" in prof_dict:
            status = prof_dict["position"][prof_count]
        if "location" in prof_dict:
            location = prof_dict["location"][prof_count]
        if "email" in prof_dict:
            email = prof_dict["email"][prof_count]
        if "photo" in prof_dict:
            photo = prof_dict["photo"][prof_count]

        prof_data = {"ko_name": ko_name,
                     "en_name": en_name,
                     "status": status,
                     "location": location,
                     "email": email,
                     "photo": photo}

    elif switch == "ict":
        # Params
        ko_name = "Ko Name"
        en_name = "En Name"
        status = "Status"
        location = "Location"
        phone = "Phone"
        email = "Email"
        photo = "photo"

        # Find the position
        prof_dict = None
        if name in ip_adjunct_data["name_kor"]:
            prof_dict = ip_adjunct_data
        elif name in ip_prof_data["name_kor"]:
            prof_dict = ip_prof_data

        # Count the number
        prof_count = 0
        for i in range(len(prof_dict["name_kor"])):
            if name == prof_dict["name_kor"][i]:
                prof_count = i

        # Put data to variable
        if "name_kor" in prof_dict:
            ko_name = prof_dict["name_kor"][prof_count]
        if "name_eng" in prof_dict:
            en_name = prof_dict["name_eng"][prof_count]
        if "position" in prof_dict:
            status = prof_dict["position"][prof_count]
        if "location" in prof_dict:
            location = prof_dict["location"][prof_count]
        if "call" in prof_dict:
            phone = prof_dict["call"][prof_count]
        if "email" in prof_dict:
            email = prof_dict["email"][prof_count]
        if "photo" in prof_dict:
            photo = prof_dict["photo"][prof_count]

        prof_data = {"ko_name": ko_name,
                     "en_name": en_name,
                     "status": status,
                     "location": location,
                     "phone": phone,
                     "email": email,
                     "photo": photo}

    return prof_data


@app.route("/")
def root():
    soft_prof_list = sp_prof_data["name_kor"]
    soft_honor_list = sp_honor_data["name_kor"]
    soft_adjunct_list = sp_adjunct_data["name_kor"]

    ict_adjunct_list = ip_adjunct_data["name_kor"]
    ict_prof_list = ip_prof_data["name_kor"]

    return render_template("index.html",
                           soft_prof_list=soft_prof_list,
                           soft_honor_list=soft_honor_list,
                           soft_adjunct_list=soft_adjunct_list,
                           ict_adjunct_list=ict_adjunct_list,
                           ict_prof_list=ict_prof_list)


@app.route("/software_professor/<name>")
def render_software_professor_controller(name):
    soft_prof_list = sp_prof_data["name_kor"]
    soft_honor_list = sp_honor_data["name_kor"]
    soft_adjunct_list = sp_adjunct_data["name_kor"]

    ict_adjunct_list = ip_adjunct_data["name_kor"]
    ict_prof_list = ip_prof_data["name_kor"]

    prof_data = get_prof_data("soft", name)

    return render_template("professor_info.html",
                           soft_prof_list=soft_prof_list,
                           soft_honor_list=soft_honor_list,
                           soft_adjunct_list=soft_adjunct_list,
                           ict_adjunct_list=ict_adjunct_list,
                           ict_prof_list=ict_prof_list,
                           prof_data=prof_data)


@app.route("/ict_professor/<name>")
def render_ict_professor_controller(name):
    soft_prof_list = sp_prof_data["name_kor"]
    soft_honor_list = sp_honor_data["name_kor"]
    soft_adjunct_list = sp_adjunct_data["name_kor"]

    ict_adjunct_list = ip_adjunct_data["name_kor"]
    ict_prof_list = ip_prof_data["name_kor"]

    prof_data = get_prof_data("ict", name)

    return render_template("professor_info.html",
                           soft_prof_list=soft_prof_list,
                           soft_honor_list=soft_honor_list,
                           soft_adjunct_list=soft_adjunct_list,
                           ict_adjunct_list=ict_adjunct_list,
                           ict_prof_list=ict_prof_list,
                           prof_data=prof_data)


@app.route("/wiki/get", methods=["GET"])
def get_wiki_context():
    # When init rendering the page (at first)
    name = request.args.get("prof_name")
    # 여기에 db 함수 넣을 것

    print(name)

    context = "교수님 좋아요 ~~~~"  # db 결과 받아 올 것

    res = json.dumps({"context": context})

    return Response(res, status=200, mimetype="application/json")


@app.route("/wiki/write", methods=["POST"])
def write_wiki_context():
    name = request.form["prof_name"]
    context = request.form["context"]

    # context = context  # db 결과 받아 올 것
    # 여기에 db 함수 넣을 것

    print(context)

    res = json.dumps({"context": context})

    return Response(res, status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True, port=9999)
