# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["SubscriptionSendSimulatedExampleParams"]


class SubscriptionSendSimulatedExampleParams(TypedDict, total=False):
    event_type: Literal[
        "account_holder.created",
        "account_holder.updated",
        "account_holder.verification",
        "balance.updated",
        "card.created",
        "card.renewed",
        "card.shipped",
        "card_transaction.updated",
        "digital_wallet.tokenization_approval_request",
        "digital_wallet.tokenization_result",
        "digital_wallet.tokenization_two_factor_authentication_code",
        "dispute.updated",
        "dispute_evidence.upload_failed",
        "payment_transaction.created",
        "payment_transaction.updated",
        "three_ds_authentication.created",
        "transfer_transaction.created",
    ]
    """Event type to send example message for."""
