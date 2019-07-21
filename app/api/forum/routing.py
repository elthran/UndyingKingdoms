from importlib import import_module

from flask import jsonify, url_for, request
from flask.views import MethodView

get_forum = lambda: import_module('app.models.forum')


class RoutingAPI(MethodView):
    def get(self):
        forum = get_forum()
        post_id = request.args.get('post_id', type=int)
        thread_id = request.args.get('thread_id', type=int)

        post = forum.Post.query.get(post_id)
        thread = forum.Thread.query.get(thread_id)

        routingTrail = [dict(
            url=url_for('forum', thread_id=0, post_id=0),
            name="Forum",
        )]
        if thread_id:
            routingTrail.append(dict(
                url=url_for('forum', thread_id=thread_id, post_id=0),
                name=thread.title,
            ))
        if post_id:
            routingTrail.append(dict(
                url=url_for('forum', thread_id=thread_id, post_id=post_id),
                name=post.title,
            ))

        return jsonify(
            routingTrail=routingTrail
        )
