"""ShipmentStatus

Revision ID: 131eabff66b2
Revises: bb8bf9017c35
Create Date: 2026-04-09 23:21:04.005283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '131eabff66b2'
down_revision: Union[str, Sequence[str], None] = 'bb8bf9017c35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE shipmentstatus ADD VALUE IF NOT EXISTS 'cancelled'")


def downgrade() -> None:
    """Downgrade schema."""
    # PostgreSQL does not support removing enum values natively.
    # To revert: recreate the type without 'cancelled' and alter affected columns.
    op.execute("""
        ALTER TYPE shipmentstatus RENAME TO shipmentstatus_old;
        CREATE TYPE shipmentstatus AS ENUM ('placed', 'in_transit', 'out_for_delivery', 'delivered');
        ALTER TABLE shipment_events
            ALTER COLUMN status TYPE shipmentstatus
            USING status::text::shipmentstatus;
        DROP TYPE shipmentstatus_old;
    """)

