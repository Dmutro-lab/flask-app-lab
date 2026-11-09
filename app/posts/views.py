from flask import abort, flash, redirect, render_template, request, session, url_for

from app import db
from app.posts import post_bp
from app.posts.forms import PostForm
from app.posts.models import Post, PostCategory

CATEGORY_NAMES = {
    "news": "Новини",
    "publication": "Публікація",
    "tech": "Технології",
    "other": "Інше",
}


def _category_value(category):
    return category.value if isinstance(category, PostCategory) else str(category)


@post_bp.route("/post/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            posted=form.publish_date.data,
            category=PostCategory(form.category.data),
            is_active=form.enabled.data,
            author=session.get("username", "Anonymous")[:20],
        )
        db.session.add(post)
        db.session.commit()
        flash("Post added successfully", "success")
        return redirect(url_for("posts.all_posts"))
    return render_template("posts/add_post.html", form=form, heading="Створення поста")


@post_bp.route("/post")
def all_posts():
    posts = db.session.scalars(
        db.select(Post).where(Post.is_active.is_(True)).order_by(Post.posted.desc())
    ).all()
    return render_template("posts/posts.html", posts=posts, category_names=CATEGORY_NAMES)


@post_bp.route("/post/<int:post_id>")
def detail_post(post_id):
    post = db.get_or_404(Post, post_id)
    return render_template("posts/detail_post.html", post=post, category_names=CATEGORY_NAMES)


@post_bp.route("/post/<int:post_id>/update", methods=["GET", "POST"])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = PostForm(obj=post)
    if form.is_submitted() and form.validate():
        post.title = form.title.data.strip()
        post.content = form.content.data.strip()
        post.is_active = form.enabled.data
        post.posted = form.publish_date.data
        post.category = PostCategory(form.category.data)
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("posts.detail_post", post_id=post.id))
    if not form.is_submitted():
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted
        form.category.data = _category_value(post.category)
    return render_template("posts/add_post.html", form=form, heading="Редагування поста", post=post)


@post_bp.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "success")
        return redirect(url_for("posts.all_posts"))
    return render_template("posts/delete_confirm.html", post=post)
