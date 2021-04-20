import pytest
from fastapi.testclient import TestClient

from main import app
from loan_application import LoanApplication


class TestApp:
    """Tests checking the API returns expected responses"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_sucessful_response_plan1(self, client):
        response  = client.get("/12/1000")
        assert response.status_code == 200
        assert response.json() == {"fee": 50}

    def test_sucessful_response_plan2(self, client):
        response  = client.get("/24/20000")
        assert response.status_code == 200
        assert response.json() == {"fee": 800}

    def test_invalid_months(self, client):
        response  = client.get("/15/4500.00")
        assert response.status_code == 422

    def test_invalid_large_amount(self, client):
        response  = client.get("/12/21000")
        assert response.status_code == 422

    def test_invalid_small_amount(self, client):
        response  = client.get("/12/500")
        assert response.status_code == 422


class TestLoanApplication:
    """Tests for methods of the LoanApplication class.
    Each test asserts that the fee is as expexted,
    and where applicable that the fee + loan amount is 
    a multiple of 5"""

    def test_fee_calc_12mon_boundary_amount(self):
        amount = 1000
        loan_app = LoanApplication(12, amount)
        fee = loan_app.fee()
        assert fee == 50
        assert (fee + amount) % 5 == 0

    def test_fee_calc_12mon_amount_within_interval(self):
        amount = 1800
        loan_app = LoanApplication(12, amount)
        fee = loan_app.fee()
        # 0.8 * (90 - 50) = 32
        # 1800 + (50 + 32) = 1882 ~ 1880
        # 1880 - 1800 = 80
        assert fee == 80
        assert (fee + amount) % 5 == 0

    def test_fee_calc_12mon_decimal_amount(self):
        amount = 4354.66
        loan_app = LoanApplication(12, amount)
        fee = loan_app.fee()
        # 0.354.66 * (100 - 115) = -5.32
        # 4354.66 + (115 - 5.32) = 4464.34 ~ 4465
        # 4354.66 + 4354.66 = 110.34
        assert fee == 110.34
        assert (fee + amount) % 5 == 0

    def test_fee_calc_24mon_boundary_amount(self):
        amount = 2000
        loan_app = LoanApplication(24, amount)
        fee = loan_app.fee()
        assert fee == 100
        assert (fee + amount) % 5 == 0

    def test_fee_calc_24mon_amount_within_interval(self):
        amount = 17500
        loan_app = LoanApplication(24, amount)
        fee = loan_app.fee()
        assert fee == 700
        assert (fee + amount) % 5 == 0

    def test_fee_calc_24mon_decimal_amount(self):
        amount = 2812.90
        loan_app = LoanApplication(24, amount)
        fee = loan_app.fee()
        # 0.81289 * (120 -100) = 16.26
        # 2812.90 + (100 + 16.26) = 2929.16 ~ 2930
        # 2930 - 2812.90 = 117.10
        assert fee == 117.10
        assert (fee + amount) % 5 == 0

    def test_fee_calc_no_fee_set(self):
        loan_app = LoanApplication(15, 1000)
        assert loan_app.fee() == None

    def test_fee_calc_amount_below_range(self):
        amount = 999.99
        loan_app1 = LoanApplication(24, amount)
        loan_app2 = LoanApplication(24, amount)
        assert loan_app1.fee() == None
        assert loan_app2.fee() == None

    def test_fee_calc_amount_above_range(self):
        amount = 20000.01
        loan_app1 = LoanApplication(24, amount)
        loan_app2 = LoanApplication(24, amount)
        assert loan_app1.fee() == None
        assert loan_app2.fee() == None  
