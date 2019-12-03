from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from wtforms.validators import DataRequired, optional

class SummonerForm(FlaskForm):
    summoner = StringField('Summoner', validators=[DataRequired()])
    region = StringField('Region', validators=[DataRequired()])