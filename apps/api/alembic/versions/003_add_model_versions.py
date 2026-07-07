"""add model_versions table

Revision ID: 003
Revises: 002
Create Date: 2026-07-07
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "model_versions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("model_id", sa.Integer(), sa.ForeignKey("models.id"), nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("metrics", sa.JSON()),
        sa.Column("artifact_path", sa.String()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("model_versions")
