from playwright.sync_api import Page, Frame


class BasePage:
    """
    Actions common to every page. Each page passes a locator that exists only on that page.
    """

    def __init__(self, page: Page):
        """
        Initialize the BasePage.

        Args:
            page: Playwright Page.
        """
        self.page = page

    # -------------------------
    # Page level
    # -------------------------

    def navigate(self, url: str):
        """Navigate to the specified url.

        Args:
            url (str): The url to navigate to.
        """
        self.page.goto(url)

    def get_url(self) -> str:
        """Get the url of the current page.

        Returns:
            str: The url of the current page.
        """
        return self.page.url

    def reload(self):
        """
        Reload the current page.
        """
        self.page.reload()

    def go_back(self):
        """
        Go to the previous page.
        """
        self.page.go_back()

    def go_forward(self):
        """
        Go to the next page.
        """
        self.page.go_forward()

    def switch_to_frame(self, frame: Frame) -> Page:
        """
        Switch to the specified frame.

        Args:
            frame (Frame): The frame to switch to.

        Returns:
            _page_frame (Page): The switched page.
        """
        _page_frame = self.page.frame_locator(frame)
        return _page_frame

