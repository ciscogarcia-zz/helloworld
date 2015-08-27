from flask import Flask, render_template

from admin_report import Admin_Report

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    admin_report = Admin_Report()
    return render_template("admin.html", admin_report=admin_report)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
