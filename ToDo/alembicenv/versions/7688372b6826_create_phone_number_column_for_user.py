"""Create phone number column for user

Revision ID: 7688372b6826
Revises: 
Create Date: 2026-05-08 23:47:12.515647

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7688372b6826'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("phone_number", sa.String(length=10), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "phone_number")
