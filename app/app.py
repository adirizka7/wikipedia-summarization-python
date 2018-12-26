from flask import Flask, render_template, request
from script.harits import fungsi_adi
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("Home.html")

@app.route("/handle_data", methods=['POST'])
def handle_data():
    result = request.form.to_dict()
    hasil = fungsi_adi(result['query'])
    return hasil

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = '5001', debug = True)
