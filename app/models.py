from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(500))
    name = db.Column(db.String(500))
    email = db.Column(db.String(120), unique = True)
    telephone = db.Column(db.String(500))
    validate=db.Column(db.Boolean(), default=False)
    validation_code=db.Column(db.String(500))
    # posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_authenticated(self):
        return False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Salle(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(500))
    site = db.Column(db.String(500))
    longitude=db.Column(db.Float)
    latitude=db.Column(db.Float)
    nb_place=db.Column(db.Integer)
    etat=db.Column(db.String(500))
    activite=db.Column(db.String(500))
    reservation=db.Column(db.String(500))

    def __repr__(self):
        return '<Salle %r>' % (self.name)

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    filiere = db.Column(db.String(500))
    classe = db.Column(db.String(500))
    annee_academique = db.Column(db.String(500))
    enseignant = db.Column(db.String(500))
    ue = db.Column(db.String(500))
    ecue = db.Column(db.String(500))
    nom_etudiant = db.Column(db.String(500))
    matricule_etudiant = db.Column(db.String(500))
    moyenne = db.Column(db.Float)
    rang_matiere = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Note(classe='{self.classe}', enseignant='{self.enseignant}', ue='{self.ue}', ecue='{self.ecue}', nom_etudiant='{self.nom_etudiant}', matricule_etudiant='{self.matricule_etudiant}', moyenne={self.moyenne}, rang_matiere={self.rang_matiere})"


# from sqlalchemy import create_engine, Column, Integer, String, Float
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


# if __name__ == '__main__':