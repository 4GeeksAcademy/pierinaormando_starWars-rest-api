"""empty message

Revision ID: 3b29c23076b5
Revises: 837fc6bf612a
Create Date: 2023-12-18 22:44:32.240613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b29c23076b5'
down_revision = '837fc6bf612a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=False),
    sa.Column('gender', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('climate', sa.String(length=120), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=False),
    sa.Column('model', sa.String(length=250), nullable=False),
    sa.Column('passengers', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('planet')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('climate', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('diameter', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='planet_pkey'),
    sa.UniqueConstraint('name', name='planet_name_key')
    )
    op.drop_table('vehicles')
    op.drop_table('planets')
    op.drop_table('characters')
    # ### end Alembic commands ###