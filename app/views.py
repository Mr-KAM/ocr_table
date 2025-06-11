from flask import url_for, redirect, render_template, flash, g, session, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm
from app.forms import *
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form = RegisterForm()
        if form.validate_on_submit() and form.password.data==form.confirm_password.data:
            try :
                user = User(username=form.user.data, email=form.email.data, name=form.name.data, telephone=form.telephone.data)
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Votre compte a été créé avec succès !', 'success')
                return redirect(url_for('login'))
            except :
                flash("Erreur lors de la création de votre compte ! Email ou nom d'utilisateur dejà utilisé","error")
        else :
            flash("Cet utilisateur existe déjà !","warning")
    return render_template('signup.html', form=form, title="signup")




@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email=request.form["username"]
        print(request.form["username"])
        password=request.form["password"]
        # print(email)
        user = User.query.filter_by(email=email).first()
        print(user.check_password(password))
        if user and user.check_password(password):
             login_user(user)
             return redirect(url_for("index"))
             

    return render_template('login.html',
        title = 'login')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    if current_user.is_authenticated:
	    return render_template('index.html',title="Accueil")
    else :
        return redirect(url_for('login'))


@app.route('/list/')
def posts():
	return render_template('list.html')


@app.route('/new/')
@login_required
def new():
	form = ExampleForm()
	return render_template('new.html', form=form)


@app.route('/save/', methods = ['GET','POST'])
@login_required
def save():
	form = ExampleForm()
	if form.validate_on_submit():
		print("salvando os dados:")
		print(form.title.data)
		print(form.content.data)
		print(form.date.data)
		flash('Dados salvos!')
	return render_template('new.html', form=form)

@app.route('/view/<id>/')
def view(id):
	return render_template('view.html')

# === User login methods ===

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))




# ====================
