import random
import string

def generate_code(length=6):
    """Generuje unikalny kod quizu (np. A8D5FZ)."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))