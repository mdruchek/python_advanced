"""merge code added columns user.surname and user.patronomic

Revision ID: 123e1c19c4d4
Revises: 22ef9ac9829e, 32a25a718bac
Create Date: 2024-05-10 09:40:51.856226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '123e1c19c4d4'
down_revision: Union[str, None] = ('22ef9ac9829e', '32a25a718bac')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
