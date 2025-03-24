from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired

class InputForm(FlaskForm):
    # I cannot use list for this WTF stuff, I would if I could
    input = StringField(label="", validators=[DataRequired()])
    input_comparison_1 = StringField(label="")
    input_comparison_2 = StringField(label="")
    input_comparison_3 = StringField(label="")
    submit = SubmitField("Submit")
