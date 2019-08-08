from test_app.extensions import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text(), nullable=True)
    alias = db.Column(db.String(100))

    def __repr__(self):
        return '<Post id:{}>\n'.format(self.id)
