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
    date = db.Column(db.Date, nullable=False)
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
    matches = Match.query.all()
    return render_template("input_scores.html", form=form, matches=matches, current_user=current_user)

@app.post('/input-scores/')
def post_input_scores():
    form = ScoresForm()
    if form.validate():
        # form data is valid, add it to authors and redirect
        match = db.session.query(Match).filter_by(id=int(form.match_id.data)).first()
        try:
            if form.homeScore.data == -1 and form.awayScore.data == -1:
                match.score_home = None
                match.score_away = None
                db.session.add(match)
                db.session.commit()
            if form.homeScore.data != -1 and form.awayScore.data != -1:
                match.score_home = form.homeScore.data
                match.score_away = form.awayScore.data
                db.session.add(match)
                db.session.commit()
            else:
                flash(f"Score could not be negative!")
                # reload new form
                return redirect(url_for('get_input_scores'))
        except:
            flash(f"Score could not be input!")
            # reload new form
            return redirect(url_for('get_input_scores'))

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
    matches = Match.query.all()
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

@app.get('/view-bracket/')
@login_required
def get_view_bracket():
    bracket = current_user.bracket
    if bracket != None:
        bracket = json.loads(bracket).get("input_labels")

    return render_template("view_bracket.html", current_user=current_user, bracket=bracket)

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
            user = User(email=form.email.data, password=form.password.data, admin=form.admin_key.data)
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
    matches = Match.query.all()
    teams = Team.query.all()
    return render_template('schedule.html', current_user=current_user, matches=matches, teams=teams)

@app.get('/logout/')
@login_required
def get_logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))
