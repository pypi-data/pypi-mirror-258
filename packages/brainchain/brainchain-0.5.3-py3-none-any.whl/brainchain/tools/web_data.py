import requests
from typing import List, Optional
from pydantic import BaseModel, Field, validator

class WebDataClientException(Exception):
    pass

class QueryOptions(BaseModel):
    history: Optional[bool] = True
    offers: Optional[int] = 100

class ProductQueryPayload(BaseModel):
    items: List[str]
    options: Optional[QueryOptions] = QueryOptions()

class DealParameters(BaseModel):
    domainId: int
    includeCategories: List[int]
    excludeCategories: Optional[List[int]] = []
    page: Optional[int] = 0

class ProductFinderParameters(BaseModel):
    title: Optional[str] = None

class BestSellersQueryParams(BaseModel):
    category: str
    domain: Optional[str] = 'US'
    wait: Optional[bool] = True

class WebDataClient:
    def __init__(self, service_url: str = "https://brainchain--web-data-service.modal.run"):
        self.service_url = service_url

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = self.service_url + endpoint
        response = requests.request(method, url, **kwargs)
        if response.status_code == 200:
            return response.json()
        else:
            raise WebDataClientException(f"Error {response.status_code} for URL {url}: {response.text}")

    def product_finder(self, params: ProductFinderParameters) -> dict:
        return self._request("POST", "/api/v1/amazon/product/finder", params=params.dict(exclude_none=True))

    def query_product(self, json_data: ProductQueryPayload) -> dict:
        return self._request("POST", "/api/v1/amazon/product/query", json=json_data.dict())

    def best_sellers(self, params: BestSellersQueryParams) -> dict:
        return self._request("GET", "/api/v1/amazon/best-sellers", params=params.dict())

    def find_deals(self, json_data: DealParameters) -> dict:
        return self._request("POST", "/api/v1/amazon/deals", json=json_data.dict())

    def seller_query(self, seller_id: str, **kwargs) -> dict:
        kwargs['seller_id'] = seller_id
        return self._request("GET", "/api/v1/amazon/seller/query", params=kwargs)

    def category_search(self, searchterm: str, **kwargs) -> dict:
        kwargs['searchterm'] = searchterm
        return self._request("GET", "/api/v1/amazon/category/search", params=kwargs)

    def google_search_simple(self, q: str) -> dict:
        params = {"q": q}
        return self._request("GET", "/api/v1/google/search/simple", params=params)

    def google_scanner(self, q: str, additional_pages: Optional[int] = 3) -> dict:
        params = {"q": q, "additional_pages": additional_pages}
        return self._request("GET", "/api/v1/google/scanner", params=params)

    def twitter_search(self, q: str, **kwargs) -> dict:
        kwargs['q'] = q
        return self._request("GET", "/api/v1/twitter/search", params=kwargs)

    def reddit_search(self, q: str, **kwargs) -> dict:
        kwargs['q'] = q
        return self._request("GET", "/api/v1/reddit/search", params=kwargs)
