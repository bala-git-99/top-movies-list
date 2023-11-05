from flask import render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

from db_operations import *

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class UpdateForm(FlaskForm):
    rating = FloatField('Your Rating Our of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')


class AddForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


@app.route("/")
def home():
    movies = select_all()
    return render_template("index.html", movies=movies)


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    form = UpdateForm()
    if request.method == 'GET':
        return render_template("edit.html", movie=select(id), form=form)
    else:
        update_movie(id, form.rating.data, form.review.data)
        return redirect(url_for('home'))


@app.route("/delete/<int:id>")
def delete(id):
    delete_movie(id)
    return redirect(url_for('home'))


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        movies = get_movie(form.title.data)
        return render_template("select.html", movies=movies)
    return render_template("add.html", form=form)


@app.route("/find/<int:id>")
def find(id):
    add_movie(id)
    return redirect(url_for("update", id=id))


if __name__ == '__main__':
    app.run(debug=True)
