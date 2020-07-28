from typing import Dict, List, Optional, Tuple

import yaml


class ProxyList:
    """
    Parser to retrieve list of proxies from the configuration file in format
    matching the proxy.py ProxyPoolPlugin

    Attributes:
        proxy_list: list of proxies

    """

    proxy_list: List[Dict[str, Tuple[str, int]]]

    def __init__(self) -> None:
        self.proxy_list = []

    def _get_proxies_from_file(self) -> None:
        with open("config/proxy_list.yaml", 'r') as stream:
            try:
                proxies = yaml.safe_load(stream).get("proxies", {})
                for i, (key, value) in enumerate(proxies.items()):
                    proxy = self._get_proxy_item(key=key, item=value)
                    if proxy not in self.proxy_list:
                        self.proxy_list.append(proxy)
            except yaml.YAMLError as error:
                raise ValueError("Improperly configured YAML file => %s" % error)

    @staticmethod
    def _validate_proxy_item(item: List[Dict[str, int]]):
        if item[0].get("ip", None) is None:
            return False
        if item[1].get("port", None) is None \
           or not isinstance(item[1].get("port", None), int):
            return False
        return True

    def _get_proxy_item(
            self, key: str, item: List[Dict[str, int]]
    ) -> Optional[Dict[str, Tuple[str, int]]]:
        if self._validate_proxy_item(item=item):
            return {
                key: (item[0]["ip"], item[1]["port"])
            }
        return None

    def get_proxies(self) -> List[Dict[str, Tuple[str, int]]]:
        """Get list of proxies defined in a YAML configuration file"""

        self._get_proxies_from_file()
        return self.proxy_list
