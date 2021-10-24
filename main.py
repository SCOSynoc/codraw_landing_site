from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SelectField, SubmitField
from werkzeug.security import generate_password_hash
from wtforms.validators import DataRequired
import smtplib
from flask_fontawesome import FontAwesome
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('MY_SECRET_KEY')
Bootstrap(app)
FontAwesome(app)

my_email = os.environ.get('EMAIL')
password = os.environ.get('PASSWORD')


class ContactForm(FlaskForm):
    mail = StringField(label="Enter your mail", validators=[DataRequired()])
    message = StringField(label="Message")
    send = SubmitField(label="Send")


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")


@app.route("/cont", methods=['GET', 'POST'])
def contact():
    contact = ContactForm()
    if contact.validate_on_submit():
        mail_id = generate_password_hash(contact.mail.data)
        msgs = contact.message.data
        if mail_id:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(
                    from_addr=mail_id,
                    to_addrs=my_email,
                    msg=f"Subject:Codraw \n\n{msgs}"
                )
        return render_template('index.html')
    return render_template('message.html', form=contact)


@app.route("/privacy")
def privacy():
    return render_template('policy.html')


if __name__ == "__main__":
    app.run(host='localhost')
