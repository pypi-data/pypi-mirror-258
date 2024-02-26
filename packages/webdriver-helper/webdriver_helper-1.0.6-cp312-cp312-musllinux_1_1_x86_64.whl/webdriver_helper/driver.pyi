from _typeshed import Incomplete
from selenium import webdriver
from selenium.webdriver.common.options import ArgOptions
from typing import Optional

__all__ = ['get_webdriver', 'DriverType']

DriverType: Incomplete

def get_webdriver(driver_type: DriverType = 'chrome', *, hub: str = '', version: Incomplete | None = None, options: Optional[ArgOptions] = None, service_args: Optional[dict] = None, capabilities: Optional[dict] = None) -> webdriver.Remote: ...
debugger = print
upload_by_drop = print
