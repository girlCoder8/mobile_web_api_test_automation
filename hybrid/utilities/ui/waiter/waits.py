from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from hybrid.decorators.loggers.logger import log
from hybrid.enums.file_paths import FilePaths
from hybrid.utilities.parser.yaml_parser_utils import YamlParser


class Waits:
    """WebDriverWait wrapper utility"""

    __config = YamlParser(FilePaths.COMMON)

    def __init__(self, driver):
        """Constructor

        Args:
            driver (webdriver): webdriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Waits.__config.get_value("waits", "max_time_out"))

    @log
    def wait_for_element_to_be_clickable(self, by_locator):
        """Wait for an element till it becomes clickable

        Args:
            by_locator: by locator
        """
        return self.wait.until(EC.element_to_be_clickable(by_locator))

    @log
    def wait_for_title(self, title: str):
        """Wait for title to load in active page in focus

        Args:
            title (str): title of current active page
        """
        self.wait.until(EC.title_is(title))

    @log
    def wait_for_element_presence(self, by_locator):
        """Wait for an element presence in the dom

        Args:
            by_locator: by locator
        """
        return self.wait.until(EC.presence_of_element_located(by_locator))

    @log
    def wait_for_element_visibility(self, by_locator):
        """Wait for an element visibility in UI

        Args:
            by_locator: by locator
        """
        return self.wait.until(EC.visibility_of_element_located(by_locator))

    @log
    def __page_load_js_script(self):
        """page load js script to detect page load completion

        Returns:
            bool: True/False
        """
        return self.driver.execute_script('return document.readyState === "complete"')

    @log
    def wait_for_until(self, func):
        """Waits for custom condition

        Args:
            func (lambda): lamda func
        """
        self.wait.until(func)

    @log
    def wait_for_page_load(self):
        """Wait for page load using javascript"""
        self.wait_for_until(lambda x: self.__page_load_js_script)  # type: ignore
