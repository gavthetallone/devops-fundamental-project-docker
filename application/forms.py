from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

class TeamForm(FlaskForm):
    description = StringField("What is the team?")
    league = SelectField("What is the league?", choices=[])
    submit = SubmitField("Submit")

class PlayerForm(FlaskForm):
    name = StringField("Who is the player?")
    position = SelectField("Which position?", choices=["QB", "RB", "WR", "TE", "K", "DEF"])
    team = SelectField("Choose a team", choices=[])
    submit = SubmitField("Submit")

class LeagueForm(FlaskForm):
    name = StringField("What is the league?")
    submit = SubmitField("Submit")