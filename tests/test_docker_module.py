#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import pytest
from selenium.webdriver import DesiredCapabilities

from testcontainers.config import SeleniumConfig
from testcontainers.webdriver import StandaloneSeleniumContainer
from testcontainers.webdriver import SeleniumGridContainers


@pytest.fixture
def selenium_container(request):
    config = SeleniumConfig(SeleniumConfig.CHROME, DesiredCapabilities.CHROME)
    container = SeleniumGridContainers(config).start()

    def fin():
        container.stop()

    request.addfinalizer(fin)
    return container


class TestDocker(object):
    def test_selenium_grid(self):
        config = SeleniumConfig(SeleniumConfig.CHROME)
        with SeleniumGridContainers(config) as firefox:
            webdriver = firefox.get_driver()
            webdriver.get("http://google.com")
            webdriver.find_element_by_name("q").send_keys("Hello")

    def test_fixture(self, selenium_container):
        driver = selenium_container.get_driver()
        driver.get("http://google.com")
        driver.find_element_by_name("q").send_keys("Hello")

    def test_standalone_container(self):
        config = SeleniumConfig(SeleniumConfig.CHROME, DesiredCapabilities.CHROME)

        with StandaloneSeleniumContainer(config) as container:
            driver = container.get_driver()
            driver.get("http://google.com")
            driver.find_element_by_name("q").send_keys("Hello")
