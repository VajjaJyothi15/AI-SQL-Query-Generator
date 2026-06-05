import os
import json

from flask import (
    Flask,
    render_template,
    request,
    send_file
)

from ai.text_to_sql import generate_sql

app = Flask(__name__)

HISTORY_FILE = "history/queries.json"


def load_history():

    if not os.path.exists(HISTORY_FILE):

        return []

    try:

        with open(HISTORY_FILE, "r") as f:
            return json.load(f)

    except:

        return []


def save_history(question, query):

    history = load_history()

    history.insert(
        0,
        {
            "question": question,
            "query": query
        }
    )

    history = history[:10]

    with open(HISTORY_FILE, "w") as f:

        json.dump(
            history,
            f,
            indent=4
        )


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    question = ""

    dialect = "MySQL"

    model = "llama-3.3-70b-versatile"

    theme = "dark"

    history = load_history()

    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        )

        dialect = request.form.get(
            "dialect",
            "MySQL"
        )

        model = request.form.get(
            "model",
            "llama-3.3-70b-versatile"
        )

        theme = request.form.get(
            "theme",
            "dark"
        )

        result = generate_sql(
            question,
            dialect,
            model
        )

        if result["query"]:

            save_history(
                question,
                result["query"]
            )

            history = load_history()

    return render_template(
        "index.html",
        result=result,
        question=question,
        dialect=dialect,
        model=model,
        theme=theme,
        history=history
    )


@app.route("/download")
def download():

    sql = request.args.get(
        "query",
        ""
    )

    path = "generated/generated_query.sql"

    os.makedirs(
        "generated",
        exist_ok=True
    )

    with open(path, "w") as f:

        f.write(sql)

    return send_file(
        path,
        as_attachment=True
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )