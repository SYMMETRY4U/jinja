# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, DecimalField, validators

from wtforms.validators import InputRequired

#RECIPE ADD FORM
class RecipeAdd(FlaskForm):
  name = StringField('Recipe Name', validators=[InputRequired()])
  author = StringField('Author')
  description = TextAreaField('Description')
  ingredients = TextAreaField('Ingredients', validators=[InputRequired()])
  instructions = TextAreaField('Instructions', validators=[InputRequired()])
  rating = FloatField('Rating')
  category_id = SelectField('Category', coerce=int, validators=[InputRequired()])

#RECIPE EDIT FORM
class RecipeEdit(FlaskForm):
    name = StringField('Recipe Name', validators=[validators.DataRequired()])
    description = TextAreaField('Description', validators=[validators.DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[validators.DataRequired()])
    instructions = TextAreaField('Instructions', validators=[validators.DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[validators.DataRequired()])
    rating = DecimalField('Rating', validators=[validators.NumberRange(min=0, max=5)])