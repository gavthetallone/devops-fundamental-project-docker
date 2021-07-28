from flask import url_for
from flask_testing import TestCase
from application import app, db
from application.models import Team, Player, League

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
            DEBUG=True,
            WTF_CSRF_ENABLED=False
        )
        return app

    def setUp(self):
        db.create_all()

        db.session.add(League(name="Run unit tests"))
        db.session.add(League(name="Do something else"))
        db.session.add(Team(description="Run unit tests", league_id=1))
        db.session.add(Player(name="Run unit tests", position="QB", active=True))

        db.session.commit()

    def tearDown(self):
        db.drop_all()

class TestViews(TestBase):
    def test_home(self):
        response = self.client.get(url_for("home"))
        self.assert200(response)
    
    def test_create_league(self):
        response = self.client.get(url_for("create_league"))
        self.assert200(response)
    
    def test_update_league(self):
        response = self.client.get(url_for("update_league", id=1))
        self.assert200(response)
    
    def test_create_team(self):
        response = self.client.get(url_for("create_team"))
        self.assert200(response)
    
    def test_update_team(self):
        response = self.client.get(url_for("update_team", id=1))
        self.assert200(response)
    
    def test_create_player(self):
        response = self.client.get(url_for("create_player"))
        self.assert200(response)

    def test_update_player(self):
        response = self.client.get(url_for("update_player", id=1))
        self.assert200(response)

class TestRead(TestBase):
    def test_home(self):
        response = self.client.get(url_for("home"))
        assert "Run unit tests" in response.data.decode()
        assert "Do something else" in response.data.decode()

class TestCreate(TestBase):
    def test_create_league(self):
        response = self.client.post(
            url_for("create_league"),
            data={"name" : "Check create is working"},
            follow_redirects=True
            )
        
        assert "Check create is working" in response.data.decode()

    def test_create_team(self):
        response = self.client.post(
            url_for("create_team"),
            data={"description" : "Example team",
                    "league_id" : 1},
            follow_redirects=True
            )
        
        assert Team.query.filter_by(description="Example team").first() != None
    
    def test_create_player(self):
        response = self.client.post(
            url_for("create_player"),
            data={"name" : "Example player",
                "position" : "QB",
                "team" : 1},
            follow_redirects=True
            )
        
        assert Player.query.filter_by(name="Example player").first() != None

class TestUpdate(TestBase):
    def test_update_league(self):
        response = self.client.post(
            url_for("update_league", id=1),
            data={"name" : "Check update is working"},
            follow_redirects=True
            )
        
        assert "Check update is working" in response.data.decode()
        assert "Do something else" in response.data.decode()
        assert "Check create is working" not in response.data.decode()

    def test_update_team(self):
        response = self.client.post(
            url_for("update_team", id=1),
            data={"description" : "Check update is working",
                    "league" : 1},
            follow_redirects=True
            )
        
        assert "Check update is working" in response.data.decode()
        assert "Do something else" in response.data.decode()
        assert "Example team" not in response.data.decode()

    def test_update_player(self):
        response = self.client.post(
            url_for("update_player", id=1),
            data={"name" : "Check update is working",
                    "position" : "QB",
                    "team" : 1},
            follow_redirects=True
            )
        
        assert "Check update is working" in response.data.decode()
        assert "Do something else" in response.data.decode()
        assert "Example player" not in response.data.decode()

    def test_inactive(self):
        response = self.client.get(
            url_for("inactive", id=1),
            follow_redirects=True
            )
        player = Player.query.get(1)
        assert player.active == False
    
    def test_active(self):
        response = self.client.get(
            url_for("active", id=1),
            follow_redirects=True
            )
        player = Player.query.get(1)
        assert player.active == True

class TestDelete(TestBase):
    def test_delete_league(self):
        response = self.client.get(
            url_for("delete_league", id=1),
            follow_redirects=True
            )

        assert "Do something else" in response.data.decode()
        assert "Check update is working" not in response.data.decode()
    
    def test_delete_team(self):
        response = self.client.get(
            url_for("delete_team", id=1),
            follow_redirects=True
            )

        assert "Do something else" in response.data.decode()
        assert "Check update is working" not in response.data.decode()

    def test_delete_player(self):
        response = self.client.get(
            url_for("delete_player", id=1),
            follow_redirects=True
            )

        assert "Do something else" in response.data.decode()
        assert "Check update is working" not in response.data.decode()
        
        