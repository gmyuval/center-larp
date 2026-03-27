"""Dynamic application form built at runtime from the YAML form schema."""

import logging
from collections.abc import Callable
from typing import Any, cast

from django import forms
from django.core.validators import RegexValidator

from apps.public_site.config_loader import ConfigLoader, FormFieldConfig, FormSchemaConfig

from .constants import FIELD_TYPE_MAP, PHONE_REGEX

logger = logging.getLogger(__name__)

phone_validator = RegexValidator(
    regex=PHONE_REGEX,
    message="נא להזין מספר טלפון תקין.",
)


class ApplicationForm(forms.Form):
    """Dynamic form built at runtime from the YAML application_form schema.

    Each field defined in ``application_form.yaml`` is mapped to the
    appropriate Django form field type.  A honeypot anti-spam field is
    appended automatically based on the schema's ``spam_protection`` section.
    """

    def __init__(self, *args: Any, schema: FormSchemaConfig | None = None, **kwargs: Any) -> None:
        """Initialise the form and build fields from the YAML schema.

        Args:
            schema: Optional pre-loaded form schema.  Falls back to
                ``ConfigLoader.get_form_schema()`` when not provided.
        """
        super().__init__(*args, **kwargs)
        self._schema = schema or ConfigLoader.get_form_schema()
        self._build_fields()

    # ------------------------------------------------------------------
    # Field construction
    # ------------------------------------------------------------------

    def _build_fields(self) -> None:
        """Populate ``self.fields`` from the YAML schema, then append the honeypot."""
        for field_config in self._schema.fields:
            self.fields[field_config.key] = self._create_field(field_config)

        honeypot_key = self._schema.spam_protection.honeypot_field
        self.fields[honeypot_key] = forms.CharField(
            required=False,
            label="",
            widget=forms.TextInput(
                attrs={
                    "tabindex": "-1",
                    "autocomplete": "off",
                    "aria-hidden": "true",
                    "class": "hp-field",
                }
            ),
        )

    def _create_field(self, config: FormFieldConfig) -> forms.Field:
        """Dispatch to the correct builder based on the YAML field type."""
        builder_name = FIELD_TYPE_MAP.get(config.type)
        if builder_name is None:
            raise ValueError(f"Unsupported application field type: {config.type!r}")
        builder = cast(Callable[[FormFieldConfig], forms.Field], getattr(self, builder_name))
        return builder(config)

    @staticmethod
    def _base_kwargs(config: FormFieldConfig) -> dict[str, Any]:
        """Return keyword arguments common to all field types."""
        return {
            "label": config.label,
            "required": config.required,
            "help_text": config.help_text or "",
        }

    def _build_char_field(self, config: FormFieldConfig) -> forms.CharField:
        """Build a ``CharField`` for plain text input."""
        kwargs = self._base_kwargs(config)
        if config.max_length:
            kwargs["max_length"] = config.max_length
        return forms.CharField(**kwargs)

    def _build_email_field(self, config: FormFieldConfig) -> forms.EmailField:
        """Build an ``EmailField`` with built-in email format validation."""
        kwargs = self._base_kwargs(config)
        if config.max_length:
            kwargs["max_length"] = config.max_length
        return forms.EmailField(**kwargs)

    def _build_tel_field(self, config: FormFieldConfig) -> forms.CharField:
        """Build a ``CharField`` with telephone input widget and phone regex validator."""
        kwargs = self._base_kwargs(config)
        if config.max_length:
            kwargs["max_length"] = config.max_length
        kwargs["widget"] = forms.TextInput(attrs={"type": "tel", "dir": "ltr"})
        kwargs["validators"] = [phone_validator]
        return forms.CharField(**kwargs)

    def _build_boolean_field(self, config: FormFieldConfig) -> forms.BooleanField:
        """Build a ``BooleanField`` for checkbox input."""
        kwargs = self._base_kwargs(config)
        return forms.BooleanField(**kwargs)

    def _build_textarea_field(self, config: FormFieldConfig) -> forms.CharField:
        """Build a ``CharField`` with a ``Textarea`` widget."""
        kwargs = self._base_kwargs(config)
        widget_attrs: dict[str, Any] = {}
        if config.rows:
            widget_attrs["rows"] = config.rows
        kwargs["widget"] = forms.Textarea(attrs=widget_attrs)
        if config.max_length:
            kwargs["max_length"] = config.max_length
        return forms.CharField(**kwargs)

    def _build_select_field(self, config: FormFieldConfig) -> forms.ChoiceField:
        """Build a ``ChoiceField`` with a ``Select`` widget from YAML choices."""
        kwargs = self._base_kwargs(config)
        blank_label = ("", "---")
        kwargs["choices"] = [blank_label] + [(c, c) for c in config.choices]
        return forms.ChoiceField(**kwargs)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def clean(self) -> dict[str, Any]:
        """Run cross-field validation: honeypot check and faction choice dedup."""
        cleaned = super().clean()
        if cleaned is None:
            return {}

        honeypot_key = self._schema.spam_protection.honeypot_field
        if cleaned.get(honeypot_key):
            logger.warning("Honeypot field filled — likely spam submission")
            raise forms.ValidationError("ההגשה נדחתה.")

        first = cleaned.get("faction_preference", "")
        second = cleaned.get("faction_second_choice", "")
        if first and second and first == second:
            self.add_error("faction_second_choice", "הסיעה השנייה חייבת להיות שונה מהסיעה הראשונה.")

        return cleaned
