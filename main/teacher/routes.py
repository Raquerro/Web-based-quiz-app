from flask_login import login_required
from .services import teacher_dashboard_service
from . import teacher_bp

@teacher_bp.route("/home")
@login_required
def home_student():
    return teacher_dashboard_service()