"""
Admin service for managing users, schools, and system statistics.
"""
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.models.school import School
from app.models.athlete import SwimmingTime
from app.models.task import Task
from app.models.admin_log import AdminActivityLog
from app.schemas.admin import AdminDashboardStats, UserUpdate
from app.schemas.school import SchoolCreate


class AdminService:
    """Service for admin operations."""

    def __init__(self, db: AsyncSession):
        """Initialize admin service."""
        self.db = db

    async def get_dashboard_stats(self) -> AdminDashboardStats:
        """Get dashboard statistics for admin."""
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        week_start = now - timedelta(days=7)

        # Total counts
        total_users_result = await self.db.execute(select(func.count(User.id)))
        total_users = total_users_result.scalar() or 0

        total_athletes_result = await self.db.execute(
            select(func.count(User.id)).where(User.role == UserRole.ATHLETE)
        )
        total_athletes = total_athletes_result.scalar() or 0

        total_coaches_result = await self.db.execute(
            select(func.count(User.id)).where(User.role == UserRole.COACH)
        )
        total_coaches = total_coaches_result.scalar() or 0

        total_schools_result = await self.db.execute(select(func.count(School.id)))
        total_schools = total_schools_result.scalar() or 0

        # Active users
        active_today_result = await self.db.execute(
            select(func.count(User.id)).where(User.last_login >= today_start)
        )
        active_users_today = active_today_result.scalar() or 0

        active_week_result = await self.db.execute(
            select(func.count(User.id)).where(User.last_login >= week_start)
        )
        active_users_week = active_week_result.scalar() or 0

        # New users
        new_today_result = await self.db.execute(
            select(func.count(User.id)).where(User.created_at >= today_start)
        )
        new_users_today = new_today_result.scalar() or 0

        new_week_result = await self.db.execute(
            select(func.count(User.id)).where(User.created_at >= week_start)
        )
        new_users_week = new_week_result.scalar() or 0

        # Swimming times
        total_times_result = await self.db.execute(select(func.count(SwimmingTime.id)))
        total_swimming_times = total_times_result.scalar() or 0

        # Tasks
        total_tasks_result = await self.db.execute(select(func.count(Task.id)))
        total_tasks = total_tasks_result.scalar() or 0

        # Pending verifications
        pending_verif_result = await self.db.execute(
            select(func.count(User.id)).where(User.is_verified == False)
        )
        pending_verifications = pending_verif_result.scalar() or 0

        return AdminDashboardStats(
            total_users=total_users,
            total_athletes=total_athletes,
            total_coaches=total_coaches,
            total_schools=total_schools,
            active_users_today=active_users_today,
            active_users_week=active_users_week,
            new_users_today=new_users_today,
            new_users_week=new_users_week,
            total_swimming_times=total_swimming_times,
            total_tasks=total_tasks,
            pending_verifications=pending_verifications
        )

    async def get_users_paginated(
        self,
        skip: int = 0,
        limit: int = 20,
        role: Optional[UserRole] = None,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_verified: Optional[bool] = None
    ) -> Tuple[List[User], int]:
        """Get paginated list of users with filters."""
        query = select(User)

        # Apply filters
        filters = []
        if role:
            filters.append(User.role == role)
        if is_active is not None:
            filters.append(User.is_active == is_active)
        if is_verified is not None:
            filters.append(User.is_verified == is_verified)
        if search:
            filters.append(User.email.ilike(f"%{search}%"))

        if filters:
            query = query.where(and_(*filters))

        # Get total count
        count_query = select(func.count()).select_from(User)
        if filters:
            count_query = count_query.where(and_(*filters))
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # Get paginated results
        query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        users = result.scalars().all()

        return list(users), total

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def update_user(
        self,
        user_id: UUID,
        user_update: UserUpdate,
        admin: User
    ) -> Optional[User]:
        """Update user details."""
        user = await self.get_user_by_id(user_id)
        if not user:
            return None

        # Update fields
        if user_update.email is not None:
            user.email = user_update.email
        if user_update.role is not None:
            user.role = user_update.role
        if user_update.is_active is not None:
            user.is_active = user_update.is_active
        if user_update.is_verified is not None:
            user.is_verified = user_update.is_verified

        user.updated_at = datetime.utcnow()

        # Log activity
        await self.log_activity(
            admin=admin,
            action="update_user",
            entity_type="user",
            entity_id=user_id,
            details=f"Updated user {user.email}"
        )

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: UUID, admin: User) -> bool:
        """Delete user."""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False

        # Log activity
        await self.log_activity(
            admin=admin,
            action="delete_user",
            entity_type="user",
            entity_id=user_id,
            details=f"Deleted user {user.email}"
        )

        await self.db.delete(user)
        await self.db.commit()
        return True

    async def get_schools_paginated(
        self,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        state: Optional[str] = None,
        division: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Tuple[List[School], int]:
        """Get paginated list of schools with filters."""
        query = select(School)

        # Apply filters
        filters = []
        if is_active is not None:
            filters.append(School.is_active == is_active)
        if state:
            filters.append(School.state == state)
        if division:
            filters.append(School.division == division)
        if search:
            filters.append(
                or_(
                    School.name.ilike(f"%{search}%"),
                    School.city.ilike(f"%{search}%")
                )
            )

        if filters:
            query = query.where(and_(*filters))

        # Get total count
        count_query = select(func.count()).select_from(School)
        if filters:
            count_query = count_query.where(and_(*filters))
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # Get paginated results
        query = query.order_by(School.name.asc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        schools = result.scalars().all()

        return list(schools), total

    async def create_school(
        self,
        school_data: SchoolCreate,
        admin: User
    ) -> School:
        """Create a new school."""
        from uuid import uuid4

        school = School(
            id=uuid4(),
            name=school_data.name,
            division=school_data.division,
            state=school_data.state,
            city=school_data.city,
            conference=school_data.conference,
            school_website=school_data.school_website,
            swim_website_men=school_data.swim_website_men,
            swim_website_women=school_data.swim_website_women,
            midseason_meet_url_men=school_data.midseason_meet_url_men,
            midseason_meet_url_women=school_data.midseason_meet_url_women,
            conference_meet_url_men=school_data.conference_meet_url_men,
            conference_meet_url_women=school_data.conference_meet_url_women,
            description=school_data.description,
            enrollment=school_data.enrollment,
            public_private=school_data.public_private,
            international_students_percentage=school_data.international_students_percentage,
            average_sat=school_data.average_sat,
            average_act=school_data.average_act,
            average_gpa=school_data.average_gpa,
            tuition_in_state=school_data.tuition_in_state,
            tuition_out_state=school_data.tuition_out_state,
            room_board=school_data.room_board,
            has_mens_team=school_data.has_mens_team,
            has_womens_team=school_data.has_womens_team,
            mens_scholarships=school_data.mens_scholarships,
            womens_scholarships=school_data.womens_scholarships,
            mens_ranking=school_data.mens_ranking,
            womens_ranking=school_data.womens_ranking,
            mens_ranking_points=school_data.mens_ranking_points,
            womens_ranking_points=school_data.womens_ranking_points,
            recruiting_questionnaire_url=school_data.recruiting_questionnaire_url,
            logo_url=school_data.logo_url,
            images=school_data.images,
            facilities_info=school_data.facilities_info,
            academic_support=school_data.academic_support,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(school)

        # Log activity
        await self.log_activity(
            admin=admin,
            action="create_school",
            entity_type="school",
            entity_id=school.id,
            details=f"Created school {school.name}"
        )

        await self.db.commit()
        await self.db.refresh(school)
        return school

    async def toggle_school_active(
        self,
        school_id: UUID,
        admin: User
    ) -> Optional[School]:
        """Toggle school active status."""
        result = await self.db.execute(
            select(School).where(School.id == school_id)
        )
        school = result.scalar_one_or_none()

        if not school:
            return None

        school.is_active = not school.is_active
        school.updated_at = datetime.utcnow()

        # Log activity
        await self.log_activity(
            admin=admin,
            action="toggle_school_status",
            entity_type="school",
            entity_id=school_id,
            details=f"Set {school.name} active status to {school.is_active}"
        )

        await self.db.commit()
        await self.db.refresh(school)
        return school

    async def log_activity(
        self,
        admin: User,
        action: str,
        entity_type: str,
        entity_id: Optional[UUID] = None,
        details: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> AdminActivityLog:
        """Log admin activity."""
        log = AdminActivityLog(
            admin_id=admin.id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            ip_address=ip_address
        )
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log

    async def get_activity_logs(
        self,
        skip: int = 0,
        limit: int = 50,
        admin_id: Optional[UUID] = None,
        action: Optional[str] = None
    ) -> Tuple[List[AdminActivityLog], int]:
        """Get paginated activity logs."""
        query = select(AdminActivityLog)

        # Apply filters
        filters = []
        if admin_id:
            filters.append(AdminActivityLog.admin_id == admin_id)
        if action:
            filters.append(AdminActivityLog.action == action)

        if filters:
            query = query.where(and_(*filters))

        # Get total count
        count_query = select(func.count()).select_from(AdminActivityLog)
        if filters:
            count_query = count_query.where(and_(*filters))
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # Get paginated results
        query = query.order_by(AdminActivityLog.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        logs = result.scalars().all()

        return list(logs), total
