from fastmcp.server.middleware import Middleware, MiddlewareContext
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult as AnonymizerRecognizerResult

DEFAULT_ENTITIES = [
    "EMAIL_ADDRESS",
    "CREDIT_CARD",
    "US_SOCIAL_SECURITY_NUMBER",
    "PHONE_NUMBER",
    "IP_ADDRESS",
    "US_BANK_NUMBER",
    "US_DRIVER_LICENSE",
    "US_PASSPORT",
    "DATE_TIME",
    "LOCATION",
    "MEDICAL_LICENSE",
    "CRYPTO",
]

def redact_text(text, analyzer, anonymizer, entities=DEFAULT_ENTITIES):
    results = analyzer.analyze(
        text=text,
        entities=entities,
        language="en"
    )
    print(f"[GuardrailsMiddleware] redact_text: '{text}'")
    print(f"[GuardrailsMiddleware] Detected entities: {[f'{r.entity_type}({text[r.start:r.end]})' for r in results]}")
    if results:
        converted = [
            AnonymizerRecognizerResult(
                entity_type=r.entity_type,
                start=r.start,
                end=r.end,
                score=r.score
            ) for r in results
        ]
        anonymized = anonymizer.anonymize(text=text, analyzer_results=converted)
        print(f"[GuardrailsMiddleware] Redacted: '{anonymized.text}'")
        return anonymized.text
    return text

def redact_dict(d, analyzer, anonymizer):
    # Recursively redact all string fields in a dict
    for key, value in d.items():
        if isinstance(value, str):
            d[key] = redact_text(value, analyzer, anonymizer)
        elif isinstance(value, dict):
            redact_dict(value, analyzer, anonymizer)
        elif isinstance(value, list):
            redact_list(value, analyzer, anonymizer)
    return d

def redact_list(lst, analyzer, anonymizer):
    # Recursively redact all string elements in a list
    for i, value in enumerate(lst):
        if isinstance(value, str):
            lst[i] = redact_text(value, analyzer, anonymizer)
        elif isinstance(value, dict):
            redact_dict(value, analyzer, anonymizer)
        elif isinstance(value, list):
            redact_list(value, analyzer, anonymizer)
    return lst

class GuardrailsMiddleware(Middleware):
    """
    Middleware for PII redaction using Presidio.
    Recursively redacts all string fields in dicts/lists.
    """

    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    async def __call__(self, context: MiddlewareContext, call_next):
        # Redact PII in incoming message (request)
        if hasattr(context, "message") and isinstance(context.message, dict):
            params = context.message.get("params")
            if isinstance(params, dict):
                redact_dict(params, self.analyzer, self.anonymizer)

        # Call the next middleware/handler
        try:
            result = await call_next(context)
        except Exception as e:
            print(f"[GuardrailsMiddleware] Error calling next middleware/handler: {e}")
            raise

        # Redact PII in outgoing result (response)
        if isinstance(result, dict):
            redact_dict(result, self.analyzer, self.anonymizer)

        return result