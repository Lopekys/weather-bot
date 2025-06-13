from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3a4d72177b3b'
down_revision: Union[str, None] = 'f2b40d220709'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('subscriptions', schema=None) as batch_op:
        batch_op.create_unique_constraint('_user_city_type_freq_uc', ['user_id', 'city', 'type_id', 'frequency_id'])
        batch_op.create_index('ix_subscriptions_user_id', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # ### Using batch mode to support SQLite ###
    with op.batch_alter_table('subscriptions', schema=None) as batch_op:
        batch_op.drop_index(op.f('ix_subscriptions_user_id'))
        batch_op.drop_constraint('_user_city_type_freq_uc', type_='unique')
