from sqlalchemy import desc

from extensions import flask_db as db
from undyingkingdoms.models.bases import GameEvent
from undyingkingdoms.models.upvotes import Upvote


class Forum(GameEvent):
    threads = db.relationship('Thread', backref='forum')

    def __init__(self):
        pass


class Thread(GameEvent):
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)
    posts = db.relationship('Post', backref='thread')
    title = db.Column(db.String(32))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship("User")

    def __init__(self, forum_id, title, author_id):
        self.forum_id = forum_id
        self.title = title
        self.author_id = author_id
        
    def get_post_count(self):
        return len(self.posts)
    
    def get_most_recent_post(self):
        return Post.query.filter_by(thread_id=self.id).order_by(desc('time_created')).first()

    def get_author(self):
        return self.author.username

    def get_votes(self):
        """Return sum of all votes on all posts."""
        return sum([
            Upvote.query.filter_by(post_id=post.id , vote=1).count()
            for post in self.posts
        ])

    def get_views(self):
        """Return sum of all views on all posts."""
        raise NotImplementedError("We currently don't have this feature.")
        # return sum([
        #     post.views
        #     for post in self.posts
        # ])
        
        
class Post(GameEvent):
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    parent_post_id = db.Column(db.Integer)  # 0 if this is the parent
    title = db.Column(db.String(32))
    content = db.Column(db.String(5000))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    votes = db.Column(db.Integer)

    author = db.relationship("User")

    def __init__(self, thread_id, author_id, title, content, parent_post_id):
        self.thread_id = thread_id
        self.author_id = author_id
        self.title = title
        self.content = content
        self.parent_post_id = parent_post_id
        self.votes = 0

    def get_reply_count(self):
        replies = Post.query.filter_by(parent_post_id=self.id).all()
        return len(replies)

    def get_replies(self):
        return Post.query.filter_by(parent_post_id=self.id).all()

    def get_most_recent_reply(self):
        post = Post.query.filter_by(parent_post_id=self.id).order_by(desc('time_created')).first()
        if post is None:
            return self
        return post

    def get_author(self):
        return self.author.username

    def get_votes(self):
        return Upvote.query.filter_by(post_id=self.id, vote=1).count()

    def get_vote_status(self, user_id):
        """Return 1 for voted and 0 for not voted.

        If no vote exists then vote is 0.
        This uses integers rather than booleans because it makes math easier.
        """
        vote = Upvote.query.filter_by(post_id=self.id, user_id=user_id).first()
        try:
            return vote.vote
        except AttributeError:
            return 0
