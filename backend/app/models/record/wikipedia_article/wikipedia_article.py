from app.models.record.record import Record
from app.models.record.wikipedia_article.category import Category
from app.models.record.wikipedia_article.external_links import ExternalLink


class WikipediaArticle(Record):

    categories: tuple[Category, ...] | None = None
    external_links: tuple[ExternalLink, ...] | None = None
