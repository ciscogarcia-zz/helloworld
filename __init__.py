from flask import Flask, render_template, request, flash

from admin_report import Admin_Report
from DB import DB
app = Flask(__name__)

@app.route("/administrator_report", methods=['GET'])
def admin_report():
    admin_report = Admin_Report()
    db = DB()
    registered_users = db.get_registered_users()
    return render_template("admin.html", admin_report=admin_report, registered_users=registered_users)

@app.route("/", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user, messages = validate_input(request.form)
        if user['valid']:
            db = DB()
            db.insert_registered_user(user)
            print messages
            return render_template("confirm.html")
        else:
            return render_template("register.html", user=user, messages=messages)
    else:
        user = {}
        messages = {}
        return render_template("register.html", user=user, messages=messages)

def validate_input(form):
    user = {}
    user['fname'] = form['fname']
    user['lname'] = form['lname']
    user['address1'] = form['address1']
    user['address2'] = form['address2']
    user['city'] = form['city']
    user['state'] = form['state']
    user['zip'] = form['zip']
    user['country'] = form['country']
    user['valid'] = True

    messages = {}
    message_map = {'fname': "First Name", 'lname': "Last Name", 'address1': "Address", 'city': "City", 'state': "State", 'zip': "Zip Code", 'country': "Country"}

    for field, value  in user.items():
        messages[field] = ""
        if value == '' and field != 'address2':
            user['valid'] = False
            messages[field] = "* " + message_map[field] + " is required *"
        if field == 'zip':
            if value == '':
                messages[field] = "* " + message_map[field] + " is required *"
                continue
            if len(value) != 5 and len(value) != 10:
                messages[field] = "* Zip code must either be 5 digits or 9 digits with a hyphen. *"
            if not value.isnumeric():
                messages[field] = "* Zip code must be all numeric *"
            if len(value) == 10:
                if "-" not in value:
                    messages[field] = "* You must have a hyphen in the zip code. *"
                    continue
                zip1, zip2 = value.split("-")
                if len(zip1) != 5 or len(zip2) != 4:
                    messages[field] = "* Zip code must be in the following format: XXXXX-XXXX *"
                if not zip1.isnumeric() or not zip2.isnumeric():
                    messages[field] = "* Zip code must be all numeric. *"

    return user, messages

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
