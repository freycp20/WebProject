"""
INSTALLING REQUIRED PACKAGES
Run the following two commands to install all required packages.
python -m pip install --upgrade pip
python -m pip install --upgrade flask-login
"""

###############################################################################
# Imports
###############################################################################
import json

import os
import sys
from flask import Flask, render_template, url_for, redirect
from flask import request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required
from flask_login import login_user, logout_user, current_user
from datetime import datetime
# from sqlalchemy import or_

# Make sure this directory is in your Python path for imports
scriptdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(scriptdir)

# Import from local package files
from hashing_examples import UpdatedHasher
from loginforms import RegisterForm, LoginForm

###############################################################################
# Basic Configuration
###############################################################################

# Identify necessary files
dbfile = os.path.join(scriptdir, "users.sqlite3")
pepfile = os.path.join(scriptdir, "pepper.bin")

# date = datetime.now()
date = datetime(2022,11,27)

# open and read the contents of the pepper file into your pepper key
# NOTE: you should really generate your own and not use the one from the starter
with open(pepfile, 'rb') as fin:
  pepper_key = fin.read()

# create a new instance of UpdatedHasher using that pepper key
pwd_hasher = UpdatedHasher(pepper_key)

admin_key = "iamanadmin"
# Configure the Flask Application
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'correcthorsebatterystaple'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Getting the database object handle from the app
db = SQLAlchemy(app)

# Prepare and connect the LoginManager to this app
app.login_manager = LoginManager()
app.login_manager.login_view = 'get_login'
@app.login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

###############################################################################
# Database Setup
###############################################################################

# Create a database model for Users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode, nullable=False)
    password_hash = db.Column(db.LargeBinary) # hash is a binary attribute
    admin_status = db.Column(db.Integer)
    score = db.Column(db.Integer)
    bracket = db.Column(db.Unicode)
    # make a write-only password property that just updates the stored hash
    @property
    def password(self):
        raise AttributeError("password is a write-only attribute")
    @password.setter
    def password(self, pwd):
        self.password_hash = pwd_hasher.hash(pwd)
    
    @property
    def admin(self):
        raise AttributeError("admin is a write-only attribute")
    @admin.setter
    def admin(self, key):
        if key == admin_key:
            self.admin_status = 1
        else:
            self.admin_status = 0
        # self.admin = 1 if key == admin_key else 0
    
    # add a verify_password convenience method
    def verify_password(self, pwd):
        return pwd_hasher.check(pwd, self.password_hash)

# Define the game data
class Stadium(db.Model):
    __tablename__ = 'Stadiums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    matches = db.relationship('Match', backref='stadiumObj')
    # Stadium is a foreign key in another table
    
    def __str__(self):
        return f"Stadium({self.id})"
    def __repr__(self):
        return f"Stadium({self.id})"

class Team(db.Model):
    __tablename__ = 'Teams'
    id = id = db.Column(db.Integer, primary_key=True)
    alpha_2 = db.Column(db.Unicode, nullable=False)
    alpha_3 = db.Column(db.Unicode, nullable=False)
    name = db.Column(db.Unicode, nullable=False)
    official_name = db.Column(db.Unicode, nullable=False)
    primary_colors = db.Column(db.Unicode, nullable=False)
    secondary_colors = db.Column(db.Unicode, nullable=False)
    home_team = db.relationship('Match', backref='home_team', foreign_keys="Match.home_id")
    away_team = db.relationship('Match', backref='away_team', foreign_keys="Match.away_id")
    # Team is a foreign key in another table
    
    def __str__(self):
        return f"Team({self.id})"
    def __repr__(self):
        return f"Team({self.id})"

class Match(db.Model):
    __tablename__ = 'Matches'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text, nullable=False)
    group = db.Column(db.Unicode, nullable=False)
    # Stadium and teams are other tables
    stadium = db.Column(db.Integer, db.ForeignKey("Stadiums.id"))
    home_id = db.Column(db.Integer, db.ForeignKey("Teams.id"))
    away_id = db.Column(db.Integer, db.ForeignKey("Teams.id"))
    score_home = db.Column(db.Integer, nullable=True)
    score_away = db.Column(db.Integer, nullable=True)
    
    def __str__(self):
        return f"Match({self.home_id} vs {self.away_id})"
    def __repr__(self):
        return f"Match({self.id})"

with app.app_context():
    # db.drop_all()
    db.create_all() # this is only needed if the database doesn't already exist

from scores_form import ScoresForm

###############################################################################
# Route Handlers
###############################################################################
@app.get('/input-scores/')
def get_input_scores():
    form = ScoresForm()
    matches = Match.query.order_by(Match.date).all()
    for match in matches:
        match.date = datetime.strptime(match.date, "%Y-%m-%d %H:%M:%S.%f")
    return render_template("input_scores.html", form=form, matches=matches, current_user=current_user)

@app.post('/input-scores/')
def post_input_scores():
    form = ScoresForm()
    if form.validate():
        # form data is valid, add it to authors and redirect
        match = db.session.query(Match).filter_by(id=int(form.match_id.data)).first()
        try:
            if form.homeScore.data == None and form.awayScore.data == None:
                match.score_home = None
                match.score_away = None
                db.session.add(match)
                db.session.commit()
            if form.homeScore.data != None and form.awayScore.data != None:
                match.score_home = form.homeScore.data
                match.score_away = form.awayScore.data
                db.session.add(match)
                db.session.commit()
            else:
                flash(f"Score could not be none!")
                # reload new form
                return redirect(url_for('get_input_scores'))
        except:
            flash(f"Score could not be input!")
            # reload new form
            return redirect(url_for('get_input_scores'))
        update_all_users_scores()
        flash(f"Score was updated successfully!")
        return redirect(url_for('get_input_scores'))
    else:
        # flash an error messages for all errors
        for field, error in form.errors.items():
            flash(f"Error! {' '.join(error)}")

        # reload new form
        return redirect(url_for('get_input_scores'))


@app.get('/create-bracket/')
@login_required
def get_create_bracket():
    # teams = Team.query.all()
    # matches = Match.query.order_by(Match.date).all()
    
    start_date = datetime(2022,12,3)
    end_date = datetime(2022, 12,7)
    #nov 27
    
    # date = datetime.now()

    matches = Match.query.filter(Match.date >= start_date).filter(Match.date <= end_date).all()
    for match in matches:
        match.date = datetime.strptime(match.date, "%Y-%m-%d %H:%M:%S.%f")
        print(match.id)
        print(match.date)

    print(matches)

    matches[5], matches[6] = matches[6], matches[5]
    print(matches)

    filtered_matches = []
    existing_teams = []
    for i in range(8):
        ht = matches[i].home_team
        at = matches[i].away_team
        if ht not in existing_teams and at not in existing_teams:
            existing_teams.append(ht)
            existing_teams.append(at)
            filtered_matches.append(matches[i])
    return render_template('create_bracket.html', current_user=current_user, matches=filtered_matches)

@app.post('/create-bracket/')
@login_required
def post_create_bracket():
    # print(request.data)
    data = request.data.decode('utf-8')
    user = db.session.query(User).filter_by(id=int(current_user.id)).first()
    user.bracket = data
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("get_view_bracket"))

def update_all_users_scores():
    users = User.query.all()
    for user in users:
        update_user_scores(user)

def update_user_scores(user):
    bracket = user.bracket
    user_score = 0
    if bracket != None:
        bracket = json.loads(bracket).get("input_labels")
        matches = 8
        skip_index = 0
        for i in range(4):
            for j in range(matches):
                print(matches)
                print(skip_index)
                # print(matches)
                home_team = bracket[skip_index + j*2]
                away_team = bracket[skip_index + j*2 + 1]
                n = [home_team["team_name"], away_team["team_name"]]
                date = datetime(2022,12,3)
                match = Match.query.filter(Match.date > date).filter((Match.home_team.has(name=n[0]) | Match.home_team.has(name=n[1])) & (Match.away_team.has(name=n[0]) | Match.away_team.has(name=n[1]))).first()
                 
                chosen = home_team if home_team["checked"] else away_team
                not_chosen = home_team if away_team["checked"] else away_team
                checked = chosen["team_name"]
                
                if match:
                    print(match)
                    winning_team = None
                    if match.score_home != None and match.score_away != None:
                        if match.score_home > match.score_away:
                            winning_team = match.home_team.name
                            home_team["won"] = True
                            away_team["won"] = False
                        elif match.score_home < match.score_away:
                            winning_team = match.away_team.name
                            away_team["won"] = True
                            home_team["won"] = False
                    if winning_team != None:
                        if winning_team == checked:
                            chosen["correct"] = True
                            print("CORRECT CHOICE")
                            user_score += 1
                        else:
                            chosen["correct"] = False
                print(home_team)
                print(away_team)

                print("\n\n")
            skip_index += matches*2
            matches //=2
        
        user.score = user_score
        db.session.commit()
    return user_score, bracket

@app.get('/view-bracket/')
@login_required
def get_view_bracket():
    user_score, bracket = update_user_scores(current_user)
    print(bracket)
    return render_template("view_bracket.html", current_user=current_user, bracket=bracket, score=user_score)

@app.get('/register/')
def get_register():
    form = RegisterForm()
    return render_template('register.html', form=form)

@app.post('/register/')
def post_register():
    form = RegisterForm()
    if form.validate():
        # check if there is already a user with this email address
        user = User.query.filter_by(email=form.email.data).first()
        # if the email address is free, create a new user and send to login
        if user is None:
            user = User(email=form.email.data, password=form.password.data, admin=form.admin_key.data, score=0)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('get_login'))
        else: # if the user already exists
            # flash a warning message and redirect to get registration form
            flash('There is already an account with that email address')
            return redirect(url_for('get_register'))
    else: # if the form was invalid
        # flash error messages and redirect to get registration form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register'))

@app.get('/login/')
def get_login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.post('/login/')
def post_login():
    form = LoginForm()
    if form.validate():
        # try to get the user associated with this email address
        user = User.query.filter_by(email=form.email.data).first()
        # if this user exists and the password matches
        if user is not None and user.verify_password(form.password.data):
            # log this user in through the login_manager
            login_user(user)
            # redirect the user to the page they wanted or the home page
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('index')
            return redirect(next)
        else: # if the user does not exist or the password is incorrect
            # flash an error message and redirect to login form
            flash('Invalid email address or password')
            return redirect(url_for('get_login'))
    else: # if the form was invalid
        # flash error messages and redirect to get login form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_login'))

@app.get('/')
def index():
    #matches = Match.query.order_by(Match.date).all()
    #nov 27
    

    matches = Match.query.filter(Match.date > date).order_by(Match.date).all()
    for match in matches:
        match.date = datetime.strptime(match.date, "%Y-%m-%d %H:%M:%S.%f")
    teams = Team.query.all()
    #do a select statement for matches that takes the matches > current date
    #for prev games - do another query where filter where matches < current date
    prevGames = Match.query.filter(Match.date < date).order_by(Match.date).all()
    for match in prevGames:
        match.date = datetime.strptime(match.date, "%Y-%m-%d %H:%M:%S.%f")
    #matches[1:] - shows matches from current and on (in html)
    leaderBoardScores = User.query.order_by(User.score.desc()).all()
    return render_template('schedule.html', current_user=current_user, matches=matches, teams=teams, prevGames = prevGames[-2:], leaderBoardScores=leaderBoardScores)

@app.get('/match/<int:match_id>/')
def get_matches(match_id):
    # match.home_team-match.away_team
    #senegal-netherlands
    #/match/senegal-netherlands/
    # presentDate = datetime(year=2022, month=11, day=27)
    presentDate = date
    # match = Match.query.all()[0]
    print(match_id)
    match = Match.query.filter(Match.id == match_id).first()
    print(match)
    if match.score_home == None or match.score_away == None:
        match.score_home = -1
        match.score_away = -1
    match_date_as_date = datetime.strptime(match.date, "%Y-%m-%d %H:%M:%S.%f")
    return render_template("match.html", match=match, current_user=current_user, presentDate=presentDate, match_date=match_date_as_date)

@app.get('/logout/')
@login_required
def get_logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.get('/get-user-scores/')
def return_scores():
    # return a json containing all the user scores
    # print()
    # leaderBoardScores = User.query.order_by(User.score.asc()).all()
    users_scores = {}

    for user in User.query.all():
        # print(user.email)
        users_scores[f"{user.email}"] = user.score

    # print(users_scores)
    return users_scores
    # return {"admin@admin.com":10,"eraine2121@gmail.com":1,"fdfsdfm@hotmail.org":51,"freycp20@gcc.edu":2,"freycp2@gcc.edu":6,"test@gmail.com":16}
