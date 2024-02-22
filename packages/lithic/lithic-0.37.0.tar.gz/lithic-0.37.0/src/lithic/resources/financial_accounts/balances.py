# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import Union
from datetime import datetime

import httpx

from ... import _legacy_response
from ...types import Balance
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...pagination import SyncSinglePage, AsyncSinglePage
from ..._base_client import (
    AsyncPaginator,
    make_request_options,
)
from ...types.financial_accounts import balance_list_params

__all__ = ["Balances", "AsyncBalances"]


class Balances(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BalancesWithRawResponse:
        return BalancesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BalancesWithStreamingResponse:
        return BalancesWithStreamingResponse(self)

    def list(
        self,
        financial_account_token: str,
        *,
        balance_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        last_transaction_event_token: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncSinglePage[Balance]:
        """
        Get the balances for a given financial account.

        Args:
          balance_date: UTC date of the balance to retrieve. Defaults to latest available balance

          last_transaction_event_token: Balance after a given financial event occured. For example, passing the
              event_token of a $5 CARD_CLEARING financial event will return a balance
              decreased by $5

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not financial_account_token:
            raise ValueError(
                f"Expected a non-empty value for `financial_account_token` but received {financial_account_token!r}"
            )
        return self._get_api_list(
            f"/financial_accounts/{financial_account_token}/balances",
            page=SyncSinglePage[Balance],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "balance_date": balance_date,
                        "last_transaction_event_token": last_transaction_event_token,
                    },
                    balance_list_params.BalanceListParams,
                ),
            ),
            model=Balance,
        )


class AsyncBalances(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBalancesWithRawResponse:
        return AsyncBalancesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBalancesWithStreamingResponse:
        return AsyncBalancesWithStreamingResponse(self)

    def list(
        self,
        financial_account_token: str,
        *,
        balance_date: Union[str, datetime] | NotGiven = NOT_GIVEN,
        last_transaction_event_token: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[Balance, AsyncSinglePage[Balance]]:
        """
        Get the balances for a given financial account.

        Args:
          balance_date: UTC date of the balance to retrieve. Defaults to latest available balance

          last_transaction_event_token: Balance after a given financial event occured. For example, passing the
              event_token of a $5 CARD_CLEARING financial event will return a balance
              decreased by $5

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not financial_account_token:
            raise ValueError(
                f"Expected a non-empty value for `financial_account_token` but received {financial_account_token!r}"
            )
        return self._get_api_list(
            f"/financial_accounts/{financial_account_token}/balances",
            page=AsyncSinglePage[Balance],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "balance_date": balance_date,
                        "last_transaction_event_token": last_transaction_event_token,
                    },
                    balance_list_params.BalanceListParams,
                ),
            ),
            model=Balance,
        )


class BalancesWithRawResponse:
    def __init__(self, balances: Balances) -> None:
        self._balances = balances

        self.list = _legacy_response.to_raw_response_wrapper(
            balances.list,
        )


class AsyncBalancesWithRawResponse:
    def __init__(self, balances: AsyncBalances) -> None:
        self._balances = balances

        self.list = _legacy_response.async_to_raw_response_wrapper(
            balances.list,
        )


class BalancesWithStreamingResponse:
    def __init__(self, balances: Balances) -> None:
        self._balances = balances

        self.list = to_streamed_response_wrapper(
            balances.list,
        )


class AsyncBalancesWithStreamingResponse:
    def __init__(self, balances: AsyncBalances) -> None:
        self._balances = balances

        self.list = async_to_streamed_response_wrapper(
            balances.list,
        )
