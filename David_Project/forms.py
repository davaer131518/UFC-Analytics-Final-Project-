from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError
from flask_wtf.file import FileField

class UFCForm(FlaskForm):

    fighter_1 = TextField("Fighter 1", render_kw={"placeholder": "Fighter 1"})
    fighter_2 = TextField("Fighter 2", render_kw={"placeholder": "Fighter 2"})

    result = TextAreaField("Predicted Results", render_kw={"placeholder": "Fighter 1 wins with x% \nFighter 2 wins with y%"})


    message = TextAreaField("Comments", render_kw={"placeholder": "Please Write your comment here in the following format. \n Incorrect Result \n Proceed with a detailed message"})

    upload = SubmitField("Predict")
