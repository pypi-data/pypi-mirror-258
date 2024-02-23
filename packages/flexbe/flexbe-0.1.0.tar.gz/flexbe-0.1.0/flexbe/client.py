import typing as t
from urllib.parse import urljoin

from requests import Session

from .exceptions import FlexbeError
from .types import Lead


class Flexbe:
    def __init__(self, url: str, token: str, prefix: str = "/mod/api/"):
        self.url = urljoin(url, prefix)
        self.token = token
        self.session = Session()

    def check_connection(self) -> bool:
        if self.request("checkConnection")["status"] == 1:
            return True
        return False

    def request(self, method: str, params: dict[str, t.Any] | None = None):
        if params is None:
            params = {"api_key": self.token, "method": method}
        else:
            params["api_key"] = self.token
            params["method"] = method

        response = self.session.request("POST", self.url, params=params)
        data = response.json()
        if data.get("error"):
            raise FlexbeError(data["error"]["code"], data["error"]["msg"])
        return data

    def get_leads(self, **filters) -> t.Sequence[Lead]:
        return list(self.request("getLeads", filters)["data"]["leads"].values())

    def get_lead(self, id: int) -> Lead | None:
        leads = self.get_leads(id=id)
        if not leads:
            return None
        return leads[0]

    def update_lead(self, id: int, **fields) -> Lead:
        fields["id"] = id
        return self.request("changeLead", fields)
