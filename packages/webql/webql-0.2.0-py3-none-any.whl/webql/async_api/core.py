"""
This module is an entrypoint to WebQL service
"""

import logging

from webql.async_api.web import InteractiveItemTypeT, PlaywrightWebDriver, WebDriver

from .session import Session

log = logging.getLogger(__name__)


async def start_async_session(
    url: str,
    *,
    web_driver: WebDriver[InteractiveItemTypeT] = PlaywrightWebDriver(),
) -> Session[InteractiveItemTypeT]:
    """Start a new asynchronous WebQL session.

    Parameters:

    url (str): The URL to start the session with.
    web_driver (optional): The web driver to use. Defaults to Playwright web driver.

    Returns:

    Session: The new session.
    """
    log.debug(f"Starting asynchronous session with {url}")

    await web_driver.start_browser()
    await web_driver.open_url(url)
    session = Session[InteractiveItemTypeT](web_driver)
    return session
