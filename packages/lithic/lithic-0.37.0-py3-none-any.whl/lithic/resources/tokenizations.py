# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from .. import _legacy_response
from ..types import TokenizationSimulateResponse, tokenization_simulate_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from .._base_client import (
    make_request_options,
)

__all__ = ["Tokenizations", "AsyncTokenizations"]


class Tokenizations(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TokenizationsWithRawResponse:
        return TokenizationsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TokenizationsWithStreamingResponse:
        return TokenizationsWithStreamingResponse(self)

    def simulate(
        self,
        *,
        cvv: str,
        expiration_date: str,
        pan: str,
        tokenization_source: Literal["APPLE_PAY", "GOOGLE", "SAMSUNG_PAY"],
        account_score: int | NotGiven = NOT_GIVEN,
        device_score: int | NotGiven = NOT_GIVEN,
        wallet_recommended_decision: Literal["APPROVED", "DECLINED", "REQUIRE_ADDITIONAL_AUTHENTICATION"]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TokenizationSimulateResponse:
        """
        This endpoint is used to simulate a card's tokenization in the Digital Wallet
        and merchant tokenization ecosystem.

        Args:
          cvv: The three digit cvv for the card.

          expiration_date: The expiration date of the card in 'MM/YY' format.

          pan: The sixteen digit card number.

          tokenization_source: The source of the tokenization request.

          account_score: The account score (1-5) that represents how the Digital Wallet's view on how
              reputable an end user's account is.

          device_score: The device score (1-5) that represents how the Digital Wallet's view on how
              reputable an end user's device is.

          wallet_recommended_decision: The decision that the Digital Wallet's recommend

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/simulate/tokenizations",
            body=maybe_transform(
                {
                    "cvv": cvv,
                    "expiration_date": expiration_date,
                    "pan": pan,
                    "tokenization_source": tokenization_source,
                    "account_score": account_score,
                    "device_score": device_score,
                    "wallet_recommended_decision": wallet_recommended_decision,
                },
                tokenization_simulate_params.TokenizationSimulateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TokenizationSimulateResponse,
        )


class AsyncTokenizations(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTokenizationsWithRawResponse:
        return AsyncTokenizationsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTokenizationsWithStreamingResponse:
        return AsyncTokenizationsWithStreamingResponse(self)

    async def simulate(
        self,
        *,
        cvv: str,
        expiration_date: str,
        pan: str,
        tokenization_source: Literal["APPLE_PAY", "GOOGLE", "SAMSUNG_PAY"],
        account_score: int | NotGiven = NOT_GIVEN,
        device_score: int | NotGiven = NOT_GIVEN,
        wallet_recommended_decision: Literal["APPROVED", "DECLINED", "REQUIRE_ADDITIONAL_AUTHENTICATION"]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TokenizationSimulateResponse:
        """
        This endpoint is used to simulate a card's tokenization in the Digital Wallet
        and merchant tokenization ecosystem.

        Args:
          cvv: The three digit cvv for the card.

          expiration_date: The expiration date of the card in 'MM/YY' format.

          pan: The sixteen digit card number.

          tokenization_source: The source of the tokenization request.

          account_score: The account score (1-5) that represents how the Digital Wallet's view on how
              reputable an end user's account is.

          device_score: The device score (1-5) that represents how the Digital Wallet's view on how
              reputable an end user's device is.

          wallet_recommended_decision: The decision that the Digital Wallet's recommend

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/simulate/tokenizations",
            body=maybe_transform(
                {
                    "cvv": cvv,
                    "expiration_date": expiration_date,
                    "pan": pan,
                    "tokenization_source": tokenization_source,
                    "account_score": account_score,
                    "device_score": device_score,
                    "wallet_recommended_decision": wallet_recommended_decision,
                },
                tokenization_simulate_params.TokenizationSimulateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TokenizationSimulateResponse,
        )


class TokenizationsWithRawResponse:
    def __init__(self, tokenizations: Tokenizations) -> None:
        self._tokenizations = tokenizations

        self.simulate = _legacy_response.to_raw_response_wrapper(
            tokenizations.simulate,
        )


class AsyncTokenizationsWithRawResponse:
    def __init__(self, tokenizations: AsyncTokenizations) -> None:
        self._tokenizations = tokenizations

        self.simulate = _legacy_response.async_to_raw_response_wrapper(
            tokenizations.simulate,
        )


class TokenizationsWithStreamingResponse:
    def __init__(self, tokenizations: Tokenizations) -> None:
        self._tokenizations = tokenizations

        self.simulate = to_streamed_response_wrapper(
            tokenizations.simulate,
        )


class AsyncTokenizationsWithStreamingResponse:
    def __init__(self, tokenizations: AsyncTokenizations) -> None:
        self._tokenizations = tokenizations

        self.simulate = async_to_streamed_response_wrapper(
            tokenizations.simulate,
        )
