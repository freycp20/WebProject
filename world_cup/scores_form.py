from flask_wtf import FlaskForm
from wtforms.fields import IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange

class ScoresForm(FlaskForm):
    # add fields with validators for homeScore and awayScore
    homeScore = IntegerField("Home Team Score", validators=[NumberRange(0, 1000, message="Score must be a valid score"), InputRequired(message="Home Team Score is Required")])
    awayScore  = IntegerField("Away Team Score", validators=[NumberRange(0, 1000, message="Score must be a valid score"), InputRequired(message="Away Team Score is Required")])
    submit = SubmitField("Submit")
    id = IntegerField("id")