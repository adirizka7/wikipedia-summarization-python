from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("Home.html")

@app.route("/handle_data", methods=['POST'])
def handle_data():
    result = request.form.to_dict()
    return (str(result))

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = '5001', debug = True)
