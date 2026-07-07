"""Add benchmarks table.

Revision ID: 002
Revises: 001
Create Date: 2024-01-02
"""

import sqlalchemy as sa

from alembic import op

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "benchmarks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("model_id", sa.Integer(), sa.ForeignKey("models.id")),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("dataset_size", sa.Integer()),
        sa.Column("metrics", sa.JSON()),
        sa.Column("duration_ms", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("benchmarks")
