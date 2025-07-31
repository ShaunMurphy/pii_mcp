import pytest
import sfmc_plugin
import logging

class DummyGet:
    def get(self):
        return [{"id": "1", "name": "Welcome"}]

class DummyClient:
    pass

def test_get_email_templates(monkeypatch):
    """
    Test that get_email_templates returns a list of templates when ET_Get and get_sfmc_client are patched.
    Ensures the plugin logic works and returns expected mock data.
    """
    monkeypatch.setattr(sfmc_plugin, "get_sfmc_client", lambda: DummyClient())
    monkeypatch.setattr(sfmc_plugin, "ET_Get", lambda *args, **kwargs: DummyGet())
    result = sfmc_plugin.get_email_templates()
    assert result["success"] is True
    assert isinstance(result["templates"], list)
    assert result["templates"][0]["name"] == "Welcome"

def test_get_queries(monkeypatch):
    """
    Test that get_queries returns a list of queries when ET_Get and get_sfmc_client are patched.
    Ensures the plugin logic works and returns expected mock data.
    """
    monkeypatch.setattr(sfmc_plugin, "get_sfmc_client", lambda: DummyClient())
    monkeypatch.setattr(sfmc_plugin, "ET_Get", lambda *args, **kwargs: DummyGet())
    result = sfmc_plugin.get_queries()
    assert result["success"] is True
    assert isinstance(result["queries"], list)
    assert result["queries"][0]["name"] == "Welcome"  # Adjust as needed

def test_missing_env(monkeypatch):
    """
    Test that get_sfmc_client raises RuntimeError when required environment variables are missing.
    Ensures proper error handling for missing credentials.
    """
    monkeypatch.delenv("SFMC_CLIENT_ID", raising=False)
    monkeypatch.delenv("SFMC_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("SFMC_SUBDOMAIN", raising=False)
    with pytest.raises(RuntimeError):
        sfmc_plugin.get_sfmc_client()

def test_no_credentials_in_logs(monkeypatch, caplog):
    """
    Test that no credentials are present in logs when get_sfmc_client fails due to missing environment variables.
    Ensures secrets are not leaked in logs.
    """
    monkeypatch.delenv("SFMC_CLIENT_ID", raising=False)
    monkeypatch.delenv("SFMC_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("SFMC_SUBDOMAIN", raising=False)
    with caplog.at_level(logging.ERROR):
        try:
            sfmc_plugin.get_sfmc_client()
        except RuntimeError:
            pass
    # Ensure no credentials are present in logs
    for record in caplog.records:
        assert "SFMC_CLIENT_ID" not in record.getMessage()
        assert "SFMC_CLIENT_SECRET" not in record.getMessage()
        assert "SFMC_SUBDOMAIN" not in record.getMessage()