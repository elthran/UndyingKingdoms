from extensions import flask_db as db
from undyingkingdoms.models.bases import GameEvent


class Forum(GameEvent):
    threads = db.relationship('Thread', backref='forum')

    def __init__(self):
        pass


class Thread(GameEvent):
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)
    posts = db.relationship('Post', backref='thread')
    title = db.Column(db.String(16))

    def __init__(self, title="New Thread"):
        self.title = title
        
        
class Post(GameEvent):
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    title = db.Column(db.String(16))
    content = db.Column(db.String(16))
    user_id = db.Column(db.Integer)

    def __init__(self, title, content):
        self.title = title
        self.content = content
