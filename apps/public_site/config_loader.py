import logging
from datetime import datetime
from pathlib import Path
from threading import RLock
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat

logger = logging.getLogger(__name__)


class LandingLogisticsItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    value: str


class LandingConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    eyebrow: str = ""
    title_main: str = ""
    title_accent: str = ""
    subtitle: str = ""
    logistics: list[LandingLogisticsItem] = Field(default_factory=list)
    divider_label: str = ""
    factions_intro_title: str = ""
    factions_intro_text: str = ""
    about_title: str = ""
    about_paragraphs: list[str] = Field(default_factory=list)
    cta_title: str = ""
    cta_text: str = ""
    cta_button: str = ""


class FactionConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    glyph: str
    name: str
    description: str


class EmailsConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gm_notification_to: list[str] = Field(default_factory=list)
    public_contact_email: str = ""


class RosterConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sort_by: str = "display_name"


class EventConfig(BaseModel):
    """Pydantic model for event_config/current_event.yaml."""

    model_config = ConfigDict(extra="forbid")

    slug: str
    title: str
    subtitle: str = ""
    location_text: str = ""
    start_at: datetime
    end_at: datetime
    price_amount: NonNegativeFloat
    currency: str = "ILS"
    registration_open: bool = False
    public_roster_enabled: bool = False
    morning_document_type: int = 320
    cardcom_language: str = "he"

    landing: LandingConfig = Field(default_factory=LandingConfig)
    factions: list[FactionConfig] = Field(default_factory=list)
    emails: EmailsConfig = Field(default_factory=EmailsConfig)
    roster: RosterConfig = Field(default_factory=RosterConfig)


class FormFieldConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    type: str
    label: str
    required: bool = False
    max_length: int | None = None
    help_text: str = ""
    rows: int | None = None


class SpamProtectionConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    honeypot_field: str = "website"


class FormSchemaConfig(BaseModel):
    """Pydantic model for event_config/application_form.yaml."""

    model_config = ConfigDict(extra="forbid")

    version: int = 1
    title: str = ""
    submit_button: str = ""
    fields: list[FormFieldConfig] = Field(default_factory=list)
    spam_protection: SpamProtectionConfig = Field(default_factory=SpamProtectionConfig)


class ConfigLoader:
    """Loads and caches YAML configuration files."""

    _event_config: EventConfig | None = None
    _form_schema: FormSchemaConfig | None = None
    _lock: RLock = RLock()

    @classmethod
    def get_event_config(cls, *, reload: bool = False) -> EventConfig:
        with cls._lock:
            if cls._event_config is None or reload:
                cls._event_config = cls._load_event_config()
            return cls._event_config

    @classmethod
    def get_form_schema(cls, *, reload: bool = False) -> FormSchemaConfig:
        with cls._lock:
            if cls._form_schema is None or reload:
                cls._form_schema = cls._load_form_schema()
            return cls._form_schema

    @classmethod
    def _config_dir(cls) -> Path:
        return Path(__file__).resolve().parent.parent.parent / "event_config"

    @classmethod
    def _load_yaml(cls, filename: str) -> dict[str, Any]:
        path = cls._config_dir() / filename
        if not path.is_file():
            raise FileNotFoundError(f"Config file not found: {path}")
        logger.debug("Loading config from %s", path)
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError(f"Expected a YAML mapping in {path}, got {type(data).__name__}")
        return data

    @classmethod
    def _load_event_config(cls) -> EventConfig:
        return EventConfig(**cls._load_yaml("current_event.yaml"))

    @classmethod
    def _load_form_schema(cls) -> FormSchemaConfig:
        return FormSchemaConfig(**cls._load_yaml("application_form.yaml"))

    @classmethod
    def clear_cache(cls) -> None:
        with cls._lock:
            cls._event_config = None
            cls._form_schema = None
