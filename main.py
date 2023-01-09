from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lingvanex_test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Application(db.Model):

    __tablename__ = 'application_data'

    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(50), nullable=False)
    release_year = db.Column(db.Date, default=datetime.utcnow)
    email = db.Column(db.String(50))

    def __repr__(self):
        return f'App {self.app_name} created by {self.company_name}'


@app.route('/')
def get_all_apps():
    all_apps_data = Application.query.all()
    return render_template('hello.html', data=all_apps_data)

@app.route('/parse')
def parse_site():
    all_apps_data = Application.query.all()
    return render_template('hello.html', data=all_apps_data)