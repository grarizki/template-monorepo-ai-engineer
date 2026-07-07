"""Ensure database tables exist before tests run."""

from ai_template.db import init_db

init_db()
