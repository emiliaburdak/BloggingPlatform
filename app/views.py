from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comments
from . import db

# import json
# from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', user=current_user, posts=posts)


@views.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method == 'POST':
        post = request.form.get('post')
        if len(post) < 1:
            flash('Post is too short!')
        else:
            new_post = Post(post=post, author=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('views.home'))

    return render_template('home.html', user=current_user)


@views.route('/delete_post/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash('Post does not exist', category='error')
    elif current_user.id != post.author:
        flash('You dont have permission', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')

    return redirect(url_for('views.home'))


@views.route('/user_posts/<username>')
@login_required
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User does not exist', category='error')
        return redirect(url_for('views.home'))
    else:
        # posts = Post.query.filter_by(author=user.id).all() jeden sposób
        posts = user.posts
        return render_template('user_posts.html', user=user, posts=posts)


@views.route('/add_comment/<post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    comment = request.form.get('comment')
    post = Post.query.filter_by(id=post_id)
    if len(comment) < 1:
        flash('Comment is too short!', category='error')
    else:
        if post:
            new_comment = Comments(comment=comment, author=current_user.id, post_id=post_id)
            db.session.add(new_comment)
            db.session.commit()
        else:
            flash('Post does not exist', category='error')
    return redirect(url_for('views.home'))


@views.route('/delete_comment/<int:comment_id>/<int:post_id>')
@login_required
def delete_comment(comment_id, post_id):
    comment = Comments.query.filter_by(id=comment_id, post_id=post_id).first()
    if comment.author != current_user.id:  #or carrent_user.id != comment.post.author
        flash('You dont have permission')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('views.home'))