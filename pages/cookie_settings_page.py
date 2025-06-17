from playwright.sync_api import Page

class CookieSettingsPage:
    def __init__(self, page: Page):
        self.page = page

    def accept_analytics_and_confirm(self):
        analytics_checkbox = self.page.get_by_label("Analityczne")
        if not analytics_checkbox.is_checked():
            analytics_checkbox.check()
        self.page.get_by_role("button", name="Zaakceptuj zaznaczone").click()

    def open_custom_settings(self):
        customize_button = self.page.get_by_role("button", name="Dostosuj")
        customize_button.wait_for(timeout=60000)
        customize_button.click()