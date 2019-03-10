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
from flask_sqlalchemy import SQLAlchemy, inspect

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Crawling Data
sp_adjunct_data = sp.get_adjunct()
sp_prof_data = sp.get_prof()
sp_honor_data = sp.get_honor()

ip_adjunct_data = ip.get_adjunct()
ip_prof_data = ip.get_prof()


# DB
class Professor(db.Model):
    __tablename__ = "professor"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    en_name = db.Column(db.String(20))
    department = db.Column(db.String(10))
    status = db.Column(db.String(10))

    def __init__(self, en_name, department, status):
        self.en_name = en_name
        self.department = department
        self.status = status

    def __repr__(self):
        return "id : {}, en_name : {}, department : {}, status : {}" \
            .format(self.id, self.en_name, self.department, self.status)


class Wiki(db.Model):
    __tablename__ = "wiki"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    en_name = db.Column(db.String(20), db.ForeignKey(Professor.en_name))
    context = db.Column(db.String(1000))

    def __init__(self, en_name):
        self.en_name = en_name
        self.context = "위키 내용을 입력해주세요."

    def __repr__(self):
        return "id : {}, en_name : {}, context : {}".format(self.id, self.en_name, self.context)


def init_db_data():
    # Insert professor data to db
    for name in sp_adjunct_data["name_eng"]:
        db.session.add(Professor(en_name=name, department="soft", status="adjunct"))
    for name in sp_prof_data["name_eng"]:
        db.session.add(Professor(en_name=name, department="soft", status="prof"))
    for name in sp_honor_data["name_eng"]:
        db.session.add(Professor(en_name=name, department="soft", status="honor"))

    for name in ip_adjunct_data["name_eng"]:
        db.session.add(Professor(en_name=name, department="ict", status="adjunct"))
    for name in ip_prof_data["name_eng"]:
        db.session.add(Professor(en_name=name, department="ict", status="prof"))

    db.session.commit()
    print("> Completed to insert professor data to the table")

    # Insert wiki data to db
    for prof_en_name in db.session.query(Professor.en_name):
        db.session.add(Wiki(en_name=prof_en_name[0]))

    db.session.commit()
    print("> Completed to insert wiki data to the table")


def drop_and_create_tables():
    # Drop tables
    ins = inspect(db.engine)

    tables = ins.get_table_names()
    if tables is not None:
        print("> Tables in DB are exist")

    for table in ins.get_table_names():
        if table == "professor":
            Professor.__table__.drop(db.engine)
            print("> Completed to delete the table, 'Professor'")
        elif table == "wiki":
            Wiki.__table__.drop(db.engine)
            print("> Completed to delete the table, 'Wiki'")

    # Create tables
    db.create_all()
    print("> Completed to create tables")


# Crawler
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
        prof_index = 0
        for i in range(len(prof_dict["name_kor"])):
            if name == prof_dict["name_kor"][i]:
                prof_index = i

        # Put data to variable
        if "name_kor" in prof_dict:
            ko_name = prof_dict["name_kor"][prof_index]
        if "name_eng" in prof_dict:
            en_name = prof_dict["name_eng"][prof_index]
        if "position" in prof_dict:
            status = prof_dict["position"][prof_index]
        if "location" in prof_dict:
            location = prof_dict["location"][prof_index]
        if "email" in prof_dict:
            email = prof_dict["email"][prof_index]
        if "photo" in prof_dict:
            photo = prof_dict["photo"][prof_index]

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
        prof_index = 0
        for i in range(len(prof_dict["name_kor"])):
            if name == prof_dict["name_kor"][i]:
                prof_index = i

        # Put data to variable
        if "name_kor" in prof_dict:
            ko_name = prof_dict["name_kor"][prof_index]
        if "name_eng" in prof_dict:
            en_name = prof_dict["name_eng"][prof_index]
        if "position" in prof_dict:
            status = prof_dict["position"][prof_index]
        if "location" in prof_dict:
            location = prof_dict["location"][prof_index]
        if "call" in prof_dict:
            phone = prof_dict["call"][prof_index]
        if "email" in prof_dict:
            email = prof_dict["email"][prof_index]
        if "photo" in prof_dict:
            photo = prof_dict["photo"][prof_index]

        prof_data = {"ko_name": ko_name,
                     "en_name": en_name,
                     "status": status,
                     "location": location,
                     "phone": phone,
                     "email": email,
                     "photo": photo}

    return prof_data


# Routing
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


@app.route("/wiki/get", methods=["POST"])
def get_wiki_context():
    # When init rendering the page (at first)
    name = request.form["prof_name"]
    name = name.split(" : ")[1]

    context = db.session.query(Wiki.context).filter(Wiki.en_name == name).one()

    res = json.dumps({"context": context})

    return Response(res, status=200, mimetype="application/json")


@app.route("/wiki/write", methods=["POST"])
def write_wiki_context():
    name = request.form["prof_name"]
    name = name.split(" : ")[1]
    context = request.form["context"]

    wiki = db.session.query(Wiki).filter(Wiki.en_name == name).one()
    wiki.context = context

    db.session.commit()

    res = json.dumps({"context": context})

    return Response(res, status=200, mimetype="application/json")


# Activate app
def activate_app():
    # Init db
    print("Initiating DB ...")
    drop_and_create_tables()
    init_db_data()


if __name__ == "__main__":
    activate_app()
    app.run(debug=False, port=9999)
