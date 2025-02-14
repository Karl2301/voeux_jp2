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
from .get_data import get_data, get_voeux_status, post_voeux_status
from .update_data import update_data
from .settings import settings
from .lost_id import lost_id_get, lost_id_post
from .test import vers_ma_page, vers_ma_page_post
from .update_theme import update_theme, get_theme
from .change_password import change_password_post, change_password_get
from .aide import aide_get, aide_post
from .configure_password import configure_password_get, configure_password_post
from .configure_prof import configure_prof_get, configure_prof_post
from .websocket import *
from .classes_prof import classes_prof_get
from .profil_eleve import profil_eleve_get
from .notifications import get_notifications, format_datetime