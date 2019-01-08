from flask import Flask, render_template, request
from script.harits import fungsi_adi
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("Home.html")

@app.route("/handle_data", methods=['POST'])
def handle_data():
    result = request.form.to_dict()
    try:
        hasil = fungsi_adi(result['query'])
    except:
        hasil = "Result not found, go search for another query !"
    return render_template("Hasil.html", result = [hasil, result['query']])

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = '5001', debug = True)
