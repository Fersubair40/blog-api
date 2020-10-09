import datetime
from . import db, bcrypt


class BlogpostModel(db.Model):

    __tablename__ = 'blogposts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("UserModel")

    def __init__(self, data):
        self.title = data.get("title")
        self.contents = data.get("contents")
        self.user_id = data.get("user_id")
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def json(self):
        return {
            "title": self.title,
            "contents": self.contents,
            "user_id": self.user_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_blogposts():
        return BlogpostModel.query.all()

    @staticmethod
    def get_blogposts_by_id(id):
        return BlogpostModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)