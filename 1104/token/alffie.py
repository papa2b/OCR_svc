from flask import Flask, request

app = Flask(__name__)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    return f"인증 코드 받음: {code}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8808, debug=True)
