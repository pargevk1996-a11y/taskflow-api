"""rename username to login

Revision ID: 6d4d0f7a9c21
Revises: 35dabff83d6d
Create Date: 2026-04-03 11:55:00.000000
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "6d4d0f7a9c21"
down_revision: Union[str, None] = "35dabff83d6d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("ix_users_username", table_name="users")
    op.alter_column("users", "username", new_column_name="login")
    op.create_index("ix_users_login", "users", ["login"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_users_login", table_name="users")
    op.alter_column("users", "login", new_column_name="username")
    op.create_index("ix_users_username", "users", ["username"], unique=True)
