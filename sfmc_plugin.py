import os
import logging
from FuelSDKWrapper import ET_API, ET_Get

def get_sfmc_client():
    try:
        params = {
            "client_id": os.environ["SFMC_CLIENT_ID"],
            "client_secret": os.environ["SFMC_CLIENT_SECRET"],
            "subdomain": os.environ["SFMC_SUBDOMAIN"],
        }
        return ET_API(params=params, debug=False)
    except KeyError as e:
        logging.error(f"Missing SFMC credential: {e}")
        raise RuntimeError(f"Missing SFMC credential: {e}")

def get_email_templates():
    try:
        client = get_sfmc_client()
        # Use ET_Get to fetch emails (templates)
        emails = ET_Get('Email', client)
        response = emails.get()
        return {"success": True, "templates": response}
    except Exception as e:
        logging.exception("Error fetching SFMC email templates")
        return {"success": False, "error": str(e)}

def get_queries():
    try:
        client = get_sfmc_client()
        # Use ET_Get to fetch queries
        queries = ET_Get('QueryDefinition', client)
        response = queries.get()
        return {"success": True, "queries": response}
    except Exception as e:
        logging.exception("Error fetching SFMC queries")
        return {"success": False, "error": str(e)}