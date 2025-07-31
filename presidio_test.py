from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()

text = (
    "My name is John Doe. My email is john.doe@example.com. "
    "My SSN is 123-45-6789. My credit card is 4111-1111-1111-1111. "
    "My password is hunter2. My phone number is 212-555-5555."
)

entities = [
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

results = analyzer.analyze(
    text=text,
    entities=entities,
    language="en"
)

print("Detected entities:")
for r in results:
    print(f"Type: {r.entity_type}, Text: '{text[r.start:r.end]}', Score: {r.score}")