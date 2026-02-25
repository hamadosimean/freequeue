# documentation
from .base import BASE_DIR
from .constants import APP_NAME
import os

SPECTACULAR_SETTINGS = {
    "TITLE": APP_NAME,
    "DESCRIPTION": f"API for {APP_NAME}",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}


JAZZMIN_SETTINGS = {
    "site_title": APP_NAME,
    "site_header": APP_NAME,
    "welcome_sign": f"Welcome to {APP_NAME} Admin",
    # "site_logo": "images/logo.png",
    # "site_logo_classes": "img-circle h-120 w-120",
    "site_icon": "images/logo.png",
    "copyright": f"{APP_NAME} © 2025",
    "show_ui_builder": False,
    "navigation_expanded": True,
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "language_chooser": False,
    "login_logo": None,
    "login_logo_dark": None,
}

# JAZZMIN_UI_TWEAKS = {
#     "theme": "darkly",
#     "dark_mode_theme": "darkly",
# }
