from flask import Blueprint
from .views import TaskTigerView

__all__ = ['TaskTigerView', 'tasktiger_admin']

tasktiger_admin = Blueprint('tasktiger_admin', __name__,
                            template_folder='templates')
