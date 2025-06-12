from flask import url_for, redirect, render_template, flash, g, session, request,jsonify
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

@app.route('/gemini')
def gemini():
    if current_user.is_authenticated:
	    return render_template('gemini.html',title="Accueil2")
    else :
        return redirect(url_for('login'))
    
@app.route('/extraction')
def extraction():
    if current_user.is_authenticated:
	    return render_template('extraction.html',title="Accueil3")
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

# @app.route('/api/notes', methods=['POST'])
# def enregistrer_notes():
#     try:
#         data = request.get_json()

#         # S'assurer que c'est une liste
#         if isinstance(data, dict):
#             data = [data]

#         notes_avec_moyenne = [n for n in data if n.get('moyenne') is not None]
#         notes_sans_moyenne = [n for n in data if n.get('moyenne') is None]

#         # Trier par moyenne décroissante
#         notes_avec_moyenne.sort(key=lambda n: n['moyenne'], reverse=True)

#         # Calcul du rang
#         rang = 1
#         for i, note in enumerate(notes_avec_moyenne):
#             if i > 0 and note['moyenne'] == notes_avec_moyenne[i - 1]['moyenne']:
#                 note['rang_matiere'] = notes_avec_moyenne[i - 1]['rang_matiere']
#             else:
#                 note['rang_matiere'] = rang
#             rang += 1

#         # Fusionner les deux listes
#         toutes_les_notes = notes_avec_moyenne + notes_sans_moyenne

#         notes = []
#         for item in toutes_les_notes:
#             note = Note(
#                 filiere=item.get('filiere'),
#                 classe=item.get('classe'),
#                 annee_academique=item.get('annee_academique'),
#                 enseignant=item.get('enseignant'),
#                 ue=item.get('ue'),
#                 ecue=item.get('ecue'),
#                 nom_etudiant=item.get('nom_etudiant'),
#                 matricule_etudiant=item.get('matricule_etudiant'),
#                 moyenne=item.get('moyenne'),
#                 rang_matiere=item.get('rang_matiere')
#             )
#             db.session.add(note)
#             notes.append(note)

#         db.session.commit()
#         print(f"{len(notes)} note(s) enregistrée(s) avec succès.")
#         return jsonify({"message": f"{len(notes)} note(s) enregistrée(s) avec succès."}), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500
@app.route('/api/notes', methods=['POST'])
def enregistrer_notes():
    try:
        data = request.get_json()

        if isinstance(data, dict):
            data = [data]

        # Champs pour identifier la fiche
        sample = data[0]
        classe = sample.get('classe')
        ue = sample.get('ue')
        ecue = sample.get('ecue')
        annee = sample.get('annee_academique')

        replace = request.args.get('replace') == 'true'

        # Vérifier si la fiche existe déjà
        fiche_existante = Note.query.filter_by(
            classe=classe,
            ue=ue,
            ecue=ecue,
            annee_academique=annee
        ).first()

        if fiche_existante and not replace:
            return jsonify({
                "message": "Cette fiche de notes existe déjà.",
                "action_required": True
            }), 409

        # Si remplacement demandé, supprimer les anciennes notes
        if fiche_existante and replace:
            Note.query.filter_by(
                classe=classe,
                ue=ue,
                ecue=ecue,
                annee_academique=annee
            ).delete()
            db.session.commit()

        # Calcul du rang avant insertion
        notes_avec_moyenne = [n for n in data if n.get('moyenne') is not None]
        notes_sans_moyenne = [n for n in data if n.get('moyenne') is None]

        notes_avec_moyenne.sort(key=lambda n: n['moyenne'], reverse=True)

        rang = 1
        for i, note in enumerate(notes_avec_moyenne):
            if i > 0 and note['moyenne'] == notes_avec_moyenne[i - 1]['moyenne']:
                note['rang_matiere'] = notes_avec_moyenne[i - 1]['rang_matiere']
            else:
                note['rang_matiere'] = rang
            rang += 1

        toutes_les_notes = notes_avec_moyenne + notes_sans_moyenne

        notes = []
        for item in toutes_les_notes:
            note = Note(
                filiere=item.get('filiere'),
                classe=item.get('classe'),
                annee_academique=item.get('annee_academique'),
                enseignant=item.get('enseignant'),
                ue=item.get('ue'),
                ecue=item.get('ecue'),
                nom_etudiant=item.get('nom_etudiant'),
                matricule_etudiant=item.get('matricule_etudiant'),
                moyenne=item.get('moyenne'),
                rang_matiere=item.get('rang_matiere')
            )
            db.session.add(note)
            notes.append(note)

        db.session.commit()
        return jsonify({"message": f"{len(notes)} note(s) enregistrée(s) avec succès."}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

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
