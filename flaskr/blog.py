"""Module Blog Blueprint"""

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.database import get_mysql_connection

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """View GET blog/index.html
    The index will show all of the posts, most recent first."""
    connection = get_mysql_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT p.`id`, `title`, `body`, `created`, `author_id`, `username`
                FROM `post` `p`
                JOIN `user` `u`
                ON p.`author_id` = u.`id`
                ORDER BY created DESC"""
        )
        posts = cursor.fetchall()

    return render_template("blog/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """View GET /create -> blog/create.html
    View POST /create"""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            connection = get_mysql_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO `post` (`title`, `body`, `author_id`)
                        VALUES (%s, %s, %s)""",
                    (title, body, g.user["id"]),
                )
            connection.commit()

            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


def get_post(id, check_author=True):
    """Get post from database by id."""
    connection = get_mysql_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT p.`id`, `title`, `body`, `created`, `author_id`, `username`
                FROM `post` `p`
                JOIN `user` `u`
                ON p.`author_id` = u.`id`
                WHERE p.`id` = %s""",
            (id,),
        )
        post = cursor.fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """View GET /id/update -> blog/update.html
    View POST /id/update"""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            connection = get_mysql_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE `post`
                        SET `title` = %s, `body` = %s
                        WHERE `id` = %s""",
                    (title, body, id),
                )
            connection.commit()

            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """View POST /id/delete"""
    get_post(id)

    connection = get_mysql_connection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM `post` WHERE `id` = %s", (id,))
    connection.commit()

    return redirect(url_for("blog.index"))
