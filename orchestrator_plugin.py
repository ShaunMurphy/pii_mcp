from sfmc_plugin import get_email_templates, get_queries
import os

ENABLE_MLFLOW = os.getenv("ENABLE_MLFLOW", "false").lower() == "true"
if ENABLE_MLFLOW:
    import mlflow

def register_tool(mcp):
    @mcp.tool
    def sfmc_get_templates() -> dict:
        """
        Get all Salesforce Marketing Cloud email templates (read-only).
        """
        if ENABLE_MLFLOW:
            with mlflow.start_run(run_name="sfmc_get_templates"):
                mlflow.log_param("tool", "sfmc_get_templates")
                result = get_email_templates()
                mlflow.log_param("result", str(result))
                return result
        else:
            return get_email_templates()

    @mcp.tool
    def sfmc_get_queries() -> dict:
        """
        Get all Salesforce Marketing Cloud queries (read-only).
        """
        if ENABLE_MLFLOW:
            with mlflow.start_run(run_name="sfmc_get_queries"):
                mlflow.log_param("tool", "sfmc_get_queries")
                result = get_queries()
                mlflow.log_param("result", str(result))
                return result
        else:
            return get_queries()