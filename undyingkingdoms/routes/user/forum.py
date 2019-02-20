from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models.forms.message import MessageForm
from undyingkingdoms.models.forum import Forum, Thread, Post


@app.route('/user/forum/<int:thread_id>/<int:post_id>', methods=['GET', 'POST'])
@mobile_template('{mobile/}user/forum.html')
@login_required
def forum(template, thread_id=0, post_id=0):
    the_forum = Forum.query.first()
    the_thread = Thread.query.get(thread_id)
    the_post = Post.query.get(post_id)
    form = MessageForm()
    if the_thread is None:
        the_thread = "None"
    if the_post is None:
        the_post = "None"
    if form.validate_on_submit():
        new_post = Post(the_thread.id, current_user.id, form.title.data, form.content.data, post_id)
        new_post.save()
        if post_id == 0:
            post_id = new_post.id  #
        return redirect(url_for('forum', thread_id=thread_id, post_id=post_id))
    return render_template(template, form=form, forum=the_forum, the_thread=the_thread, the_post=the_post)
