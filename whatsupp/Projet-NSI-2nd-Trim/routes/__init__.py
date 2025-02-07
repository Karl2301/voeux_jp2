from .login import login_get, login_post
from .dashboard import dashboard
from .reset_password import reset_password
from .admin import admin
from .register import register
from .reports import reports
from .get_messages import get_messages
from .update_user import update_user
from .delete_user import delete_user
from .new_user_conv import search_user
from .search_users import search_users
from .send_friend_request import send_friend_request
from .friend_requests import friend_requests
from .accept_friend_request import accept_friend_request
from .reject_friend_request import reject_friend_request
from .user_contacts import user_contacts
from .user_conversations import user_conversations
from .report_user import report_user
from .logout import logout
from .delete_message import delete_message
from .update_user_info import update_user_info
from .send_message import send_message
from .change_password import change_password
from .handle_report import handle_report
from .remove_friend import remove_friend
from .upload_image import upload_image
from .home import home, about_us, about_among_us
from .get_user_id import get_user_id
from .fonctions import app, engine, key, cipher_suite, encrypt_message, decrypt_message, get_db_connection, generate_session_cookie, get_users_info, get_messages_between_users
from .websocket import socketio
from .otp_verif import otp_verif
from .new_password import new_password
from .email_sent import email_sent
from .admin_panel import admin_panel
from .admin_panel_list_user import list_user_on_app
from .user_info_admin import user_info_admin, get_user_info, update_user_admin_info
from .admin_panel_banned import user_banned, user_banned_post
from .dashboard_theme import update_dashboard_theme
from .admin_panel_report import user_report_page, user_report_post
