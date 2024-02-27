"""
Run Tests on the Splitwise Plugin
"""

import json
import logging
from os import path

import pytest
import splitwise

from lunchable_splitlunch.lunchmoney_splitwise import SplitLunch, _get_splitwise_impact
from tests.conftest import lunchable_cassette

logger = logging.getLogger(__name__)


@pytest.mark.filterwarnings("ignore:datetime.datetime.utcfromtimestamp")
@lunchable_cassette
def test_update_balance() -> None:
    """
    Update the Balance
    """
    lunch = SplitLunch()
    lunch.update_splitwise_balance()


@pytest.mark.filterwarnings("ignore:datetime.datetime.utcfromtimestamp")
def test_financial_impact() -> None:
    """
    Test the financial impact algorithm
    """
    for [file, expected_self_paid, expected_impact] in [
        # For both expenses and transfers, when someone else pays,
        # financial impact should be positive
        ["splitwise_non_user_paid_expense.json", False, 9.99],
        ["splitwise_non_user_paid_transfer.json", False, 523.84],
        # When you pay, financial impact should be negative
        ["splitwise_user_paid_expense.json", True, -61.65],
        ["splitwise_user_paid_transfer.json", True, -431.92],
        # And any transaction that doesn't involve you should have no impact
        ["splitwise_non_involved_expense.json", False, 0],
        ["splitwise_non_involved_transfer.json", False, 0],
    ]:
        with open(path.join(path.dirname(__file__), f"data/{file}")) as json_file:
            expense = splitwise.Expense(json.load(json_file))
        financial_impact, self_paid = _get_splitwise_impact(
            expense=expense, current_user_id=1234059
        )
        assert (
            self_paid is expected_self_paid
        ), f"Expected {expected_self_paid} for {file}"
        assert (
            financial_impact == expected_impact
        ), f"Expected {expected_impact} for {file}"
