from pytest_mock import MockFixture

from app.anti_recommenders.arkg import ArkgAntiRecommender
from app.database.client import DatabaseClient
from app.models import Record


def test_generate_anti_recommendations(
    session_mocker: MockFixture,
    arkg_anti_recommender: ArkgAntiRecommender,
    records: tuple[Record, ...],
) -> None:
    """Test that ArkgAntiRecommender.generate_anti_recommendations() yields AntiRecommendations of a given record key."""

    session_mocker.patch.object(DatabaseClient, "upsert", return_value=None)

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
