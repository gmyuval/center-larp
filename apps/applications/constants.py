"""Application-domain constants shared across forms, services, and views."""

from typing import Final

# Contact fields stored as dedicated Application model columns (not in answers_json).
CONTACT_FIELD_KEYS: Final[frozenset[str]] = frozenset({"full_name", "display_name", "email", "phone"})

# Regex for phone validation: digits, plus, dash, spaces, parens, dots — 7-32 chars.
PHONE_REGEX: Final[str] = r"^[\d\s\-+().]{7,32}$"

# Maps YAML field type strings to ApplicationForm builder method names.
FIELD_TYPE_MAP: Final[dict[str, str]] = {
    "text": "_build_char_field",
    "email": "_build_email_field",
    "tel": "_build_tel_field",
    "checkbox": "_build_boolean_field",
    "textarea": "_build_textarea_field",
}
