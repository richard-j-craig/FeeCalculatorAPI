import pytest
from fastapi.testclient import TestClient

from main import app
from functions import plan_lookup, fee_calculator


class TestMain:

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_sucessful_response_plan1(self, client):
        response  = client.get("/12/1000")
        assert response.status_code == 200
        assert response.json() == {
            "months": 12,
            "amount": 1000,
            "fee": 50
        }

    def test_sucessful_response_plan2(self, client):
        response  = client.get("/24/20000")
        assert response.status_code == 200
        assert response.json() == {
            "months": 24,
            "amount": 20000,
            "fee": 800
        }

    def test_invalid_months(self, client):
        response  = client.get("/15/4500.00")
        assert response.status_code == 422

    def test_invalid_large_amount(self, client):
        response  = client.get("/12/21000")
        assert response.status_code == 422

    def test_invalid_small_amount(self, client):
        response  = client.get("/12/500")
        assert response.status_code == 422


class TestFunctions:

    @pytest.fixture
    def plan_1(self):
        return [
            [1000, 50],
            [2000, 90],
            [3000, 90],
            [4000, 115],
            [5000, 100],
            [20000, 400]
        ]

    @pytest.fixture
    def plan_2(self):
        return [
            [1000, 70],
            [2000, 100],
            [3000, 120],
            [20000, 800]
        ]

    # Tests for plan_lookup function

    def test_plan_lookup_12_months(self, plan_1):
        assert plan_lookup(12) == plan_1

    def test_plan_lookup_24_months(self, plan_2):
        assert plan_lookup(24) == plan_2

    def test_plan_lookup_invalid_months(self):
        assert plan_lookup(15) == None

    # Tests for fee_calculator function
    # Each test asserts that the fee is as expexted,
    # and additionally that the fee + loan amount is 
    # a multiple of 5.

    def test_fee_calc_plan1_boundary_amount(self, plan_1):
        amount = 1000
        fee = fee_calculator(plan_1, amount)
        assert fee == 50
        assert (fee + amount) % 5 == 0

    def test_fee_calc_plan1_amount_within_interval(self, plan_1):
        amount = 1800
        fee = fee_calculator(plan_1, amount)
        # 0.8 * (90 - 50) = 32
        # 1800 + (50 + 32) = 1882 ~ 1880
        # 1880 - 1800 = 80
        assert fee == 80
        assert (fee + amount) % 5 == 0

    def test_fee_calc_plan1_decimal_amount(self, plan_1):
        amount = 4354.66
        fee = fee_calculator(plan_1, amount)
        # 0.354.66 * (100 - 115) = -5.32
        # 4354.66 + (115 - 5.32) = 4464.34 ~ 4465
        # 4354.66 + 4354.66 = 110.34
        assert fee == 110.34
        assert (fee + amount) % 5 == 0

    def test_fee_calc_plan2_boundary_amount(self, plan_2):
        amount = 2000
        fee = fee_calculator(plan_2, amount)
        assert fee == 100
        assert (fee + amount) % 5 == 0

    def test_fee_calc_plan2_amount_within_interval(self, plan_2):
        amount = 17500
        fee = fee_calculator(plan_2, amount)
        assert fee == 700
        assert (fee + amount) % 5 == 0

    def test_fee_calc_plan2_decimal_amount(self, plan_2):
        amount = 2812.90
        fee = fee_calculator(plan_2, amount)
        # 0.81289 * (120 -100) = 16.26
        # 2812.90 + (100 + 16.26) = 2929.16 ~ 2930
        # 2930 - 2812.90 = 117.10
        assert fee == 117.10
        assert (fee + amount) % 5 == 0

    def test_fee_calc_amount_below_range(self, plan_1, plan_2):
        assert fee_calculator(plan_1, 999.99) == None
        assert fee_calculator(plan_2, 999.99) == None

    def test_fee_calc_amount_above_range(self, plan_1, plan_2):
        assert fee_calculator(plan_1, 20000.01) == None
        assert fee_calculator(plan_2, 20000.01) == None    
