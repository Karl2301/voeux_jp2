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