from test_app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(128))
    birth_date= db.Column(db.Date, nullable=True)

    def __repr__(self):
        return '<User id:{}>\n'.format(self.id)
