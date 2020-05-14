from flask import Flask, request, jsonify
from .models import User
from requests import get

app = Flask(__name__)
server_user = User("dev", "dev")

REST_API_ID = "18575706"
MOBILE_ID = "18577476"
WEB_ID = "18577488"
COMPOSE_ID = "18784831"

HEADER = {"PRIVATE-TOKEN": "ios4yeuCgN6sz3UJ-XVB"}


def reg_token(data):
    token = data.get("token")
    if token is None or token == "":
        return "Missing parameter: 'token'", 400
    else:
        server_user.register_token(token)
        return "Token registered successfully"


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username is None:
        return "Missing parameter: 'username'", 400
    elif password is None:
        return "Missing parameter: 'password'", 400
    else:
        ret_val = server_user.check_credentials(username, password)
        if ret_val:
            return reg_token(data)
        else:
            return "Invalid credentials", 400


@app.route("/tokens", methods=["GET", "DELETE"])
def tokens():
    if request.method == "GET":
        return jsonify(server_user.tokens)
    else:
        token = request.get_json().get("token")
        if token is None or token == "":
            return "Missing parameter: 'token'", 400
        else:
            ret_val = server_user.delete_token(token)
            if ret_val:
                return "Token deleted with success!"
            else:
                return "Token does not exist", 400


def fetch_build_state(project_id):
    response = get(url=f"https://gitlab.com/api/v4/projects/{project_id}/pipelines?per_page=1&page=1", headers=HEADER).json()
    if len(response) > 0:
        return response[0]["status"]
    else:
        return None


@app.route("/build-info")
def get_build_info():
    info = {"rest_api": "null", "mobile": "null", "web": "null", "deploy": "null"}
    
    # rest_api
    status = fetch_build_state(REST_API_ID)
    if status is not None:
        info["rest_api"] = status

    # web
    status = fetch_build_state(WEB_ID)
    if status is not None:
        info["web"] = status

    # mobile
    status = fetch_build_state(MOBILE_ID)
    if status is not None:
        info["mobile"] = status

    # deploy
    status = fetch_build_state(COMPOSE_ID)
    if status is not None:
        info["deploy"] = status

    return info

if __name__ == "__main__":
    app.run()