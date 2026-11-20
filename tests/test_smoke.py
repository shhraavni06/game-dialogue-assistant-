from app.cli import build_model

def test_cli_model_builds():
    model = build_model()
    assert model.vocabulary
