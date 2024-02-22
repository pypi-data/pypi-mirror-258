"""
Create the get_org_from_ccx_course_url function to support CCX courses
"""
from alembic import op


revision = "0033"
down_revision = "0032"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""

def upgrade():
    op.execute(
        f"""
        CREATE OR REPLACE FUNCTION get_org_from_ccx_course_url {on_cluster}
        AS (
        course_url) ->
           nullIf(EXTRACT(course_url, 'ccx-v1:([a-zA-Z0-9]*)'), '');

        """
    )



def downgrade():
    op.execute("DROP FUNCTION IF EXISTS get_org_from_ccx_course_url;")
