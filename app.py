from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo, NumberRange

import requests

app = Flask(__name__)
app.secret_key = "eflwsrkmksj82398reyd0873eirds0923kjo83r7iwerwed"

class RegisterForm(Form):
    Name = StringField('Name', validators= [InputRequired()], render_kw={"placeholder":"Name","autocomplete":"off"})
    Email = StringField('Email', validators = [InputRequired(), Email(message='Invalid email')], render_kw={"placeholder":"Email","autocomplete":"off"})    
    Phone = IntegerField('Phone', validators = [InputRequired()], render_kw={"placeholder":"Phone","autocomplete":"off"})
    Password = PasswordField('Password', validators = [ InputRequired(), Length(min = 6, max = 30, message = 'Password length must be atleast 6'), EqualTo('Confirm', message = "Passwords must match")], render_kw={"placeholder":"Password","autocomplete":"off"})
    Confirm = PasswordField('Confirm Password', render_kw={"placeholder":"Confirm Password","autocomplete":"off"})

@app.route('/',methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        payload = {
                'name':form.Name.data,
                'email':form.Email.data,
                'phone':form.Phone.data,
                'password':form.Password.data,
                'confirm_password':form.Confirm.data
                
            }
        data = {
            'name':form.Name.data,
            'email':form.Email.data,
            'password':form.Password.data,
            'returnSecureToken': True

        }
 
        session=requests.Session()
        session.post('https://ucsp-quiz.herokuapp.com/register',data=payload)
        session.post('https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=AIzaSyDpKtHKmbF-Ctvyno1OtpoJJOktnrCx8g4',data=data)

        flash(" Dear {}, your registration was successful!".format(form.Name.data),"message") 
        return redirect(url_for('inst'))

    return render_template('register.html', form=form)

@app.route('/inst')
def inst():
    return render_template('inst.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
    

