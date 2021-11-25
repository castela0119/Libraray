"""empty message

Revision ID: 5b353c8318d7
Revises: 
Create Date: 2021-11-24 15:14:53.049993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b353c8318d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sqlite_sequence')
    op.alter_column('lib_books', 'book_id',
               existing_type=sa.BLOB(),
               nullable=False,
               autoincrement=True)
    op.alter_column('lib_books', 'book_name',
               existing_type=sa.BLOB(),
               nullable=False)
    op.alter_column('lib_books', 'isbn',
               existing_type=sa.BLOB(),
               nullable=False)
    op.drop_column('lib_books', 'link')
    op.alter_column('lib_reviews', 'review_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.alter_column('lib_reviews', 'user_email',
               existing_type=sa.BLOB(),
               nullable=False)
    op.alter_column('lib_reviews', 'book_id',
               existing_type=sa.BLOB(),
               nullable=False)
    op.alter_column('lib_reviews', 'rating',
               existing_type=sa.BLOB(),
               nullable=False)
    op.create_foreign_key(None, 'lib_reviews', 'lib_users', ['user_email'], ['user_email'])
    op.create_foreign_key(None, 'lib_reviews', 'lib_books', ['book_id'], ['book_id'])
    op.alter_column('lib_status', 'status_no',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.alter_column('lib_status', 'book_id',
               existing_type=sa.BLOB(),
               nullable=False)
    op.alter_column('lib_status', 'user_email',
               existing_type=sa.BLOB(),
               nullable=False)
    op.alter_column('lib_status', 'book_name',
               existing_type=sa.BLOB(),
               nullable=False)
    op.alter_column('lib_status', 'avg',
               existing_type=sa.BLOB(),
               nullable=False)
    op.create_foreign_key(None, 'lib_status', 'lib_users', ['user_email'], ['user_email'])
    op.create_foreign_key(None, 'lib_status', 'lib_books', ['book_id'], ['book_id'])
    op.create_foreign_key(None, 'lib_status', 'lib_books', ['book_name'], ['book_name'])
    op.create_foreign_key(None, 'lib_status', 'lib_books', ['img_path'], ['img_path'])
    op.alter_column('lib_users', 'user_no',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.alter_column('lib_users', 'user_email',
               existing_type=sa.BLOB(),
               nullable=False)
    op.alter_column('lib_users', 'user_pw',
               existing_type=sa.BLOB(),
               nullable=False)
    op.alter_column('lib_users', 'user_name',
               existing_type=sa.BLOB(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('lib_users', 'user_name',
               existing_type=sa.BLOB(),
               nullable=True)
    op.alter_column('lib_users', 'user_pw',
               existing_type=sa.BLOB(),
               nullable=True)
    op.alter_column('lib_users', 'user_email',
               existing_type=sa.BLOB(),
               nullable=True)
    op.alter_column('lib_users', 'user_no',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    op.drop_constraint(None, 'lib_status', type_='foreignkey')
    op.drop_constraint(None, 'lib_status', type_='foreignkey')
    op.drop_constraint(None, 'lib_status', type_='foreignkey')
    op.drop_constraint(None, 'lib_status', type_='foreignkey')
    op.alter_column('lib_status', 'avg',
               existing_type=sa.BLOB(),
               nullable=True)
    op.alter_column('lib_status', 'book_name',
               existing_type=sa.BLOB(),
               nullable=True)
    op.alter_column('lib_status', 'user_email',
               existing_type=sa.BLOB(),
               nullable=True)
    op.alter_column('lib_status', 'book_id',
               existing_type=sa.BLOB(),
               nullable=True)
    op.alter_column('lib_status', 'status_no',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    op.drop_constraint(None, 'lib_reviews', type_='foreignkey')
    op.drop_constraint(None, 'lib_reviews', type_='foreignkey')
    op.alter_column('lib_reviews', 'rating',
               existing_type=sa.BLOB(),
               nullable=True)
    op.alter_column('lib_reviews', 'book_id',
               existing_type=sa.BLOB(),
               nullable=True)
    op.alter_column('lib_reviews', 'user_email',
               existing_type=sa.BLOB(),
               nullable=True)
    op.alter_column('lib_reviews', 'review_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    op.add_column('lib_books', sa.Column('link', sa.BLOB(), nullable=True))
    op.alter_column('lib_books', 'isbn',
               existing_type=sa.BLOB(),
               nullable=True)
    op.alter_column('lib_books', 'book_name',
               existing_type=sa.BLOB(),
               nullable=True)
    op.alter_column('lib_books', 'book_id',
               existing_type=sa.BLOB(),
               nullable=True,
               autoincrement=True)
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    # ### end Alembic commands ###
