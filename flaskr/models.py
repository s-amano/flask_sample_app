from flaskr import db

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    publisher = db.Column(db.Text)

    def __repr__(self):
        return '<Book id={id} title={title!r}>'.format(
                id=self.id, title=self.title)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return u'<User id={self.id} user_name={self.user_name!r}>'.format(
            self=self)


def init():
    db.create_all()