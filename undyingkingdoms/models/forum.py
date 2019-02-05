from sqlalchemy import desc

from extensions import flask_db as db
from undyingkingdoms.models.bases import GameEvent
from undyingkingdoms.models.upvotes import Upvote
from undyingkingdoms.models.users import User


class Forum(GameEvent):
    threads = db.relationship('Thread', backref='forum')

    def __init__(self):
        pass


class Thread(GameEvent):
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)
    posts = db.relationship('Post', backref='thread')
    title = db.Column(db.String(32))
    author_id = db.Column(db.Integer)

    def __init__(self, forum_id, title, author_id):
        self.forum_id = forum_id
        self.title = title
        self.author_id = author_id
        
    def get_post_count(self):
        return len(self.posts)
    
    def get_most_recent_post(self):
        return Post.query.filter_by(thread_id=self.id).order_by(desc('time_created')).first()

    def get_author(self):
        author = User.query.filter_by(id=self.author_id).first()
        return author.username
        
        
class Post(GameEvent):
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    parent_post_id = db.Column(db.Integer)  # 0 if this is the parent
    title = db.Column(db.String(32))
    content = db.Column(db.String(5000))
    author_id = db.Column(db.Integer)
    votes = db.Column(db.Integer)

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
        author = User.query.filter_by(id=self.author_id).first()
        return author.username

    def get_votes(self):
        votes = Upvote.query.filter_by(post_id=self.id, vote=1).all()
        return len(votes)

    def get_vote_status(self, user_id):
        vote = Upvote.query.filter_by(post_id=self.id, user_id=user_id).first()
        if vote:
            return 1 - vote.vote
        else:
            return 1
