import argparse
import logging
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import Optional


# Initialize a logger
logger = logging.getLogger(__name__)


def setup_driver(proxy: str = None) -> webdriver.Chrome:
    """
    This function sets up a Chrome WebDriver using ChromeDriverManager. It allows for
    optional configuration of a proxy server. The WebDriver is configured to run headless by default,
    but this can be adjusted in the Chrome options settings.

    Parameters:
    - proxy (str, optional): The proxy server address to configure with the WebDriver.
      Format should be "host:port". If None, no proxy will be configured. Default is None.

    Returns:
    - webdriver.Chrome: An instance of Chrome WebDriver with or without proxy configuration based on the input.
    """
    logging.debug("Configuring Chrome WebDriver options")
    chrome_options = Options()
    if proxy:
        logging.debug(f"Proxy detected, setting proxy server in Chrome to {proxy}")
        chrome_options.add_argument(f"--proxy-server={proxy}")
    logging.debug("Setting Chrome too run headless")
    chrome_options.add_argument(" --headless=new")
    logging.debug("Creating the new Chrome WebDriver")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def highlight_and_zoom(driver: webdriver.Chrome, element: WebElement):
    """
    This function takes a Chrome WebDriver and executes Javascript code to highlight and zoom in on a specific element
    on an HTML page.

    Parameters:
    - driver (webdriver.Chrome): The Chrome WebDriver.
    - element (WebElement): The Selenium WebElement
    """
    logging.debug("Highlighting search string")
    driver.execute_script(
        "arguments[0].setAttribute('style', arguments[1]);",
        element,
        "background-color: yellow; border: 2px solid red;",
    )
    logging.debug("Zooming in on search string")
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'});",
        element,
    )
    driver.execute_script("document.body.style.zoom='150%'")


def search_and_highlight(
    url: str, search_string: str, proxy: str = None
) -> Optional[str]:
    """
    This function initializes a Chrome WebDriver with optional proxy settings, navigates to the given URL, searches for
    the given search string, and if found, highlights and zooms in on the search string then take a screenshot of it
    using a uuid as the filename.

    Parameters:
    - url (str): The URL to navigate to.
    - search_string (str): The search string to search for in the HTML.
    - proxy (str, optional): The proxy server address to configure with the WebDriver.
      Format should be "host:port". If None, no proxy will be configured. Default is None.

    Returns:
    - (str, optional): If the search string is found, the screenshot of the filename is returned.
    """
    driver = setup_driver(proxy)
    logging.debug(
        f"Navigating to {url} using the Chrome WebDriver that was just created"
    )
    driver.get(url)
    logging.debug(f"Searching the HTML code for the search string {search_string}")
    elements = driver.find_elements(
        By.XPATH, f"//*[contains(text(), '{search_string}')]"
    )
    if elements:
        logging.debug("Search string was found")
        highlight_and_zoom(
            driver, elements[0]
        )  # Highlight and zoom on the first occurrence
        filename = f"{str(uuid.uuid4())}.png"
        logging.debug(f"Saving screenshot to {filename}")
        driver.save_screenshot(filename)

        return filename
    else:
        logging.debug("Search string was not found")
    logging.debug("Shutting down the Chrome WebDriver")
    driver.quit()

    return None


def _cli():
    """
    Command line interface function for Fern.
    """
    parser = argparse.ArgumentParser(
        description="Fern - HTML Highlight and Screenshot Tool by irisdotsh"
    )

    parser.add_argument("url", help="URL")
    parser.add_argument("search_string", help="Search string")
    parser.add_argument(
        "-p", "--proxy", default="", help="Proxy URI, eg. socks5://127.0.0.1:9091"
    )

    args = parser.parse_args()

    filename = search_and_highlight(args.url, args.search_string, args.proxy)

    if filename is not None:
        print(f"Search term found, screenshot saved to {filename}")
    else:
        print("Could not find search term")
