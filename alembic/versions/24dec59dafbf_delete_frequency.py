"""Delete frequency

Revision ID: 24dec59dafbf
Revises: 3a4d72177b3b
Create Date: 2024-06-13 21:55:00.000000

"""

revision = '24dec59dafbf'
down_revision = '3a4d72177b3b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'subscriptions_new',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False, index=True),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('type_id', sa.Integer(), nullable=False),
        sa.Column('time', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(['type_id'], ['subscription_types.id']),
        sa.UniqueConstraint('user_id', 'city', 'type_id', 'time', name='_user_city_type_time_uc')
    )
    op.execute("""
        INSERT INTO subscriptions_new (id, user_id, city, type_id, time)
        SELECT id, user_id, city, type_id, time FROM subscriptions
    """)
    op.drop_table('subscriptions')
    op.rename_table('subscriptions_new', 'subscriptions')

def downgrade():
    pass
