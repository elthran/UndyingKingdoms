from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models.forms.forum import ForumPost
from undyingkingdoms.models.forum import Forum, Thread, Post


@login_required
@app.route('/user/forum/', methods=['GET', 'POST'])
def forum():
    if not current_user.logged_in:
        current_user.logged_in = True
    the_forum = Forum.query.first()
    if the_forum is None:
        the_forum = Forum()
        the_forum.save()
    
    the_thread = Thread.query.first()
    if the_thread is None:
        the_thread = Thread(the_forum.id, "Bug Reports")
        the_thread.save()
        
    form = ForumPost()
    if form.validate_on_submit():
        new_post = Post(the_thread.id, form.title.data, form.message.data)
        new_post.save()
        return redirect(url_for('forum'))
    return render_template('user/forum.html', forum=the_forum)
