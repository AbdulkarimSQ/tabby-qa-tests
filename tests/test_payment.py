"""
Test suite for Tabby-style payment processing
"""
import pytest
from app.payment import (
    calculate_installment, check_balance, process_installment,
    validate_email, calculate_total
)

class TestInstallmentCalculation:
    @pytest.mark.parametrize("total, installments, expected", [
        (1200, 4, 300.0),
        (900, 3, 300.0),
        (500, 2, 250.0),
        (1800, 6, 300.0),
    ])
    def test_valid_installments(self, total, installments, expected):
        assert calculate_installment(total, installments) == expected

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError):
            calculate_installment(-100, 4)

    def test_invalid_installment_count(self):
        with pytest.raises(ValueError):
            calculate_installment(1000, 5)

class TestBalanceCheck:
    @pytest.fixture
    def rich_user(self):
        return {"name": "Ahmed", "balance": 5000}

    @pytest.fixture
    def poor_user(self):
        return {"name": "Khalid", "balance": 100}

    def test_sufficient_balance(self, rich_user):
        result = check_balance(rich_user["balance"], 1200)
        assert result["approved"] == True
        assert result["remaining"] == 3800

    def test_insufficient_balance(self, poor_user):
        result = check_balance(poor_user["balance"], 500)
        assert result["approved"] == False
        assert result["shortage"] == 400

    def test_exact_balance(self, rich_user):
        result = check_balance(rich_user["balance"], 5000)
        assert result["approved"] == True
        assert result["remaining"] == 0

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError):
            check_balance(1000, -50)

class TestProcessInstallment:
    def test_first_installment_paid(self):
        result = process_installment(1200, 4, 1)
        assert result["installment"] == 300.0
        assert result["remaining"] == 900.0
        assert result["paid"] == 1

    def test_fully_paid(self):
        result = process_installment(900, 3, 3)
        assert result["installment"] == 300.0
        assert result["remaining"] == 0.0

    @pytest.mark.parametrize("total, installments, paid", [
        (-100, 2, 0),
        (500, 5, 0),
        (200, 2, 3),
    ])
    def test_invalid_inputs_raise(self, total, installments, paid):
        with pytest.raises(ValueError):
            process_installment(total, installments, paid)

class TestEmailValidation:
    @pytest.mark.parametrize("email, expected", [
        ("ahmed@tabby.ai", True),
        ("sara@mail.com", True),
        ("", False),
        ("no-at-sign", False),
        ("missing@dot", False),
        ("has space@mail.com", False),
        ("@mail.com", False),
        (None, False),
        (123, False),
    ])
    def test_email_validation(self, email, expected):
        assert validate_email(email) == expected

class TestCalculateTotal:
    def test_normal_purchase(self):
        assert calculate_total(100, 3, 10) == 270.0

    def test_no_discount(self):
        assert calculate_total(50, 4, 0) == 200.0

    def test_negative_price_raises(self):
        with pytest.raises(ValueError):
            calculate_total(-10, 2, 0)

    def test_invalid_discount_raises(self):
        with pytest.raises(ValueError):
            calculate_total(100, 2, 150)

    @pytest.mark.parametrize("price, qty, discount, expected", [
        (100, 3, 10, 270.0),
        (50, 4, 0, 200.0),
        (200, 1, 50, 100.0),
    ])
    def test_various_totals(self, price, qty, discount, expected):
        assert calculate_total(price, qty, discount) == expected
