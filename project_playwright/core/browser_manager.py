from playwright.sync_api import sync_playwright


class BrowserManager:

    def __init__(self, headless=False):
        self.headless = headless

    def launch(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            record_video_dir="videos/"
        )
        return self.context.new_page()

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()
