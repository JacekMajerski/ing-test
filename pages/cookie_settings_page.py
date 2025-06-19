from playwright.sync_api import Page, Locator

class CookieSettingsPage:
    def __init__(self, page: Page):
        self.page = page
        # Buttony
        self.customize_button: Locator = page.get_by_role("button", name="Dostosuj")
        self.accept_button: Locator = page.get_by_role("button", name="Zaakceptuj zaznaczone")
        # Inne lokatory
        self.analytics_checkbox: Locator = page.get_by_label("Analityczne")

    def open_custom_settings(self):
        self.customize_button.wait_for(timeout=60000)
        self.customize_button.click()

    def accept_analytics_and_confirm(self):
        if not self.analytics_checkbox.is_checked():
            self.analytics_checkbox.check()
        self.accept_button.click()
