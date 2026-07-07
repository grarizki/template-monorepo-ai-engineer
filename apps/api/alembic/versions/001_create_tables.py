"""Create tables.

Revision ID: 001
Revises:
Create Date: 2024-01-01
"""

import sqlalchemy as sa

from alembic import op

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), unique=True, nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("image_url", sa.String()),
    )
    op.create_table(
        "models",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), unique=True, nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("artifact_path", sa.String()),
        sa.Column("metrics", sa.JSON()),
    )
    op.create_table(
        "training_scripts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), unique=True, nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("model_id", sa.Integer(), sa.ForeignKey("models.id")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("image_url", sa.String()),
    )
    op.create_table(
        "deployments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("model_id", sa.Integer(), sa.ForeignKey("models.id")),
        sa.Column("status", sa.String(), default="pending"),
        sa.Column("deployed_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("url", sa.String()),
    )


def downgrade():
    op.drop_table("deployments")
    op.drop_table("training_scripts")
    op.drop_table("models")
    op.drop_table("projects")
