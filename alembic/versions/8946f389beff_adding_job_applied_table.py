"""adding job_applied table

Revision ID: 8946f389beff
Revises: ecf080c9e2f8
Create Date: 2021-12-31 21:17:46.362065

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8946f389beff'
down_revision = 'ecf080c9e2f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jobs_applied',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('seeker_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['seeker_id'], ['seekers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_jobs_applied_id'), 'jobs_applied', ['id'], unique=False)
    op.drop_column('seekers', 'jobs_applied')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seekers', sa.Column('jobs_applied', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_jobs_applied_id'), table_name='jobs_applied')
    op.drop_table('jobs_applied')
    # ### end Alembic commands ###
