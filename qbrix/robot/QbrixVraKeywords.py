from time import sleep

from Browser import ElementState, SelectAttribute
from robot.api.deco import library

from qbrix.core.qbrix_robot_base import QbrixRobotTask


@library(scope='GLOBAL', auto_keywords=True, doc_format='reST')
class QbrixVraKeywords(QbrixRobotTask):
    """Shared VRA Keywords"""

    def create_vra_service_channel(self):
        """ Creates the VRA Service Channel """
        self.shared.go_to_setup_admin_page("ServiceChannelSettings/home")
        self.builtin.log_to_console("\n -> Loaded VRA Service Channel Page")
        iframe_selector = self.shared.iframe_handler()
        self.browser.wait_for_elements_state(f"{iframe_selector} .btn:has-text('New')", ElementState.visible, '15s')
        self.builtin.log_to_console("\n -> Checking settings...")
        if "visible" not in self.browser.get_element_states("iframe >>> .listRelatedObject:has-text('SDO_VRA_End_User_Session_Request')"):
            self.builtin.log_to_console("\n -> Not configured... applying settings now...")
            self.browser.click(f"{iframe_selector} .btn:has-text('New')")
            self.browser.fill_text(f"{iframe_selector} tr:has-text('Service Channel Name') >> input", "VRA - End User Session Request")
            self.browser.fill_text(f"{iframe_selector} tr:has-text('Developer Name') >> input", "")
            sleep(1)
            self.browser.fill_text(f"{iframe_selector} tr:has-text('Developer Name') >> input", "SDO_VRA_End_User_Session_Request")
            sleep(1)
            self.browser.select_options_by(f"{iframe_selector} tr:has-text('Salesforce Object') >> select", SelectAttribute.value, "tspa__Visual_Support_Request__c")
            sleep(2)
            self.browser.click(f"{iframe_selector} :nth-match(.saveBtn:has-text('Save'),1)")
            sleep(1)
        self.builtin.log_to_console("\n -> Configuration Complete!")
