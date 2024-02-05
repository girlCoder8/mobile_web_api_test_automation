from hybrid.enums.file_paths import FilePaths
from hybrid.utilities.parser.yaml_parser_utils import YamlParser
from hybrid.utilities.ui.element.element_utils import ElementUtils
from hybrid.utilities.ui.locator.locator_utils import LocatorUtils
from hybrid.utilities.ui.scroller.scroll import ScrollUtils
from hybrid.utilities.ui.swipe.swipe_utils import SwipeUtils
from hybrid.utilities.ui.waiter.waits import Waits
from hybrid.utilities.ui.window.window_utils import WindowUtils


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.element = ElementUtils(driver)
        self.scroller = ScrollUtils(driver)
        self.config = YamlParser(FilePaths.COMMON)
        self.wait = Waits(driver)
        self.locator = LocatorUtils(driver)
        self.window = WindowUtils(driver)
        self.swipe = SwipeUtils(driver)
