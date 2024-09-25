from pytest_mock import MockFixture

from app.anti_recommenders.arkg import ArkgAntiRecommender
from app.models import AntiRecommendation
from app.models.types import RecordKey, RecordType


def test_generate_anti_recommendations(
    arkg_anti_recommendations: tuple[AntiRecommendation, ...],
    arkg_anti_recommender: ArkgAntiRecommender,
    arkg_record_keys: tuple[RecordKey, ...],
) -> None:
    """Test that ArkgAntiRecommender.generate_anti_recommendations() yields AntiRecommendations of a given record key."""

    assert (
        arkg_anti_recommendations[0].key
        == tuple(
            arkg_anti_recommender.generate_anti_recommendations(
                record_key=arkg_record_keys[0]
            )
        )[-1].key
    )
