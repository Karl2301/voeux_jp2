"""
Ce fichier __init__.py est utilisé pour initialiser le package 'routes' dans l'application Parcoursup Voeux JP2.
Il importe et expose les différentes routes de l'application, permettant ainsi de gérer les différentes
fonctionnalités de l'application telles que la connexion, la déconnexion, l'affichage de la page d'accueil,
le tableau de bord, et la gestion des données.
"""

from .login_get import login_get
from .login_post import login_post
from .home import home
from .dashboard import dashboard
from .logout import logout
from .get_data import get_data
from .update_data import update_data
from .settings import settings
