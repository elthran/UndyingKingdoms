from flask import redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models.forum import Post
from undyingkingdoms.models.upvotes import Upvote


@app.route('/gameplay/upvote/<thread_id>/<post_id>', methods=['GET', 'POST'])
@login_required
def upvote(thread_id, post_id):
    if not current_user.in_active_session:
        current_user.in_active_session = True
    upvote = Upvote.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if upvote is None:
        upvote = Upvote(current_user.id, post_id, 1)
        upvote.save()
    else:
        upvote.vote = 1 - upvote.vote

    post = Post.query.filter_by(id=post_id).first()
    if post.parent_post_id == 0:
        new_post_id = post_id
    else:
        new_post_id = post.parent_post_id
    return redirect(url_for('forum', thread_id=thread_id, post_id=new_post_id))
