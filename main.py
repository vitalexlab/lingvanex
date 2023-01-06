from flask import Flask

from utils.managet import run_parser

app = Flask(__name__)


@app.route("/")
def hello_world():
    parser = run_parser('https://apps.microsoft.com/store/category/Business')
    host = parser.host
    return f"<a href='{host}'>{host}</p>"
