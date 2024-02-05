from appium.webdriver.common.appiumby import AppiumBy
from pytest import mark

from tests.fixtures.conftest import mobile_driver
from hybrid.enums.appium_automation_name import AppiumAutomationName
from hybrid.enums.browser_make import MobileWebBrowserMake
from hybrid.enums.direction import Direction
from hybrid.enums.mobile_app_type import MobileAppType
from hybrid.enums.mobile_device_environment_type import MobileDeviceEnvironmentType
from hybrid.enums.mobile_os import MobileOs
from hybrid.utilities.ui.swipe.swipe_utils import SwipeUtils


@mark.skip(reason="require infrastructure to support to run this test case and is resource intensive")
@mark.unit_test
@mark.parametrize(
    "mobile_driver",
    [
        {
            "arg_mobile_os": MobileOs.ANDROID,
            "arg_mobile_app_type": MobileAppType.WEB,
            "arg_mobile_device_environment_type": MobileDeviceEnvironmentType.PHYSICAL,
            "arg_automation_name": AppiumAutomationName.UIAUTOMATOR2,
            "arg_mobile_web_browser": MobileWebBrowserMake.CHROME,
        }
    ],
    indirect=True,
)
def test_appium_swipe_utils(mobile_driver):
    swipe = SwipeUtils(mobile_driver)
    mobile_driver.close()
    mobile_driver.switch_to.context("NATIVE_APP")
    swipe.long_swipe(Direction.DOWN)
    swipe.swipe_till_text_visibility("Ecomess", Direction.DOWN)
