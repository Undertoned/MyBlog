# --*-- coding=utf-8 --*--
from flask import render_template, request, flash, redirect, url_for, jsonify
from . import main
from .. import db
from .forms import PostForm, EditForm
from ..models import Post, Category
from flask_login import login_required

PER_POSTS_PER_PAGE = 8

#主页路由
@main.route('/')
@main.route('/blog')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=PER_POSTS_PER_PAGE, error_out=False)
    posts = pagination.items
    category = Category.query.order_by(Category.count)[::-1]
    return render_template('index.html', posts=posts, pagination=pagination, categorys=category)

#博客发布路由
@main.route('/write', methods=['GET', 'POST'])
#@login_required
def write():
    form = PostForm()
    category = Category.query.filter_by(tag=form.category.data).first()
    if form.validate_on_submit():
        if category:
            category.count += 1
            post = Post(title=form.title.data, body=form.body.data,
                        summary=form.summary.data, category=category)
        else:
            post = Post(title=form.title.data, body=form.body.data,
                        summary=form.summary.data, category=Category(form.category.data))
        db.session.add(post)
        flash('You have posted a blog')
        return redirect(url_for('main.post', title=post.title))
    return render_template('write.html', form=form)

##博客编辑路由
@main.route('/edit/<string:title>', methods=['GET', 'POST'])
#@login_required
def edit(title):
    post = Post.query.filter_by(title=title).first_or_404()
    form = EditForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.summary = form.summary.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('main.post',title=post.title))
    form.title.data = post.title
    form.body.data = post.body
    form.summary.data = post.summary
    return render_template('edit.html', form=form)

#博客文章独立网址路由
@main.route('/post/<string:title>', methods=['GET'])
def post(title):
    post = Post.query.filter_by(title=title).first_or_404()
    return render_template("post.html", post=post)

#标签路由
@main.route('/category/<tag>',methods=['GET'])
def category(tag):
    page = request.args.get('page', 1, type=int)
    the_posts =Category.query.filter_by(tag=tag).first().posts
    pagination =the_posts .paginate(page,per_page=PER_POSTS_PER_PAGE,error_out=False)
    posts = pagination.items

    return render_template("category_search.html",posts=posts)

#其他功能
@main.route('/music')
def love_music():
    return render_template('music.html')

@main.route('/about')
def about_me():
    # liked = Like.query.get_or_404(1)
    return render_template("about.html")




