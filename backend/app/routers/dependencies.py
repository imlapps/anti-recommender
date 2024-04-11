def next_records_parameters(record_key: str, record_type: str) -> dict[str, str]:
    """Return parameters for the next_records endpoint."""
    return {"record_key": record_key, "record_type": record_type}
