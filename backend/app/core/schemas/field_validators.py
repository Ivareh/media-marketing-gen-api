from datetime import datetime, timezone


def datetime_hour_utc_offset(timestamp: datetime | None):
    if not timestamp:
        return

    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    utc_value = timestamp.astimezone(timezone.utc)
    # Format as ISO 8601 string with +00:00 offset
    return utc_value.isoformat()
