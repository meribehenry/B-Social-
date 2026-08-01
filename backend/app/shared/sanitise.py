import bleach

def sanitise(text):
    if not text:
        return text
    return bleach.clean(str(text), tags=[], strip=True).strip()