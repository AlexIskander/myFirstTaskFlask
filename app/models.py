from app import db

class User(db.Model ):
    id       = db.Column(db.Integer, primary_key=True)
    login    = db.Column(db.String(80), unique=True)
    email    = db.Column(db.String(120))
    password = db.Column(db.String(64))
    
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.login)


class Question(db.Model):
    id        = db.Column(db.Integer, primary_key = True)
    text      = db.Column(db.String(240))
    timestamp = db.Column(db.DateTime)
    user_id   = db.Column(db.String)

    def __repr__(self):
        return '<Post %r>' % (self.text)


class Answer(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    text_answer = db.Column(db.String(240))
    timestamp   = db.Column(db.DateTime)
    user_id     = db.Column(db.String)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    vote        = db.Column(db.Integer)

    def __repr__(self):
        return '<Post %r>' % (self.text_answer)

