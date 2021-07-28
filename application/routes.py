from . import app, db
from .models import Player, Team, League
from .forms import TeamForm, PlayerForm, LeagueForm
from flask import redirect, url_for, request, render_template

@app.route("/")
def home():
    teams = Team.query.all()
    players = Player.query.all()
    leagues = League.query.all()

    return render_template("home.html", teams=teams, players=players, leagues=leagues)

@app.route("/create_league", methods=["GET", "POST"])
def create_league():
    form = LeagueForm()

    if request.method == "POST":
        new_league = League(
            name=form.name.data,
            )
        db.session.add(new_league)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("create_league.html", form=form)


@app.route("/create_team", methods=["GET", "POST"])
def create_team():
    form1 = LeagueForm()
    form2 = TeamForm()

    leagues = League.query.all()
    form2.league.choices = [(league.id, league.name) for league in leagues]

    if request.method == "POST":
        new_team = Team(
            description=form2.description.data,
            league_id=form2.league.data
            )
        db.session.add(new_team)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        return render_template("create_team.html", form=form2)

@app.route("/create_player", methods=["GET", "POST"])
def create_player():
    form1 = TeamForm()
    form2 = PlayerForm()

    teams = Team.query.all()
    form2.team.choices = [(team.id, team.description) for team in teams]

    if request.method == "POST":
        new_player = Player(name=form2.name.data, position=form2.position.data, team_id=form2.team.data)
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return render_template("create_player.html", form=form2)

@app.route("/update_league/<int:id>/", methods=["GET", "POST"])
def update_league(id):
    league = League.query.get(id)
    form = LeagueForm()

    if request.method == "POST":
        league.name = form.name.data
        db.session.add(league)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        form.name.data = league.name

    return render_template("create_league.html", form=form)



@app.route("/update_team/<int:id>/", methods=["GET", "POST"])
def update_team(id):
    team = Team.query.get(id)
    form1 = TeamForm()

    if request.method == "POST":
        team.description = form1.description.data
        team.league_id = form1.league.data
        db.session.add(team)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        leagues = League.query.all()
        form1.league.choices = [(league.id, league.name) for league in leagues]

        form1.description.data = team.description
        form1.league.data = team.league_id

        return render_template("create_team.html", form=form1)

@app.route("/update_player/<int:id>", methods=["GET", "POST"])
def update_player(id):
    player = Player.query.get(id)
    form2 = PlayerForm()

    teams = Team.query.all()
    form2.team.choices = [(team.id, team.description) for team in teams]

    if request.method == "POST":
        player.name = form2.name.data
        player.position = form2.position.data
        player.team_id = form2.team.data
        db.session.add(player)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        players = Player.query.all()
        form2.name.choices = [(player.id, player.team) for player in players]

        form2.name.data = player.name
        form2.position.data = player.position
        form2.team.data = player.team_id

        return render_template("create_player.html", form=form2)

@app.route("/delete_league/<int:id>")
def delete_league(id):
    league = League.query.get(id)
    db.session.delete(league)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/delete_team/<int:id>")
def delete_team(id):
    team = Team.query.get(id)
    db.session.delete(team)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/delete_player/<int:id>")
def delete_player(id):
    player = Player.query.get(id)
    db.session.delete(player)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/active/<int:id>")
def active(id):
    player = Player.query.get(id)
    player.active = True
    db.session.add(player)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/inactive/<int:id>")
def inactive(id):
    player = Player.query.get(id)
    player.active = False
    db.session.add(player)
    db.session.commit()

    return redirect(url_for("home"))

    