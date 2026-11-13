"""Track match requests, acceptance, and decline state (FR-7, NFR-6, NFR-22).

Revision ID: 0005
Revises: 0004
"""

import sqlalchemy as sa

from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("match_records") as batch_op:
        batch_op.add_column(
            sa.Column(
                "request_status",
                sa.String(length=20),
                server_default="recommended",
                nullable=False,
            )
        )
        batch_op.add_column(sa.Column("requester_user_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_match_records_requester_user_id_users",
            "users",
            ["requester_user_id"],
            ["id"],
            ondelete="SET NULL",
        )
        batch_op.create_check_constraint(
            "ck_match_records_request_status",
            "request_status IN ('recommended', 'pending', 'accepted', 'declined')",
        )

    op.execute(
        sa.text(
            """
            UPDATE match_records
            SET request_status = 'accepted',
                requester_user_id = (
                    SELECT founder_profiles.user_id
                    FROM startups
                    JOIN founder_profiles ON founder_profiles.id = startups.founder_profile_id
                    WHERE startups.id = match_records.startup_id
                )
            WHERE founder_accepted IS TRUE AND candidate_accepted IS TRUE
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE match_records
            SET request_status = 'pending',
                requester_user_id = CASE
                    WHEN founder_accepted IS TRUE THEN (
                        SELECT founder_profiles.user_id
                        FROM startups
                        JOIN founder_profiles ON founder_profiles.id = startups.founder_profile_id
                        WHERE startups.id = match_records.startup_id
                    )
                    ELSE candidate_user_id
                END
            WHERE (founder_accepted IS TRUE AND candidate_accepted IS FALSE)
               OR (founder_accepted IS FALSE AND candidate_accepted IS TRUE)
            """
        )
    )


def downgrade() -> None:
    with op.batch_alter_table("match_records") as batch_op:
        batch_op.drop_constraint("ck_match_records_request_status", type_="check")
        batch_op.drop_constraint(
            "fk_match_records_requester_user_id_users", type_="foreignkey"
        )
        batch_op.drop_column("requester_user_id")
        batch_op.drop_column("request_status")
