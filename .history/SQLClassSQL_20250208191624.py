"""
Ce fichier est utilisé pour définir la structure des tables dans la base de données SQL, facilitant ainsi les opérations CRUD (Create, Read, Update, Delete) sur les enregistrements des étudiants.
"""

from sqlmodel import SQLModel, Field
from typing import Optional

class Student(SQLModel, table=True):
    __tablename__ = "eleves"
    identifiant_unique: str = Field(primary_key=True, index=True)
    cookie: Optional[str] = Field(default=None)
    niveau_classe: Optional[str] = Field(default=None)
    voeux_etablissements: Optional[str] = Field(default=None)
    online: Optional[bool] = Field(default=None)
    deja_connecte: Optional[bool] = Field(default=None)
    choix_validees: Optional[bool] = Field(default=None)

class IdentifiantPerdue(SQLModel, table=True):
    __tablename__ = "identifiants_perdus"
    nom: str = Field(primary_key=True, index=True)
    prenom: str = Field(primary_key=True, index=True)
    classe: str = Field(primary_key=True, index=True)
    created_at: Optional[str] = Field(default=None)

class Professeur(SQLModel, table=True):
    __tablename__ = "professeurs"
    identifiant: str = Field(primary_key=True, index=True)
    mot_de_passe: str = Field()
    nom: str = Field()
    prenom: str = Field()
    created_at: Optional[str] = Field(default=None)
    online: Optional[bool] = Field(default=None)
    permissions: int = Field(default=1)
    superuser: Optional[bool] = Field(default=False)
