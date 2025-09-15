import json
import logging
from flask import Flask, g, session, redirect, url_for, jsonify, request
from flask_oidc import OpenIDConnect
import urllib.parse
from flask_session import Session  # Add the Flask-Session module

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Flask-Session settings to store the session on the server
app.config["SESSION_TYPE"] = "filesystem"  # Stores sessions in the file system
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True  # Sign session cookies for greater security
app.config["SESSION_FILE_DIR"] = (
    "/tmp/flask_sessions"  # Location where sessions will be stored on the server
)
app.config["SESSION_COOKIE_SECURE"] = False  # Set to True in production if using HTTPS

# Inicialize Flask-Session
Session(app)

app.config.update(
    {
        "SECRET_KEY": "CLIENT_SECRET_KEYCLOAK",
        "TESTING": True,
        "DEBUG": True,
        "OIDC_CLIENT_SECRETS": "client_secrets.json",
        "OIDC_ID_TOKEN_COOKIE_SECURE": False,
        "OIDC_USER_INFO_ENABLED": True,
        "OIDC_OPENID_REALM": "master",
        "OIDC_SCOPES": ["openid", "email", "profile"],
        "OIDC_INTROSPECTION_AUTH_METHOD": "client_secret_post",
    }
)

oidc = OpenIDConnect(app)


@app.route("/")
def hello_world():
    if oidc.user_loggedin:
        return (
            'Hello, %s, <a href="/private">See private</a> '
            '<a href="/logout">Log out</a>'
        ) % oidc.user_getfield("preferred_username")
    else:
        return """
            <html>
                <head>
                    <style>
                        body {
                            font-family: 'Helvetica', sans-serif;
                            background-color: #f9f9f9;
                            color: #333;
                            margin: 0;
                            padding: 0;
                        }
                        .navbar {
                            background-color: #4CAF50;
                            padding: 1em;
                            text-align: center;
                        }
                        .navbar a {
                            color: white;
                            font-size: 1.5em;
                            text-decoration: none;
                            padding: 0 15px;
                        }
                        .hero {
                            text-align: center;
                            padding: 50px;
                            background-color: #e3f2fd;
                        }
                        .hero h1 {
                            font-size: 4em;
                            margin-bottom: 0.5em;
                        }
                        .hero p {
                            font-size: 1.5em;
                            margin-bottom: 1.5em;
                            color: #555;
                        }
                        .hero a {
                            font-size: 1.2em;
                            color: white;
                            background-color: #007bff;
                            padding: 0.7em 1.5em;
                            border-radius: 30px;
                            text-decoration: none;
                            transition: background-color 0.3s ease;
                        }
                        .hero a:hover {
                            background-color: #0056b3;
                        }
                        .products {
                            display: flex;
                            justify-content: space-around;
                            margin: 50px 0;
                        }
                        .product-card {
                            background: white;
                            border-radius: 10px;
                            padding: 20px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            text-align: center;
                            max-width: 300px;
                        }
                        .product-card img {
                            max-width: 100%;
                            border-radius: 10px;
                        }
                        .product-card h3 {
                            font-size: 1.5em;
                            margin: 15px 0;
                        }
                        .product-card a {
                            font-size: 1em;
                            color: #4CAF50;
                            text-decoration: none;
                            padding: 0.5em 1em;
                            border: 2px solid #4CAF50;
                            border-radius: 5px;
                            transition: background-color 0.3s ease, color 0.3s ease;
                        }
                        .product-card a:hover {
                            background-color: #4CAF50;
                            color: white;
                        }
                        footer {
                            text-align: center;
                            padding: 20px;
                            background-color: #333;
                            color: white;
                            position: absolute;
                            width: 100%;
                            bottom: 0;
                        }
                    </style>
                </head>
                <body>
                    <div class="navbar">
                        <a href="/">Flask OSP</a>
                    </div>
                    <div class="hero">
                        <h1>Welcome to Flask OSP</h1>
                        <p>Your one-stop platform for all your needs.</p>
                        <a href="/private">Login with Keycloak</a>
                    </div>
                    <div class="products">
                        <div class="product-card">
                            <img src="/static/img/bag.jpg" alt="Product 1">
                            <h3>Product 1</h3>
                            <p>Amazing features and unbeatable price.</p>
                            <a href="#">View More</a>
                        </div>
                        <div class="product-card">
                            <img src="/static/img/bike.jpg" alt="Product 2">
                            <h3>Product 2</h3>
                            <p>Top-quality product for all your needs.</p>
                            <a href="#">View More</a>
                        </div>
                        <div class="product-card">
                            <img src="/static/img/shoes.jpg" alt="Product 3">
                            <h3>Product 3</h3>
                            <p>Stylish and modern, perfect for everyone.</p>
                            <a href="#">View More</a>
                        </div>
                    </div>
                    <footer>
                        Flask OSP &copy; 2024 - All Rights Reserved
                    </footer>
                </body>
            </html>
        """


@app.route("/private")
@oidc.require_login
def hello_me():
    info = oidc.user_getinfo(
        ["preferred_username", "email", "sub", "compliance_veryhigh"]
    )
    username = info.get("preferred_username")
    email = info.get("email")
    user_id = info.get("sub")

    if oidc.user_loggedin:
        access_token = oidc.get_access_token()

    return """
        <html>
            <head>
                <style>
                    body {{
                        font-family: 'Helvetica', sans-serif;
                        background-color: #f9f9f9;
                        color: #333;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        text-align: center;
                        margin-top: 10%;
                    }}
                    h1 {{
                        font-size: 2.5em;
                        color: #333;
                        margin-bottom: 0.5em;
                    }}
                    p {{
                        font-size: 1.2em;
                        margin-bottom: 2em;
                    }}
                    ul {{
                        list-style: none;
                        padding: 0;
                    }}
                    li {{
                        display: inline;
                        margin-right: 10px;
                    }}
                    a {{
                        font-size: 1.2em;
                        color: #007bff;
                        text-decoration: none;
                    }}
                    a:hover {{
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Welcome, {username}!</h1>
                    <p>Your email is {email}, and your user ID is {user_id}.</p>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/logout">Log out</a></li>
                    </ul>
                </div>
            </body>
        </html>
    """.format(
        username=username, email=email, user_id=user_id
    )


@app.route("/logout")
def logout():
    id_token = oidc.get_id_token()

    if not id_token:
        logging.warning("ID Token is missing or invalid.")
        return redirect(url_for("hello_world"))

    # Build the Keycloak logout URL
    logout_url = (
        "http://127.0.0.1:8080/realms/master/protocol/openid-connect/logout?id_token_hint=%s&post_logout_redirect_uri=%s"
        % (id_token, urllib.parse.quote("http://127.0.0.1:5000/", safe=""))
    )

    # Clear the Flask session
    session.clear()

    # Expire all cookies related to OIDC and session
    response = redirect(logout_url)
    response.set_cookie("session", "", expires=0)
    response.set_cookie("oidc_id_token", "", expires=0)
    response.set_cookie("oidc_access_token", "", expires=0)
    response.set_cookie("oidc_refresh_token", "", expires=0)
    response.set_cookie("remember_token", "", expires=0)

    # Remove Keycloak session cookies manually
    response.set_cookie("KEYCLOAK_SESSION", "", expires=0)
    response.set_cookie("KEYCLOAK_IDENTITY", "", expires=0)
    response.set_cookie("KEYCLOAK_SESSION_LEGACY", "", expires=0)

    # Remove all cookies set by Flask (just to ensure)
    for cookie in request.cookies:
        response.delete_cookie(cookie)

    logging.info(f"Redirecting to logout URL: {logout_url}")

    return response


@app.route("/backchannel-logout", methods=["POST"])
def backchannel_logout():
    """Endpoint for backchannel logout requests"""
    logging.info("Backchannel logout request received.")

    # Clear the session and cookies
    session.clear()

    response = jsonify({"status": "logged out"})
    response.set_cookie("session", "", expires=0)
    response.set_cookie("oidc_id_token", "", expires=0)
    response.set_cookie("oidc_access_token", "", expires=0)
    response.set_cookie("oidc_refresh_token", "", expires=0)
    response.set_cookie("remember_token", "", expires=0)

    # Remove all cookies set by Flask (just to ensure)
    for cookie in request.cookies:
        response.delete_cookie(cookie)

    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
