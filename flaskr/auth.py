"""Module Authentication Blueprint"""

import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.database import get_database

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """View GET /register -> auth/register.html
    View POST /register"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        database = get_database()

        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                database.execute(
                    """INSERT INTO `user` (`username`, `password`)
                        VALUES (?, ?)""",
                    (username, generate_password_hash(password)),
                )
                database.commit()
            except database.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """View GET /login -> auth/login.html
    View POST /login"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        database = get_database()

        error = None

        user = database.execute(
            """SELECT * FROM `user`
                WHERE `username` = ?""",
            (username,),
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user() -> None:
    """Checks if a user id is stored in the session and gets that user’s data from the database,
    storing it on g.user, which lasts for the length of the request. If there is no user id,
    or if the id doesn’t exist, g.user will be None."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_database()
            .execute(
                """SELECT * FROM `user`
                    WHERE `id` = ?""",
                (user_id,),
            )
            .fetchone()
        )


@bp.route("/logout")
def logout():
    """View GET /logout"""
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    """Decorator for check if the user is logged."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
