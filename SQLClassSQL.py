from sqlmodel import SQLModel, Field
from sqlalchemy import Column, TEXT, Integer
from typing import Optional

class Student(SQLModel, table=True):
    __tablename__ = "eleves"
    identifiant_unique: str = Field(sa_column=Column(TEXT, primary_key=True, index=True))
    cookie: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    niveau_classe: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    voeux_etablissements: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    online: Optional[bool] = Field(default=None)
    deja_connecte: Optional[bool] = Field(default=None)
    choix_validees: Optional[bool] = Field(default=None)

class IdentifiantPerdue(SQLModel, table=True):
    __tablename__ = "identifiants_perdus"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True))
    classe: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    nom: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    prenom: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    created_at: Optional[str] = Field(default=None, sa_column=Column(TEXT))

class Professeurs(SQLModel, table=True):
    __tablename__ = "professeurs"
    id: Optional[int] = Field(default=None, sa_column=Column(Integer, primary_key=True))
    username: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    nom: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    prenom: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    email: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    password: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    created_at: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    online: Optional[bool] = Field(default=None)
    deja_connecte: Optional[bool] = Field(default=None)