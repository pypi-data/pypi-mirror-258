# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PaymentSimulateReleaseParams"]


class PaymentSimulateReleaseParams(TypedDict, total=False):
    payment_token: Required[str]
