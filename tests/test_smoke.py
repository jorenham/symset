import pytest


def test_import_symset() -> None:
    try:
        import symset  # noqa: F401, PLC0415
    except Exception as e:  # noqa: BLE001
        pytest.fail(f"Failed to import symset: {e}")
