"""Application-domain constants shared across forms, services, and views."""

from typing import Final

# ---------------------------------------------------------------------------
# Form constants
# ---------------------------------------------------------------------------

# Contact fields stored as dedicated Application model columns (not in answers_json).
CONTACT_FIELD_KEYS: Final[frozenset[str]] = frozenset({"full_name", "display_name", "email", "phone"})

# Regex for phone validation: must contain 7-15 digits; allows +, -, spaces, parens, dots.
PHONE_REGEX: Final[str] = r"^(?=(?:\D*\d){7,15}\D*$)[\d\s\-+().]{7,32}$"

# Maps YAML field type strings to ApplicationForm builder method names.
FIELD_TYPE_MAP: Final[dict[str, str]] = {
    "text": "_build_char_field",
    "email": "_build_email_field",
    "tel": "_build_tel_field",
    "checkbox": "_build_boolean_field",
    "textarea": "_build_textarea_field",
    "select": "_build_select_field",
}

# ---------------------------------------------------------------------------
# GM workflow state transitions
# ---------------------------------------------------------------------------

from apps.applications.models import Application  # noqa: E402

# gm_status values from which an application can be approved.
APPROVABLE_STATUSES: Final[frozenset[str]] = frozenset({Application.GmStatus.SUBMITTED.value})

# gm_status values from which an application can be rejected.
REJECTABLE_STATUSES: Final[frozenset[str]] = frozenset({Application.GmStatus.SUBMITTED.value})

# gm_status values from which an application can be published to the public roster.
PUBLISHABLE_STATUSES: Final[frozenset[str]] = frozenset({Application.GmStatus.APPROVED.value})
