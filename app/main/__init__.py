from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission

#Context processors help to avail Permissions globally
#Permission class will be used by templates as well
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)