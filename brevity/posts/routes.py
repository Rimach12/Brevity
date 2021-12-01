from flask import (render_template, url_for, flash, redirect,
                    request, abort, Blueprint, jsonify)
from flask_login import login_required, current_user
from brevity import db
from brevity.posts.forms import CommentForm, PostForm
from brevity.models import Comment, Post

posts = Blueprint('posts', '__name__')



@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title = 'New Post', form = form, legend='New Post')



@posts.route('/post/<int:post_id>/vote/<action>', methods=['GET', 'POST'])
@login_required
def vote_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    
    if action == 'upvote':
        current_user.upvote_post(post)
        db.session.commit()
        upvote_count = post.upvotes.count()
        downvote_count = post.downvotes.count()
        return jsonify({'result': 'success', 'upvote_count': upvote_count, 'downvote_count': downvote_count})
    
    elif action == 'downvote':
        current_user.downvote_post(post)
        db.session.commit()
        upvote_count = post.upvotes.count()
        downvote_count = post.downvotes.count()
        return jsonify({'result': 'success', 'upvote_count': upvote_count, 'downvote_count': downvote_count})

    elif action =='unauthorized_upvote':
        current_user.upvote_post(post)
        db.session.commit()
        return redirect(request.referrer)

    elif action == 'unauthorized_downvote':
        current_user.downvote_post(post)
        db.session.commit()
        return redirect(request.referrer)


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])            #'int:' imposes that post_id must be int.
def post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)                               #get(id) is used to query the db through Primary key. 
                                                                        #get_or_404(id) to return 404 error instead of None in case of missing entry.
    
    comments = Comment.query.filter_by(post_id = post_id)
        
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template('post.html', title="post.title",form = form, post=post, comments = comments)



@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title = 'Update Post',
                            form = form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
