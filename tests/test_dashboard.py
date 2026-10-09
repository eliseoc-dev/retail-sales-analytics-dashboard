from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DASHBOARD_PATH = (
    PROJECT_ROOT
    / "dashboard"
    / "app.py"
)


def test_dashboard_file_exists():
    assert DASHBOARD_PATH.exists()


def test_dashboard_contains_streamlit():
    content = DASHBOARD_PATH.read_text(
        encoding="utf-8"
    )

    assert "streamlit" in content
    assert "st.metric" in content or ".metric(" in content
    