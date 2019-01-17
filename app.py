# -*- coding: utf-8 -*-

"""
 Created by IntelliJ IDEA.
 Project: Jaram-Professor-Crawler
 ===========================================
 User: ByeongGil Jung
 Date: 2019-01-17
 Time: 오후 4:08
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def root():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=9999)
