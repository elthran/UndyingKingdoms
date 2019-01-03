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

    def __init__(self, forum_id, title="New Thread"):
        self.forum_id = forum_id
        self.title = title
        
    def get_post_count(self):
        return len(self.posts)
    
    def get_most_recent_post(self):
        post = Post.query.filter_by(thread_id=self.id).order_by(desc('time_created')).first()
        return post.time_created
        
        
class Post(GameEvent):
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    title = db.Column(db.String(16))
    content = db.Column(db.String(16))
    user_id = db.Column(db.Integer)

    def __init__(self, thread_id, title, content):
        self.thread_id = thread_id
        self.title = title
        self.content = content
