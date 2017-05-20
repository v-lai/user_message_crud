"""reformat with wtforms

Revision ID: 3c2bd0ffe8f1
Revises: 57ea49df8978
Create Date: 2017-05-19 18:38:58.192224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c2bd0ffe8f1'
down_revision = '57ea49df8978'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'text',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('messages', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('messages', 'text',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###
