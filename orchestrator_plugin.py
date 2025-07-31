from sfmc_plugin import get_email_templates, get_queries

def register_tool(mcp):
    @mcp.tool
    def sfmc_get_templates() -> dict:
        """
        Get all Salesforce Marketing Cloud email templates (read-only).
        """
        return get_email_templates()

    @mcp.tool
    def sfmc_get_queries() -> dict:
        """
        Get all Salesforce Marketing Cloud queries (read-only).
        """
        return get_queries()