from flask import abort, flash, redirect, render_template, request, url_for

from app import db
from app.posts import post_bp
from app.posts.forms import PostForm
from app.posts.models import Post, PostCategory, Tag
from app.users.models import User

CATEGORY_NAMES = {
    "news": "Новини",
    "publication": "Публікація",
    "tech": "Технології",
    "other": "Інше",
}


def _category_value(category):
    return category.value if isinstance(category, PostCategory) else str(category)


def _populate_relationship_choices(form):
    authors = db.session.scalars(db.select(User).order_by(User.id)).all()
    tags = db.session.scalars(db.select(Tag).order_by(Tag.id)).all()
    form.author_id.choices = [(author.id, author.username) for author in authors]
    form.tags.choices = [(tag.id, tag.name) for tag in tags]


@post_bp.route("/post/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    _populate_relationship_choices(form)
    if form.validate_on_submit():
        author = db.session.get(User, form.author_id.data)
        selected_tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all() if form.tags.data else []
        if author is None:
            form.author_id.errors.append("Оберіть наявного користувача.")
        else:
            post = Post(
                title=form.title.data.strip(),
                content=form.content.data.strip(),
                posted=form.publish_date.data,
                category=PostCategory(form.category.data),
                is_active=form.enabled.data,
                user=author,
                tags=selected_tags,
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
    _populate_relationship_choices(form)
    if form.is_submitted() and form.validate():
        author = db.session.get(User, form.author_id.data)
        if author is None:
            form.author_id.errors.append("Оберіть наявного користувача.")
        else:
            selected_tags = db.session.scalars(
                db.select(Tag).where(Tag.id.in_(form.tags.data))
            ).all() if form.tags.data else []
            post.title = form.title.data.strip()
            post.content = form.content.data.strip()
            post.is_active = form.enabled.data
            post.posted = form.publish_date.data
            post.category = PostCategory(form.category.data)
            post.user = author
            post.tags = selected_tags
            db.session.commit()
            flash("Post updated successfully", "success")
            return redirect(url_for("posts.detail_post", post_id=post.id))
    if not form.is_submitted():
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted
        form.category.data = _category_value(post.category)
        form.author_id.data = post.user_id
        form.tags.data = [tag.id for tag in post.tags]
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
