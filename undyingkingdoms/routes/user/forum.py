from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models.forms.forum import ForumPost
from undyingkingdoms.models.forum import Forum, Thread, Post


@login_required
@app.route('/user/forum/<int:thread_id>', methods=['GET', 'POST'])
def forum(thread_id=0):
    if not current_user.logged_in:
        current_user.logged_in = True
        
    the_forum = Forum.query.first()
    the_thread = Thread.query.filter_by(id=thread_id).first()
    
    form = ForumPost()
    if form.validate_on_submit() and the_thread is not None:
        new_post = Post(the_thread.id, current_user.id, form.title.data, form.message.data)
        new_post.save()
        return redirect(url_for('forum'))
    return render_template('user/forum.html', form=form, forum=the_forum, the_thread=the_thread)
