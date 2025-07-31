# Security Considerations for PII Redacting FastMCP Server with SFMC Integration

## Overview

This project is designed with privacy and security as top priorities. It orchestrates Salesforce Marketing Cloud (SFMC) operations via FastMCP, with all incoming and outgoing data protected by PII redaction middleware. The following security practices are implemented to safeguard sensitive information and credentials.

---

## PII Redaction

- **Presidio Middleware:** All requests and responses are filtered through Microsoft Presidio, automatically redacting emails, credit cards, SSNs, and other personally identifiable information (PII).
- **Defense in Depth:** PII is never exposed to orchestration logic, logs, or external systems, reducing risk of data leakage.

---

## Secrets Management

- **Environment Variables:** All sensitive credentials (e.g., SFMC Client ID, Client Secret, Subdomain) are loaded from environment variables, never hardcoded or stored in source code or configuration files.
- **Why Environment Variables?**
  - **Separation of Code and Secrets:** Keeps secrets out of version control and codebase, reducing risk of accidental exposure.
  - **Easier Rotation:** Credentials can be rotated without code changes or redeployments.
  - **Integration with Secret Managers:** Compatible with Docker, Kubernetes, CI/CD pipelines, and cloud secret managers (AWS Secrets Manager, Azure Key Vault, etc.).
  - **Least Privilege:** Only the running process has access to secrets, minimizing attack surface.

---

## Credential Handling

- **No Logging of Secrets:** Credentials are never logged or exposed in error messages.
- **No Persistent Storage:** Secrets are not written to disk or persistent storage.
- **Runtime Only:** Secrets exist only in memory during process execution.

---

## Dependency Security

- **Pinned Versions:** All dependencies are pinned in `requirements.txt` to avoid supply chain attacks.
- **Regular Updates:** Dependencies should be regularly updated to patch vulnerabilities.
- **Trusted Sources:** Only official or vetted forks of FuelSDKWrapper and Salesforce-FuelSDK-Sans are used.

---

## Network Security

- **TLS/HTTPS:** All communication with SFMC and FastMCP should use TLS/HTTPS to prevent interception.
- **Firewall/Access Controls:** Restrict access to the FastMCP server and SFMC endpoints to trusted networks.

---

## Recommendations

- **Use a Secret Manager:** For production, inject environment variables from a secret manager (AWS, Azure, GCP, HashiCorp Vault).
- **Audit Logs:** Monitor access and usage logs for suspicious activity.
- **Rotate Credentials:** Regularly rotate SFMC credentials and other secrets.
- **Review PII Redaction:** Periodically audit redaction rules to ensure coverage of new PII types.

---

## References

- [Twelve-Factor App: Store config in the environment](https://12factor.net/config)
- [Microsoft Presidio](https://microsoft.github.io/presidio/)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
