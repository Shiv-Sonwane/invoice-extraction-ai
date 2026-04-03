from datetime import datetime

def clean_amount(amount):
    if not amount:
        return None
    amount = str(amount).replace(",", "").replace("$", "").strip()
    try:
        return float(amount)
    except:
        return None


def clean_date(date_str):
    if not date_str:
        return None
    
    from datetime import datetime

def format_date(date_str):
    if not date_str:
        return None

    formats = [
        "%d.%m.%Y",
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d %B %Y",
        "%b %d, %Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except:
            continue

    return None  # fallback if all fail


def validate_invoice(data):
    return {
        "vendor_name": data.get("vendor_name", "").strip(),
        "invoice_number": data.get("invoice_number", "").strip(),
        "invoice_date": format_date(data.get("invoice_date")),
        "total_amount": float(str(data.get("total_amount", "0")).replace(",", "")),
        "currency": data.get("currency", "$")
    }