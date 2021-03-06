"""Base Datamodel

Revision ID: ecf080c9e2f8
Revises: 
Create Date: 2021-12-31 12:01:15.635320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecf080c9e2f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recruiters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recruiters_id'), 'recruiters', ['id'], unique=False)
    op.create_table('seekers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('jobs_applied', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('resume', sa.String(), nullable=False),
    sa.Column('portfolio', sa.String(), nullable=True),
    sa.Column('job_field', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_seekers_id'), 'seekers', ['id'], unique=False)
    op.create_table('jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('posted_by', sa.Integer(), nullable=False),
    sa.Column('posted_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('eligibility_Criteria', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('job_type', sa.String(), nullable=False),
    sa.Column('experience_level', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['posted_by'], ['recruiters.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_jobs_id'), 'jobs', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_jobs_id'), table_name='jobs')
    op.drop_table('jobs')
    op.drop_index(op.f('ix_seekers_id'), table_name='seekers')
    op.drop_table('seekers')
    op.drop_index(op.f('ix_recruiters_id'), table_name='recruiters')
    op.drop_table('recruiters')
    # ### end Alembic commands ###
