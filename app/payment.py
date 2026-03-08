"""
Payment processing module — Tabby-style installment logic
"""


def calculate_installment(total_price, num_installments):
    if total_price <= 0:
        raise ValueError("Amount must be positive")
    if num_installments not in [2, 3, 4, 6]:
        raise ValueError("Installments must be 2, 3, 4, or 6")
    return round(total_price / num_installments, 2)


def check_balance(user_balance, purchase_amount):
    if purchase_amount <= 0:
        raise ValueError("Amount must be positive")
    if user_balance < purchase_amount:
        return {"approved": False, "remaining": user_balance, "shortage": purchase_amount - user_balance}
    return {"approved": True, "remaining": user_balance - purchase_amount}


def process_installment(total_amount, num_installments, paid_count):
    if total_amount <= 0:
        raise ValueError("Amount must be positive")
    if num_installments not in [2, 3, 4, 6]:
        raise ValueError("Invalid installment count")
    if paid_count < 0 or paid_count > num_installments:
        raise ValueError("Invalid paid count")
    installment = round(total_amount / num_installments, 2)
    remaining = round(total_amount - (installment * paid_count), 2)
    return {"installment": installment, "remaining": remaining, "paid": paid_count}


def validate_email(email):
    if not email or not isinstance(email, str):
        return False
    if " " in email:
        return False
    if "@" not in email:
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    if "." not in parts[1]:
        return False
    if len(parts[0]) == 0 or len(parts[1]) < 3:
        return False
    return True


def calculate_total(price, quantity, discount=0):
    if price < 0 or quantity < 0:
        raise ValueError("Values must be positive")
    if discount < 0 or discount > 100:
        raise ValueError("Discount must be between 0 and 100")
    total = price * quantity
    total = total - (total * discount / 100)
    return round(total, 2)
