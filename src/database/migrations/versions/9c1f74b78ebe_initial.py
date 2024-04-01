"""Initial

Revision ID: 9c1f74b78ebe
Revises: 
Create Date: 2024-03-31 02:31:14.586048

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9c1f74b78ebe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
                              nullable=True),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
                              nullable=True),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_role')),
                    sa.UniqueConstraint('name', name=op.f('uq_role_name'))
                    )
    op.create_table('user',
                    sa.Column('email', sa.String(length=150), nullable=False),
                    sa.Column('password', sa.Text(), nullable=False),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.Column('code', sa.String(length=150), nullable=True),
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
                              nullable=True),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
                              nullable=True),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
                    sa.UniqueConstraint('email', name=op.f('uq_user_email'))
                    )
    op.create_table('permission',
                    sa.Column('name', sa.String(length=32), nullable=True),
                    sa.Column('module', sa.String(length=32), nullable=True),
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
                              nullable=True),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
                              nullable=True),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_permission')),
                    sa.UniqueConstraint('name', name=op.f('uq_permission_name'))
                    )
    op.create_table('role_permission',
                    sa.Column('role_id', sa.UUID(), nullable=True),
                    sa.Column('permission_id', sa.UUID(), nullable=True),
                    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'],
                                            name=op.f('fk_role_permission_permission_id_permission')),
                    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name=op.f('fk_role_permission_role_id_role'))
                    )
    op.create_table('user_role',
                    sa.Column('user_id', sa.UUID(), nullable=True),
                    sa.Column('role_id', sa.UUID(), nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name=op.f('fk_user_role_role_id_role')),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_user_role_user_id_user'))
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_table('role_permission')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('permission')
    # ### end Alembic commands ###
