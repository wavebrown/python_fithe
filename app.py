from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField, StringField
from wtforms.validators import NumberRange
import pandas as pd
from tensorflow.keras.models import load_model
import joblib


def return_prediction(model, scaler, sample_json):
    test_sex = sample_json['test_sex']
    height = sample_json['height']
    weight = sample_json['weight']
    # fat = sample_json['fat']
    core_cm = sample_json['core_cm']
    situp = sample_json['situp']
    sitflex = sample_json['sitflex']
    longrun = sample_json['longrun']
    run10m = sample_json['run10m']
    longjump = sample_json['longjump']

    test_data = [[test_sex, height, weight, core_cm, situp, sitflex, longrun, run10m, longjump]]
    # scaler를 불러와서 scaling
    test_data_scaled = scaler.transform(test_data)

    # 예측값 생성
    predict = model.predict(test_data_scaled)

    return str(round(predict[0][0], 3))

app = Flask(__name__)
# Configure a secret SECRET_KEY
app.config['SECRET_KEY'] = 'someRandomKey'
F_modelage = load_model("model/F_model_age.h5")
M_modelage = load_model("model/M_model_age.h5")
F_scalerage = joblib.load("model/F_scaler_age.pkl")
M_scalerage = joblib.load("model/M_scaler_age.pkl")
F_model = load_model("model/F_model_bodyf.h5")
M_model = load_model("model/M_model_bodyf.h5")
F_scaler = joblib.load("model/F_scaler_bodyf.pkl")
M_scaler = joblib.load("model/M_scaler_bodyf.pkl")
median = pd.read_pickle("model/median.pkl")
# Loading the model and scaler
# adult_model = load_model("F_model_1208.h5")
# adult_scaler = joblib.load("F_scaler_1208.pkl")

class GreetUserForm(FlaskForm):
    test_sex = TextField('성별')
    height = TextField('키')
    weight = TextField('몸무게')
    # fat = TextField('체지방율')
    core_cm = TextField('허리둘레')
    situp = TextField('교차윗몸일으키기')
    sitflex = TextField('앉아윗몸앞으로굽히기')
    longrun = TextField('20m왕복오래달리기')
    run10m = TextField('10M4회왕복달리기')
    longjump = TextField('제자리멀리뛰기')

    submit = SubmitField("분석하기")

@app.route('/', methods=('GET', 'POST'))
def index():
    form = GreetUserForm()
    if form.validate_on_submit():
        session['test_sex'] = form.test_sex.data
        session['height'] = form.height.data
        session['weight'] = form.weight.data
        # session['fat'] = form.fat.data
        session['core_cm'] = form.core_cm.data
        print(form.test_sex.data)
        print(form.height.data)
        print(form.weight.data)


        return redirect(url_for("update"))
    return render_template('survey_form.html', form=form)

@app.route('/update', methods=('POST','GET'))
def update():
    print(session);
    content1 ={}

    content1['test_sex'] = session['test_sex']
    content1['height'] =  session['height']
    content1['weight'] = session['weight']
    content1['core_cm'] = session['core_cm']

    print(content1);
    return render_template('sUpdateForm.html', content1=content1)

@app.route('/prediction', methods=('POST','GET'))
def prediction():
    form = GreetUserForm();
    print(form.situp.data);
    print(form.sitflex.data);
    content = {}

    content['test_sex'] = int(session['test_sex'])
    content['height'] = int(session['height'])
    content['weight'] = int(session['weight'])
    content['core_cm'] = int(session['core_cm'])
    content['situp'] = int(form.situp.data)
    content['sitflex'] = int(form.sitflex.data)
    content['longrun'] = int(form.longrun.data)
    content['run10m'] = int(form.run10m.data)
    content['longjump'] = int(form.longjump.data) / 10

    print(content)
    if(content['test_sex'] == 0):
        results_age = return_prediction(model=F_modelage,scaler=F_scalerage,sample_json=content)
        results_body = return_prediction(model=F_model, scaler=F_scaler, sample_json=content)
        gender = "남성" #--------------------------------------------------------------------#
        print(gender)
    elif (content['test_sex'] == 1):
        results_age = return_prediction(model=M_modelage, scaler=M_scalerage, sample_json=content)
        print("results_age", results_age)
        results_body = return_prediction(model=F_model, scaler=F_scaler, sample_json=content)
        gender = "여성" #--------------------------------------------------------------------#
        print(gender)


    # pivot data select
    group_label = str(session['test_sex'])
    # pivot_select = pd.DataFrame(group.loc[group_label]).T
    pivot_select = median
    if float(session['test_sex']) > 0.5:
        pivot_col = [pivot_select.columns[0][0], pivot_select.columns[1][0], pivot_select.columns[2][0],
                     pivot_select.columns[3][0],pivot_select.columns[4][0]]
        print("pivot_col",pivot_col)
        pivot_data = [pivot_select.iloc[1, 0], pivot_select.iloc[1, 1], pivot_select.iloc[1, 2],
                      pivot_select.iloc[1, 3],pivot_select.iloc[1, 4]]
        print("pivot_data",pivot_data)
    else:
        pivot_col = [pivot_select.columns[0][0], pivot_select.columns[1][0], pivot_select.columns[2][0],
                     pivot_select.columns[3][0], pivot_select.columns[4][0]]

        pivot_data = [pivot_select.iloc[0, 0], pivot_select.iloc[0, 1], pivot_select.iloc[0, 2],
                      pivot_select.iloc[0, 3], pivot_select.iloc[0, 4]]



    # 예측 결과 리턴
    return render_template('prediction.html', results_age=results_age,results_body=results_body, pivot_col=pivot_col,
                           pivot_data=pivot_data,content=content, gender=gender)




if __name__ == '__main__':
    app.run(debug=True)