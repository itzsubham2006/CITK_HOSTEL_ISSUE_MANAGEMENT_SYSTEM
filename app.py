from flask import Flask, render_template
from forms import Registration_form, login_form

app = Flask(__name__)

app.config["SECRET_KEY"] = "363dda57aa12f2c0fa8fd27e6d71212b1541154f48fc9d41df21898a9a301e53d946802750950018140df0fad0c9471795f75e51f1"


@app.route("/")
def register():
    form = Registration_form()
    return render_template("auth/register.html", title="register", form=form)

@app.route("/login")
def login():
    form = login_form()
    return render_template("auth/login.html", title="login", form=form)

if __name__ == "__main__":
    app.run(debug=True)
    
