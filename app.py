from flask import Flask, render_template, redirect, request
import sqlite3
from Parser import Parser

app = Flask(__name__)


@app.route('/')
def hello_world():
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()
    all_elements = cursor.execute("SELECT * FROM pastCheck")
    tup = all_elements.fetchall()
    allCheck = []
    for element in tup:
        allCheck.append(list(element))

    connect.commit()
    connect.close()
    return render_template("html.html", last_conversion=allCheck)

@app.route('/api/endpoint', methods=['POST'])
def api_endpoint():
    pars = Parser()
    try:
        inputStr = request.form.get("input")

    except Exception:
        inputStr = None

    result = pars.generiere_pruefziffer(inputStr)
    connect = sqlite3.connect("database.db")
    cursor =connect.cursor()
    cursor.execute("insert into pastCheck (pastInput, pastResult) values (?, ?)",(inputStr, result))
    connect.commit()
    connect.close()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
