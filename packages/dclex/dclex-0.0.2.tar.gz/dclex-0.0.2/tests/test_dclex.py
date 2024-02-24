from datetime import date, timedelta
from decimal import Decimal
from time import sleep
from unittest.mock import ANY

import pytest
from eth_typing.encoding import HexStr
from web3 import Web3

from dclex.dclex import AccountStatus, Dclex
from dclex.types import (
    ClaimableWithdrawal,
    Order,
    OrderSide,
    OrderStatus,
    Portfolio,
    TransactionType,
    Transfer,
    TransferHistoryStatus,
)

sepolia_provider_url = "http://127.0.0.1:8545"
_PRIVATE_KEY = "7c852118294e51e653712a81e05800f419141751be58f605c371e15141b007a6"


def _wait_for_transaction(tx_hash: HexStr) -> None:
    Web3(Web3.HTTPProvider(sepolia_provider_url)).eth.wait_for_transaction_receipt(
        tx_hash
    )


@pytest.fixture(name="dclex")
def dclex_fixture() -> Dclex:
    return Dclex(private_key=_PRIVATE_KEY, web3_provider_url=sepolia_provider_url)


def test_login_and_logout(dclex):
    assert not dclex.logged_in()

    dclex.login()
    assert dclex.logged_in()

    dclex.logout()
    assert not dclex.logged_in()


def test_deposit_and_withdraw_usdc(dclex):
    dclex.login()

    usdc_available_balance_before = dclex.get_usdc_available_balance()
    usdc_ledger_balance_before = dclex.get_usdc_ledger_balance()

    tx_hash = dclex.deposit_usdc(amount=Decimal(100))
    _wait_for_transaction(tx_hash)

    sleep(3)

    assert dclex.get_usdc_ledger_balance() - usdc_ledger_balance_before == 100
    assert dclex.get_usdc_available_balance() - usdc_available_balance_before == 100

    tx_hash = dclex.withdraw_usdc(Decimal(100))
    _wait_for_transaction(tx_hash)

    sleep(3)

    assert dclex.get_usdc_ledger_balance() == usdc_ledger_balance_before
    assert dclex.get_usdc_available_balance() == usdc_available_balance_before


def test_withdraw_and_deposit_stock(dclex):
    dclex.login()

    tx_hash = dclex.deposit_usdc(Decimal(200))
    _wait_for_transaction(tx_hash)
    sleep(3)

    dclex.create_limit_order(OrderSide.BUY, "AAPL", 1, Decimal(190))
    sleep(30)

    aapl_available_balance_before = dclex.get_stock_available_balance("AAPL")
    aapl_ledger_balance_before = dclex.get_stock_ledger_balance("AAPL")

    tx_hash = dclex.withdraw_stock_token("AAPL", 1)
    _wait_for_transaction(tx_hash)
    sleep(3)

    assert (
        dclex.get_stock_available_balance("AAPL") - aapl_available_balance_before == -1
    )
    assert dclex.get_stock_ledger_balance("AAPL") - aapl_ledger_balance_before == -1

    tx_hash = dclex.deposit_stock_token("AAPL", 1)
    _wait_for_transaction(tx_hash)
    sleep(3)

    assert dclex.get_stock_available_balance("AAPL") == aapl_available_balance_before
    assert dclex.get_stock_ledger_balance("AAPL") == aapl_ledger_balance_before


def test_should_claim_digital_identity(dclex):
    dclex.login()

    tx_hash = dclex.claim_digital_identity()
    _wait_for_transaction(tx_hash)

    sleep(3)

    assert dclex.get_account_status() == AccountStatus.DID_MINTED


def test_create_buy_and_sell_limit_order(dclex):
    dclex.login()

    tx_hash = dclex.deposit_usdc(Decimal(200))
    _wait_for_transaction(tx_hash)

    aapl_available_balance_before = dclex.get_stock_available_balance("AAPL")
    aapl_ledger_balance_before = dclex.get_stock_ledger_balance("AAPL")

    dclex.create_limit_order(OrderSide.BUY, "AAPL", 1, Decimal(190))
    sleep(30)

    assert (
        dclex.get_stock_available_balance("AAPL") - aapl_available_balance_before == 1
    )
    assert dclex.get_stock_ledger_balance("AAPL") - aapl_ledger_balance_before == 1

    dclex.create_limit_order(
        OrderSide.SELL, "AAPL", 1, Decimal(190), date.today() + timedelta(days=10)
    )
    sleep(30)

    assert dclex.get_stock_available_balance("AAPL") == aapl_available_balance_before
    assert dclex.get_stock_ledger_balance("AAPL") == aapl_ledger_balance_before


def test_create_sell_market_order(dclex):
    dclex.login()

    tx_hash = dclex.deposit_usdc(Decimal(200))
    _wait_for_transaction(tx_hash)

    aapl_available_balance_before = dclex.get_stock_available_balance("AAPL")
    aapl_ledger_balance_before = dclex.get_stock_ledger_balance("AAPL")

    dclex.create_limit_order(OrderSide.BUY, "AAPL", 1, Decimal(190))
    sleep(30)

    assert (
        dclex.get_stock_available_balance("AAPL") - aapl_available_balance_before == 1
    )
    assert dclex.get_stock_ledger_balance("AAPL") - aapl_ledger_balance_before == 1

    dclex.create_sell_market_order("AAPL", 1)
    sleep(30)

    assert dclex.get_stock_available_balance("AAPL") == aapl_available_balance_before
    assert dclex.get_stock_ledger_balance("AAPL") == aapl_ledger_balance_before


def test_cancelling_orders(dclex):
    dclex.login()

    tx_hash = dclex.deposit_usdc(Decimal(200))
    _wait_for_transaction(tx_hash)
    sleep(3)

    usdc_available_balance_before = dclex.get_usdc_available_balance()
    usdc_ledger_balance_before = dclex.get_usdc_ledger_balance()
    aapl_available_balance_before = dclex.get_stock_available_balance("AAPL")
    aapl_ledger_balance_before = dclex.get_stock_ledger_balance("AAPL")

    order_id = dclex.create_limit_order(OrderSide.BUY, "AAPL", 1, Decimal(190))
    dclex.cancel_order(order_id)
    sleep(30)

    assert dclex.get_usdc_available_balance() == usdc_available_balance_before
    assert dclex.get_usdc_ledger_balance() == usdc_ledger_balance_before
    assert dclex.get_stock_available_balance("AAPL") == aapl_available_balance_before
    assert dclex.get_stock_ledger_balance("AAPL") == aapl_ledger_balance_before


def test_open_orders(dclex):
    dclex.login()

    tx_hash = dclex.deposit_usdc(Decimal(600))
    _wait_for_transaction(tx_hash)
    sleep(3)

    order_id_1 = dclex.create_limit_order(OrderSide.BUY, "AAPL", 1, Decimal(190))
    order_id_2 = dclex.create_limit_order(
        OrderSide.BUY, "AMZN", 2, Decimal(170), date.today() + timedelta(days=10)
    )

    open_orders = dclex.open_orders()
    assert len(open_orders) == 2
    assert open_orders[0] == Order(
        id=order_id_1,
        order_side=OrderSide.BUY,
        type="LIMIT",
        symbol="AAPL",
        quantity=1,
        price=Decimal(190),
        status=OrderStatus.PENDING,
        date_of_cancellation=None,
    )
    assert open_orders[1] == Order(
        id=order_id_2,
        order_side=OrderSide.BUY,
        type="LIMIT",
        symbol="AMZN",
        quantity=2,
        price=Decimal(170),
        status=OrderStatus.PENDING,
        date_of_cancellation=date.today() + timedelta(days=10),
    )

    dclex.cancel_order(order_id_2)
    sleep(30)
    assert dclex.open_orders() == []


def test_closed_orders(dclex):
    dclex.login()

    tx_hash = dclex.deposit_usdc(Decimal(600))
    _wait_for_transaction(tx_hash)
    sleep(3)
    closed_orders_len_before = len(dclex.closed_orders())

    order_id_1 = dclex.create_limit_order(OrderSide.BUY, "AAPL", 1, Decimal(190))
    order_id_2 = dclex.create_limit_order(
        OrderSide.BUY, "AMZN", 2, Decimal(170), date.today() + timedelta(days=10)
    )

    closed_orders_id = {order.id for order in dclex.closed_orders()}
    assert order_id_1 not in closed_orders_id
    assert order_id_2 not in closed_orders_id

    dclex.cancel_order(order_id_2)
    sleep(30)

    closed_orders = {order.id: order for order in dclex.closed_orders()}
    assert len(closed_orders) == closed_orders_len_before + 2
    assert closed_orders[order_id_1] == Order(
        id=order_id_1,
        order_side=OrderSide.BUY,
        type="LIMIT",
        symbol="AAPL",
        quantity=1,
        price=Decimal(190),
        status=OrderStatus.EXECUTED,
        date_of_cancellation=None,
    )
    assert closed_orders[order_id_2] == Order(
        id=order_id_2,
        order_side=OrderSide.BUY,
        type="LIMIT",
        symbol="AMZN",
        quantity=2,
        price=Decimal(170),
        status=OrderStatus.CANCELED,
        date_of_cancellation=date.today() + timedelta(days=10),
    )


def test_usdc_pending_transfers(dclex):
    dclex.login()

    assert dclex.pending_transfers() == []

    tx_hash = dclex.deposit_usdc(Decimal(100))
    _wait_for_transaction(tx_hash)
    sleep(3)
    assert dclex.pending_transfers() == [
        Transfer(
            ANY,
            Decimal(100),
            "USDC",
            TransactionType.DEPOSIT,
            TransferHistoryStatus.PENDING,
        )
    ]

    sleep(10)
    assert dclex.pending_transfers() == []

    tx_hash = dclex.withdraw_usdc(Decimal(100))
    assert dclex.pending_transfers() == [
        Transfer(
            ANY,
            Decimal(100),
            "USDC",
            TransactionType.WITHDRAWAL,
            TransferHistoryStatus.CLAIMABLE,
        )
    ]
    _wait_for_transaction(tx_hash)
    sleep(3)
    assert dclex.pending_transfers() == []


def test_usdc_closed_transfers(dclex):
    dclex.login()
    deposit_tx_hash = dclex.deposit_usdc(Decimal(100))
    _wait_for_transaction(deposit_tx_hash)
    sleep(2)
    withdrawal_tx_hash = dclex.withdraw_usdc(Decimal(100))
    _wait_for_transaction(withdrawal_tx_hash)
    sleep(2)

    closed_transfers = {
        transfer.transaction_id: transfer for transfer in dclex.closed_transfers()
    }
    assert closed_transfers[deposit_tx_hash] == Transfer(
        deposit_tx_hash,
        Decimal(100),
        "USDC",
        TransactionType.DEPOSIT,
        TransferHistoryStatus.DONE,
    )
    assert closed_transfers[withdrawal_tx_hash] == Transfer(
        withdrawal_tx_hash,
        Decimal(100),
        "USDC",
        TransactionType.WITHDRAWAL,
        TransferHistoryStatus.DONE,
    )


def test_stock_token_pending_transfers(dclex):
    dclex.login()
    _wait_for_transaction(dclex.deposit_usdc(Decimal(200)))
    sleep(2)
    dclex.create_limit_order(OrderSide.BUY, "AAPL", 1, Decimal(190))
    sleep(30)

    dclex.withdraw_stock_token("AAPL", 1)
    assert dclex.pending_transfers() == [
        Transfer(
            None,
            Decimal(1),
            "AAPL",
            TransactionType.WITHDRAWAL,
            TransferHistoryStatus.CLAIMABLE,
        )
    ]
    sleep(3)

    assert dclex.pending_transfers() == []


def test_stock_token_closed_transfers(dclex):
    dclex.login()
    _wait_for_transaction(dclex.deposit_usdc(Decimal(200)))
    sleep(2)
    dclex.create_limit_order(OrderSide.BUY, "AAPL", 1, Decimal(190))
    sleep(30)

    withdrawal_tx_hash = dclex.withdraw_stock_token("AAPL", 1)
    _wait_for_transaction(withdrawal_tx_hash)
    sleep(2)
    deposit_tx_hash = dclex.deposit_stock_token("AAPL", 1)
    _wait_for_transaction(deposit_tx_hash)
    sleep(2)

    closed_transfers = {
        transfer.transaction_id: transfer for transfer in dclex.closed_transfers()
    }
    assert closed_transfers[deposit_tx_hash] == Transfer(
        deposit_tx_hash,
        Decimal(1),
        "AAPL",
        TransactionType.DEPOSIT,
        TransferHistoryStatus.DONE,
    )
    assert closed_transfers[withdrawal_tx_hash] == Transfer(
        withdrawal_tx_hash,
        Decimal(1),
        "AAPL",
        TransactionType.WITHDRAWAL,
        TransferHistoryStatus.DONE,
    )


def test_should_get_portfolio(dclex):
    dclex.login()

    assert dclex.portfolio() == Portfolio(
        available=ANY,
        equity=ANY,
        funds=ANY,
        profit_loss=ANY,
        total_value=ANY,
        stocks=ANY,
    )
