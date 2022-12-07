import os
import io
import json
import atexit
import logging
from flask_sock import Sock
import services.recorder as rec
import services.reporting as rep
import services.subscription as sub
from flask import Flask, render_template, send_from_directory
from flask import request, Response, session
from adapters import postgres, user_repository, notification, report_repository


def page_not_found(e):
    return render_template('404.html'), 404


def server_error(e):
    return render_template('500.html'), 500


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static")
app.secret_key = os.urandom(24)
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, server_error)
sock = Sock(app)


def get_pool():
    try:
        pool = postgres.get_connection_pool()
    except (Exception) as err:
        app.logger.error(err)
        raise err
    return pool


connection_pool = get_pool()


def initialize_repos(pool):
    user_repo = user_repository.UserRepository(pool)
    report_repo = report_repository.ReportRepository(pool)
    return user_repo, report_repo


user_repo, report_repo = initialize_repos(connection_pool)
user_notifier = notification.UserNotification()
clients = dict()


@app.route("/starter")
def starter():
    pass


@app.route("/register", methods=["POST"])
def signup():
    pass


@app.route("/auth", methods=["POST"])
def login():
    pass


@app.route("/users")
def get_session_user():
    pass


@sock.route('/tab-capture')
def tab_capture(sock):
    pass


@app.route("/logs/<report_id>/users/<user_id>/console-log-entries",
           methods=["POST"])
def console_log_entries(report_id: str, user_id: str):
    pass


@app.route("/logs/<report_id>/users/<user_id>/network-log-entries",
           methods=["POST"])
def network_log_entries(report_id: str, user_id: str):
    pass


def is_empty(str_input: str) -> bool:
    if str_input is None:
        return True

    str_input = str_input.strip()
    if len(str_input) == 0:
        return True

    return False


@app.route("/finalize-recording/<report_id>")
def show_report(report_id):
    pass


def router(environ, start_reponse):
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    return app(environ, start_reponse)


def shutdown_hook():
    connection_pool.close()
    return


atexit.register(shutdown_hook)
