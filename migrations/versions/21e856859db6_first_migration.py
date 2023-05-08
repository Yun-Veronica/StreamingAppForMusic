"""first_migration

Revision ID: 21e856859db6
Revises: 01cef15365ec
Create Date: 2023-05-07 19:28:07.797998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21e856859db6'
down_revision = '01cef15365ec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Genre',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('musician_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('musicians', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('tracks', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Genre_pkey')
    )
    op.create_table('Track',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('genre', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('link_to_file', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Track_pkey')
    )
    op.create_table('Musician',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('tracks', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('genre', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('year_start', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('year_end', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Musician_pkey')
    )
    op.create_table('Playlist',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Playlist_pkey')
    )
    op.create_table('User',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('full_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=1), autoincrement=False, nullable=True),
    sa.Column('disabled', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('playlists', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='User_pkey')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
