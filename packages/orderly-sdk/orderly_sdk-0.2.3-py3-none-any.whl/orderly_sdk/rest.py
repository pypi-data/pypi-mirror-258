"""
Orderly Async REST API Client
"""
import base64
import datetime
import json as jsonlib
from collections import defaultdict
from typing import Dict, Optional
from urllib.parse import urlparse

import aiohttp
import base58
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .exceptions import OrderlyRequestException
from .helpers import get_loop
from .log import logger


class AsyncClient:
    """
    Async REST API Client
    """

    _id: str
    account_id: Optional[str]
    orderly_key: Optional[str]
    orderly_secret: Optional[str]
    endpoint: Optional[str]
    api_version: str = "v1"
    timeout = 30

    def __init__(
        self,
        _id="rest_client",
        account_id: Optional[str] = None,
        orderly_key: Optional[str] = None,
        orderly_secret: Optional[str] = None,
        endpoint: Optional[str] = None,
        loop=None,
    ):
        self._id = _id
        self.account_id = account_id
        self.orderly_key = orderly_key
        self.orderly_secret = orderly_secret
        if orderly_secret is not None:
            self.orderly_private_key = Ed25519PrivateKey.from_private_bytes(
                base58.b58decode(orderly_secret)[0:32]
            )
        self.endpoint = endpoint
        self.loop = loop or get_loop()
        self.session = self._init_session()
        self.headers: Dict[str, str] = defaultdict(str)
        self.response = None

    def _get_headers(self) -> Dict:
        headers = {
            "Accept": "application/json",
        }
        if self.orderly_key:
            headers["orderly-key"] = self.orderly_key
        return headers

    def _init_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(loop=self.loop, headers=self._get_headers())

    async def close_connection(self):
        """
        Close the connection
        """
        if self.session:
            assert self.session
            await self.session.close()

    async def _request(
        self,
        method,
        uri: str,
        signed: bool,
        params: Optional[Dict],
        json: Optional[Dict],
    ):
        if signed:
            ts = round(datetime.datetime.now().timestamp() * 1000)
            json_str = ""
            if json is not None:
                logger.debug(f"request json body: {json}")
                json_str = jsonlib.dumps(json)
            path = urlparse(uri).path
            # logger.info(f"request path: {path.path}")
            signature_str = f"{ts}{method.upper()}{path}{json_str}"
            logger.debug(f"request signature: {signature_str}")
            data_bytes = bytes(signature_str, "utf-8")

            req_signature = base64.b64encode(
                self.orderly_private_key.sign(data_bytes)
            ).decode("utf-8")

            self.headers["orderly-signature"] = req_signature
            if self.account_id is not None:
                self.headers["orderly-account-id"] = self.account_id
            else:
                pass
            self.headers["orderly-key"] = f"ed25519:{self.orderly_key}"
            self.headers["orderly-timestamp"] = str(ts)
            self.headers["Content-Type"] = (
                "application/json" if json else "application/x-www-form-urlencoded"
            )
            self.headers["Cache-Control"] = "no-cache"
            self.session.headers.update(self.headers)

        logger.debug("request uri: {}", uri)
        async with getattr(self.session, method)(
            uri, params=params, json=json
        ) as response:
            self.response = response
            return await self._handle_response(response)

    async def _handle_response(self, response: aiohttp.ClientResponse):
        if not str(response.status).startswith("2"):
            logger.error("response: {}", response)
        try:
            return await response.json()
        except ValueError as exc:
            txt = await response.text()
            raise OrderlyRequestException(f"Invalid Response: {txt}") from exc

    def _create_rest_uri(self, ep: str, v: str = ""):
        if not v:
            v = self.api_version
        return f"{self.endpoint}/{v}/{ep}"

    async def _request_api(
        self, method, ep: str, signed: bool, v: str = "", params=None, json=None
    ):
        uri = self._create_rest_uri(ep, v)
        return await self._request(method, uri, signed, params=params, json=json)

    async def _get(self, ep, signed=False, v: str = "", params=None, json=None):
        return await self._request_api("get", ep, signed, v, params, json)

    async def _post(self, ep, signed=False, v: str = "", params=None, json=None):
        return await self._request_api("post", ep, signed, v, params, json)

    async def _put(self, ep, signed=False, v: str = "", params=None, json=None):
        return await self._request_api("put", ep, signed, v, params, json)

    async def _delete(self, ep, signed=False, v: str = "", params=None, json=None):
        return await self._request_api("delete", ep, signed, v, params, json)

    async def get_maintenance_info(self) -> Dict:
        """
        Get maintenance info
        https://docs-api-evm.orderly.network/#restful-api-public-system-maintenance-status
        """
        return await self._get("public/system_info")

    async def get_user_statistics(self) -> Dict:
        """
        Get user statistics
        https://docs-api-evm.orderly.network/#restful-api-private-get-user-volume-statistics
        """
        return await self._get("client/statistics", True)

    async def create_order(self, json: Dict) -> Dict:
        """
        Create an order
        https://docs-api-evm.orderly.network/#restful-api-private-create-order
        """
        return await self._post("order", True, json=json)

    async def claim_liquidated_positions(self, json: Dict) -> Dict:
        """
        Claim liquidated positions
        https://docs-api-evm.orderly.network/#restful-api-private-get-account-information
        """
        return await self._post("liquidation", True, json=json)

    async def claim_insurance_fund(self, json: Dict) -> Dict:
        """
        Claim insurance fund
        https://docs-api-evm.orderly.network/#restful-api-private-get-user-statistics
        """
        return await self._post("claim_insurance_fund", True, json=json)

    async def get_all_positions(self) -> Dict:
        """
        Get all positions
        https://docs-api-evm.orderly.network/#restful-api-private-get-funding-fee-history
        """
        return await self._get("positions", True)

    async def get_liquidation(self, params) -> Dict:
        """
        Get liquidation
        https://docs-api-evm.orderly.network/#restful-api-public-get-liquidated-positions-info
        """
        return await self._get("public/liquidation", params=params)

    async def get_liquidated_positions(self, params) -> Dict:
        """
        Get liquidated positions
        https://docs-api-evm.orderly.network/#restful-api-public-get-liquidated-positions-info
        """
        return await self._get("public/liquidated_positions", params=params)

    async def get_insurance_fund(self) -> Dict:
        """
        Get insurance fund
        https://docs-api-evm.orderly.network/#restful-api-public-get-insurance-fund-info
        """
        return await self._get("public/insurancefund")

    async def get_available_symbols(self) -> Dict:
        """
        Get available symbols
        https://docs-api-evm.orderly.network/#restful-api-public-available-symbols
        """
        return await self._get("public/info")

    async def get_futures_for_one_market(self, symbol) -> Dict:
        """
        Get futures for one market
        https://docs-api-evm.orderly.network/#restful-api-public-get-futures-info-for-all-markets
        """
        return await self._get("public/futures/" + symbol)

    async def get_current_holding(self) -> Dict:
        """
        Get current holding
        https://docs-api-evm.orderly.network/#restful-api-private-get-current-holding
        """
        return await self._get("client/holding", True)

    async def get_account_info(self) -> Dict:
        """
        Get account info
        https://docs-api-evm.orderly.network/#restful-api-private-get-account-information
        """
        return await self._get("client/info", True)
