from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from wtforms.validators import DataRequired, optional

class SummonerForm(FlaskForm):
    summoner = StringField('Summoner', validators=[DataRequired()])
    region = SelectField('Region', choices=[("euw1","EUW"),("eun1","EUNE"),("tr1","TR"),("na1","NA"),("br1","BR"),("ru","RU"),("la2","LAS"),("la1","LAN"),("oc1","OCE"),("kr","KR"),("jp","JP")])