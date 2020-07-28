import ipaddress
import json
import random
import socket
from typing import Any, Dict, List, Optional, Tuple

from proxy.common.constants import DEFAULT_TIMEOUT
from proxy.http.parser import HttpParser
from proxy.plugin.proxy_pool import ProxyPoolPlugin

from utils import ProxyList


class ProxyPool(ProxyPoolPlugin):
    """Proxy incoming requests separating each tab from the browser by tab.id"""

    UPSTREAM_PROXY_POOL: List[Dict[str, Tuple[str, int]]] = []
    conn: Optional[socket.socket]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        proxy_list = ProxyList()
        self.UPSTREAM_PROXY_POOL = proxy_list.get_proxies()

    @staticmethod
    def _load_used_proxies() -> List[str]:
        with open("proxies_used.json", "r") as file:
            data = json.load(file)
            return data
    
    @staticmethod
    def _get_proxy_name(proxy: Dict[str, Tuple[str, int]]) -> str:
        return [*proxy.keys()][0]
    
    @staticmethod
    def _get_proxy(proxy: Dict[str, Tuple[str, int]]) -> Tuple[str, int]:
        return [*proxy.values()][0]
    
    @classmethod
    def _update_used_proxies(cls, proxy: Dict[str, Tuple[str, int]]) -> None:
        used_proxies = cls._load_used_proxies()
        used_proxies.append(cls._get_proxy_name(proxy=proxy))

        with open("proxies_used.json", "w+") as file:
            json.dump(used_proxies, file)

    @classmethod
    def _can_use_proxy(cls, proxy: Dict[str, Tuple[str, int]]) -> bool:
        proxy_name = cls._get_proxy_name(proxy=proxy)
        if proxy_name not in cls._load_used_proxies():
            return True
        return False
    
    @classmethod
    def _new_socket_connection(
        cls, proxy: Dict[str, Tuple[str, int]], timeout: int = DEFAULT_TIMEOUT
    ) -> socket.socket:
        connection = None
        proxy_address = cls._get_proxy(proxy=proxy)

        try:
            ip_address = ipaddress.ip_address(proxy_address[0])
            if ip_address.version == 4:
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.settimeout(timeout)
                connection.connect(proxy_address)
        except ValueError:
            pass  # Not a valid IPv4 address

        if connection is not None:
            return connection

    def before_upstream_connection(self, request: HttpParser) -> Optional[HttpParser]:
        """
        Establish connection to random proxy from `proxy_list`

        Before establishing connection:
            ensure proxy is not in use

        After establishing connection:
            update list of proxies in use

        """

        while self.conn is None:
            proxy = random.choice(self.UPSTREAM_PROXY_POOL)
            if self._can_use_proxy(proxy=proxy):
                self.conn = self._new_socket_connection(proxy=proxy)
                if self.conn is not None:
                    self._update_used_proxies(proxy=proxy)

        return None
