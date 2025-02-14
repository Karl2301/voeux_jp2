from sqlmodel import SQLModel, Field
from sqlalchemy import Column, TEXT, Integer
from typing import Optional
from datetime import datetime


class Users(SQLModel, table=True):
    __tablename__ = "utilisateurs"
    identifiant_unique: str = Field(sa_column=Column(TEXT, primary_key=True, index=True))
    password: Optional[str] = Field(default="EleveMDP", sa_column=Column(TEXT))
    cookie: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    niveau_classe: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    voeux_etablissements: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    online: Optional[bool] = Field(default=None)
    deja_connecte: Optional[bool] = Field(default=None)
    choix_validees: Optional[bool] = Field(default=None)
    dashboard_theme: Optional[bool] = Field(default=0)
    nom: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    prenom: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    email: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    professeur: bool = Field(default=False)


class IdentifiantPerdus(SQLModel, table=True):
    __tablename__ = "identifiants_perdus"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True))
    classe: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    nom: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    prenom: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    created_at: Optional[str] = Field(default=None, sa_column=Column(TEXT))

class DemandeAide(SQLModel, table=True):
    __tablename__ = "demandes_aide"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True))
    identifiant_eleve: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    classe: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    titre: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    message: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    created_at: Optional[str] = Field(default=None, sa_column=Column(TEXT))

class Classes(SQLModel, table=True):
    __tablename__ = "classes"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True))
    classe: Optional[str] = Field(default=None, sa_column=Column(TEXT))  # Ajout de la propriété 'classe'
    nom: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    professeur_principale: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    online_student: Optional[int] = Field(default=0)
    created_at: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    nbr_eleve_voeux_valide: Optional[int] = Field(default=0)

class NotificationsVoeux(SQLModel, table=True):
    __tablename__ = "notifications_voeux"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True))
    identifiant_eleve: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    message: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    created_at: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    