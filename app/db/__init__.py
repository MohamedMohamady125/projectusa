"""
Database package initialization.
Import all models here to ensure they are registered with SQLAlchemy.
This is important for Alembic migrations.
"""
from app.db.base import Base

# Import all models to register them with SQLAlchemy
# These imports must come after Base is defined
from app.models.user import User  # noqa
from app.models.athlete import AthleteProfile, SwimmingTime  # noqa
from app.models.school import School, Coach, TeamRanking  # noqa
from app.models.task import Task  # noqa
from app.models.recruitment import RecruitmentTracking, Communication  # noqa
from app.models.document import Document  # noqa
from app.models.tutorial import VideoTutorial, TutorialProgress  # noqa
from app.models.email_template import EmailTemplate  # noqa
from app.models.notification import Notification  # noqa
from app.models.admin_log import AdminActivityLog  # noqa

__all__ = [
    "Base",
    "User",
    "AthleteProfile",
    "SwimmingTime",
    "School",
    "Coach",
    "TeamRanking",
    "Task",
    "RecruitmentTracking",
    "Communication",
    "Document",
    "VideoTutorial",
    "TutorialProgress",
    "EmailTemplate",
    "Notification",
    "AdminActivityLog",
]
