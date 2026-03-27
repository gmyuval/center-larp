"""Audit logging service for recording GM and system actions."""

import logging
from typing import Any

from django.db import models
from django.http import HttpRequest

from .models import AuditLog

logger = logging.getLogger(__name__)


class AuditService:
    """Creates AuditLog entries for GM and system actions.

    Provides convenience methods that extract actor information from
    Django admin requests and format target references consistently.
    """

    @classmethod
    def log(
        cls,
        *,
        actor_type: str,
        actor_label: str,
        action: str,
        target_type: str = "",
        target_id: str = "",
        details: dict[str, Any] | None = None,
    ) -> AuditLog:
        """Create an audit log entry.

        Args:
            actor_type: One of ``AuditLog.ActorType`` values (``"gm"`` or ``"system"``).
            actor_label: Human-readable identifier for the actor (e.g. username).
            action: Short description of the action performed.
            target_type: Model or entity type affected (e.g. ``"Application"``).
            target_id: Identifier of the target (e.g. public_id or pk).
            details: Optional dict of additional context to store as JSON.
        """
        entry = AuditLog.objects.create(
            actor_type=actor_type,
            actor_label=actor_label,
            action=action,
            target_type=target_type,
            target_id=str(target_id),
            details_json=details or {},
        )
        logger.debug(
            "Audit: %s %s %s/%s",
            actor_label,
            action,
            target_type,
            target_id,
        )
        return entry

    @classmethod
    def log_gm_action(
        cls,
        *,
        request: HttpRequest,
        action: str,
        target: models.Model,
        details: dict[str, Any] | None = None,
    ) -> AuditLog:
        """Convenience wrapper for GM actions triggered from the admin.

        Extracts the username from the request and derives the target
        type and id from the model instance.
        """
        username = getattr(request.user, "username", "unknown")
        target_type = type(target).__name__
        target_id = str(getattr(target, "public_id", target.pk))

        return cls.log(
            actor_type=AuditLog.ActorType.GM,
            actor_label=username,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details,
        )
