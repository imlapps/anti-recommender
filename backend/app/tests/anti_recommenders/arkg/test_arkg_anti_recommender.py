from postgrest import APIResponse
from pytest_mock import MockFixture

from app.anti_recommenders.arkg import ArkgAntiRecommender
from app.database.supabase import SupabaseDatabaseService, SupabaseUpsertQueryResult
from app.models import Record


def test_generate_anti_recommendations(
    session_mocker: MockFixture,
    arkg_anti_recommender: ArkgAntiRecommender,
    records: tuple[Record, ...],
) -> None:
    """Test that ArkgAntiRecommender.generate_anti_recommendations() yields AntiRecommendations of a given record key."""

    session_mocker.patch.object(
        SupabaseDatabaseService,
        "command",
        return_value=SupabaseUpsertQueryResult(APIResponse(data=[{"name": "N/A"}])),
    )

    assert (
        records[1].key
        == next(
            iter(
                arkg_anti_recommender.generate_anti_recommendations(
                    record_key=records[0].key
                )
            )
        ).key
    )
