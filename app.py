# rendering contact.html template and making JSON response
import os
from email.message import Message

from django.core import mail
from flask import Flask, render_template, jsonify, request, make_response
# using Flask-WTF CSRF protection for AJAX requests
from flask_wtf.csrf import CSRFProtect
# initializing app
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)


@app.route('/')
def index():
    return render_template("pages/contact.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """User can send e-mail via contact form"""

    if request.method == 'POST':
        """User sent an email request"""
        msg = Message("Feedback", recipients=[app.config['MAIL_USERNAME']])
        msg.body = "You have received new feedback from {0} {1} <{2}>.\n\n {3}".format(
            request.form['first-name'],
            request.form['last-name'],
            request.form['mail-address'],
            request.form['comment-field'])
        try:
            mail.send(msg)
            msg = "We will respond as soon as possible."
            category = "success"
        except Exception as err:
            msg = str(err)
            category = "danger"

        resp = {'feedback': msg, 'category': category}
        return make_response(jsonify(resp), 200)

    elif request.method == 'GET':
        """User is viewing the page"""
        return render_template('pages/contact.html')


app.run()
