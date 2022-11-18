from flask_wtf import FlaskForm
from wtforms.fields import IntegerField, SubmitField, HiddenField
from wtforms.validators import InputRequired, NumberRange, Optional

class ScoresForm(FlaskForm):
    # add fields with validators for homeScore and awayScore
    homeScore = IntegerField("Home Team Score", validators=[NumberRange(-1, 1000, message="Score must be a valid score"), Optional()])
    awayScore  = IntegerField("Away Team Score", validators=[NumberRange(-1, 1000, message="Score must be a valid score"), Optional()])
    match_id = HiddenField("id", validators=[])
    submit = SubmitField("Submit")