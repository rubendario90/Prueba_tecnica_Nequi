import pytest
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.message import MessageCreate, MessageMetadata, BogotaDateTime

def test_message_create_validators():
    # content vacío
    with pytest.raises(ValueError):
        MessageCreate(
            message_id="id1",
            session_id="sess1",
            content="   ",
            timestamp=datetime.now(ZoneInfo("America/Bogota")),
            sender="user"
        )
    # message_id vacío
    with pytest.raises(ValueError):
        MessageCreate(
            message_id="",
            session_id="sess1",
            content="Hola",
            timestamp=datetime.now(ZoneInfo("America/Bogota")),
            sender="user"
        )
    # session_id vacío
    with pytest.raises(ValueError):
        MessageCreate(
            message_id="id1",
            session_id="",
            content="Hola",
            timestamp=datetime.now(ZoneInfo("America/Bogota")),
            sender="user"
        )

def test_bogota_datetime_process_bind_param_naive():
    bogota_type = BogotaDateTime()
    dt = datetime(2025, 9, 25, 10, 0, 0)
    assert bogota_type.process_bind_param(dt, None) == dt

def test_bogota_datetime_process_bind_param_aware():
    bogota_type = BogotaDateTime()
    dt = datetime(2025, 9, 25, 10, 0, 0, tzinfo=ZoneInfo("America/Bogota"))
    result = bogota_type.process_bind_param(dt, None)
    assert result == dt.replace(tzinfo=None)

def test_bogota_datetime_process_bind_param_string():
    bogota_type = BogotaDateTime()
    dt_str = "2025-09-25T10:00:00Z"
    result = bogota_type.process_bind_param(dt_str, None)
    assert isinstance(result, datetime)
    assert result.year == 2025 and result.month == 9

def test_message_metadata_model():
    meta = MessageMetadata(word_count=2, character_count=10, processed_at=datetime.now(ZoneInfo("America/Bogota")))
    assert meta.word_count == 2