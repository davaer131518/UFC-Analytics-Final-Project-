import os
import requests
import pickle
import json
import config
import traceback
from flask import Flask, render_template,request,flash
from forms import UFCForm
from flask_mail import Message, Mail
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, patch_request_class



base_host_name = config.BASE_HOST_NAME

mail = Mail()
app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = config.SECRET_KEY

app.config['DEBUG'] = config.DEBUG
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD

app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.config['UPLOADS_DEFAULT_DEST'] = config.UPLOADS_DEFAULT_DEST

ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS

cv_set = UploadSet('cv', ALLOWED_EXTENSIONS)
configure_uploads(app, cv_set)
patch_request_class(app)  # set maximum file size, default is 16MB

mail.init_app(app)


def load_pickle(file_path):
    with open(file_path, "rb") as f:
        obj = pickle.load(f)
    return obj

prof_perf = load_pickle("prof_perf.pkl")
fights_name = load_pickle("fighter_stats.pkl")
clf = load_pickle("clf.pkl")

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/ufc1v1', methods=['GET', 'POST'])
def upload():
    form = UFCForm()
    try:

        if request.method == 'POST':
            if form.validate() == False:
                flash('All f-ields are required.')
                return render_template('upload.html', form=form)
            else:

                if form.upload.data:
                    ufc_result = predict_winner(form.fighter_1.data,form.fighter_2.data)
                    form.result.data = str(ufc_result)

                    return render_template('upload.html', success=True,  form = form)
                else:
                     return render_template('upload.html', form=form)


        elif request.method == 'GET':
            return render_template('upload.html', form=form)

    except Exception as e:
        print(traceback.format_exc())
        return render_template('upload.html', form=form)





def predict_winner(name_1, name_2):
    try:
        row = list(prof_perf.loc[name_1.lower()].values) + list(prof_perf.loc[name_2.lower()].values)


        score = clf.predict([row])
        confdence = clf.predict_proba([row])[0]
        print(score)


        confidence_parag = "\n The Net Predicts that \n {} has {} prob to win \n{} has {} prob to win".format(name_1,confdence[1],name_2,confdence[0])

        if confdence[1] >0.7:

            statement = "The winner is " + name_1

        elif confdence[0] > 0.7:

            statement = "The winner is " + name_2
        else:
            statement = "This seems like a close fight"

    except Exception as e:
        return "Error Encountered: Maybe one of the fighter names is wrong ?"


    return statement + '\n' + confidence_parag



if __name__ == '__main__':
    app.run(debug=True)
