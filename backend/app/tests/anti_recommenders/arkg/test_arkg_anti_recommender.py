from app.anti_recommenders.arkg import ArkgAntiRecommender
from app.models import Record


def test_generate_anti_recommendations(
    arkg_anti_recommender: ArkgAntiRecommender,
    records: tuple[Record, ...],
) -> None:
    """Test that ArkgAntiRecommender.generate_anti_recommendations() yields AntiRecommendations of a given record key."""

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
