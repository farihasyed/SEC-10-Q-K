from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired

STOCKS = [('', 'Company'), ('AAPL', 'AAPL'), ('GOOG', 'GOOG'), ('AMZN', 'AMZN'), ('FB', 'FB'), ('MSFT', 'MSFT')]


class Index(FlaskForm):
    company = SelectField('Company', choices=STOCKS, validators=[InputRequired()])
    submit = SubmitField()
