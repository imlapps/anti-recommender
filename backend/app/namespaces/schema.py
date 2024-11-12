from pyoxigraph import NamedNode


class SCHEMA:
    """A class containing Schema.org RDF Nodes."""

    BASE_IRI = NamedNode("http://schema.org/")

    ABOUT = NamedNode(BASE_IRI.value + "about")
    ITEM_REVIEWED = NamedNode(BASE_IRI.value + "itemReviewed")
    NAME = NamedNode(BASE_IRI.value + "name")
    RECOMMENDATION = NamedNode(BASE_IRI.value + "Recommendation")
    SAME_AS = NamedNode(BASE_IRI.value + "sameAs")
    TEXT_OBJECT = NamedNode(BASE_IRI.value + "TextObject")
    THING = NamedNode(BASE_IRI.value + "Thing")
    URL = NamedNode(BASE_IRI.value + "url")
