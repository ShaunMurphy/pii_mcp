# FastMCP Server with Presidio PII Redaction

## Overview

This project implements a Python 3.12 FastMCP server that uses Microsoft's Presidio to redact PII in both incoming and outgoing data.  
It features a Guardrails Middleware for PII redaction using Presidio and a stub Orchestrator Plugin.

## Features

- FastMCP server (requires fastmcp-server >=2.9.0)
- Presidio-based PII redaction middleware (names, emails, etc.)
- Example orchestrator plugin route
- Demo/test route for PII redaction
- Unit tests for middleware and plugin

## Setup

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```
   python main.py
   ```

3. **Test PII redaction:**
   - POST to `/mcp` with JSON:  
     `{ "input": "My name is John Doe and my email is john.doe@example.com" }`
   - The response will have PII redacted.

4. **Run tests:**
   ```
   pytest
   ```

## References

- FastMCP Middleware Docs: https://gofastmcp.com/servers/middleware
- Presidio: https://github.com/microsoft/presidio
