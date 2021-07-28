from . import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    players = db.relationship('Player', backref="team")
    league_id = db.Column(db.Integer, db.ForeignKey("league.id"))

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(10), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))

class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    teams = db.relationship('Team', backref="league")