from flask import Flask
from flask import render_template
from flask import request

from ai.text_to_sql import generate_sql

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    question = ""
    dialect = "MySQL"

    if request.method == "POST":
        question = request.form.get("question", "")
        dialect = request.form.get("dialect", "MySQL")
        result = generate_sql(question, dialect)

    return render_template(
        "index.html",
        result=result,
        question=question,
        dialect=dialect
    )


if __name__ == "__main__":
    app.run(debug=True)