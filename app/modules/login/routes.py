import os
import pathlib
import flask
import cachecontrol as cachecontrol
import google as google
import google_auth_oauthlib
import requests
from flask import session, abort, redirect, request
from flask_migrate import Migrate
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow

from app.modules.login import blueprint

GOOGLE_CLIENT_ID = "994624214778-q5sg1hsei2a3mvk79u5j17bdlrrs1k2t.apps.googleusercontent.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

client_secret_file = os.path.join(os.getcwd(), "env/client_secret.json")
scopes = ['https://www.googleapis.com/auth/userinfo.profile',
          'https://www.googleapis.com/auth/userinfo.email',
          'https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.metadata', 'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.readonly',
          'https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/admin.directory.user.readonly','openid']


# flow = Flow.from_client_secrets_file(client_secrets_file=client_secret_file,
#                                      scopes=scopes,
#                                      redirect_uri="http://127.0.0.1:5000/callback"
#                                      )


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if 'credentials' not in flask.session:
            return redirect('/authorize')
        else:
            return function()

    return wrapper


# @blueprint.route("/login")
# def login():
#     authorization_url, state = flow.authorization_url(access_type='online', include_granted_scopes='true')
#     session["state"] = state
#     return redirect(authorization_url)
#
#
# @blueprint.route("/callback")
# def callback():
#     flow.fetch_token(authorization_response=request.url)
#
#     if not session["state"] == request.args["state"]:
#         abort(500)  # State does not match!
#
#     credentials = flow.credentials
#     flask.session['credentials'] = credentials_to_dict(credentials)
#     request_session = requests.session()
#     cached_session = cachecontrol.CacheControl(request_session)
#     token_request = google.auth.transport.requests.Request(session=cached_session)
#
#     id_info = id_token.verify_oauth2_token(
#         id_token=credentials._id_token,
#         request=token_request,
#         audience=GOOGLE_CLIENT_ID
#     )
#
#     session["google_id"] = id_info.get("sub")
#     session["name"] = id_info.get("name")
#     return redirect("/")
#
#
@blueprint.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@blueprint.route('/authorize')
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secret_file, scopes=scopes)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = flask.url_for('login.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@blueprint.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secret_file, scopes=scopes, state=state)
    flow.redirect_uri = flask.url_for('login.oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    return redirect("/")


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
