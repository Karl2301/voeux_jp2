from flask import Flask, render_template
import sqlmodel
from routes import *
from ext_config import app, engine
from SQLClassSQL import *
import datetime

classes = [('TA','Termiale A'), ('TB','Termiale B'), ('TC','Termiale C'), ('TD','Termiale D'), ('TE','Termiale E'), ('TF','Termiale F'), ('TG','Termiale G')]

def create_all_classes():
    for classe in classes:
        with Session(engine) as session:
            # Vérifier si la classe existe déjà
            existing_classe = session.query(Classes).filter_by(classe=classe[0]).first()
            if not existing_classe:
                print(f"Création de la classe {classe[0]}")
                new_classe = Classes(
                    classe=classe[0],
                    nom=classe[1],
                    created_at=datetime.datetime.now(),
                )
                session.add(new_classe)
                session.commit()
                print(f"Classe {classe[0]} créée")