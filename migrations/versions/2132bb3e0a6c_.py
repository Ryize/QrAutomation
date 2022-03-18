"""empty message

Revision ID: 2132bb3e0a6c
Revises: d886e017232e
Create Date: 2022-03-18 22:18:16.018803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2132bb3e0a6c'
down_revision = 'd886e017232e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('cabinet')
    op.drop_table('schedule_cleaning')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('schedule_cleaning',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('cabinet_id', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('created_on', sa.DATETIME(), nullable=True),
    sa.Column('updated_on', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['cabinet_id'], ['cabinet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cabinet',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('number', sa.VARCHAR(length=48), nullable=False),
    sa.Column('created_on', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=64), nullable=True),
    sa.Column('name', sa.VARCHAR(length=64), nullable=False),
    sa.Column('surname', sa.VARCHAR(length=64), nullable=False),
    sa.Column('patronymic', sa.VARCHAR(length=64), nullable=True),
    sa.Column('password', sa.VARCHAR(length=128), nullable=False),
    sa.Column('created_on', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
