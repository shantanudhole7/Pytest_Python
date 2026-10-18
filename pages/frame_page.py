import re
from pages.base_page import BasePage
from pages.core.base_element import BaseElement


class FramePage(BasePage):
    _FRAMES = {
        "frame_1": "#iframe-1",
        "frame_2": "#iframe-2",
    }
    def __init__(self, page, frame: str):
        super().__init__(page)
        if frame not in self._FRAMES:
            raise ValueError(f"Unknown frame '{frame}'. Use one of: {', '.join(self._FRAMES)}")

        self.page_frame = self.switch_to_frame(self._FRAMES[frame])
        self.lnk_docs = BaseElement(self.page_frame.get_by_role("link", name=re.compile(r"^(Docs|Documentation)$")))
        self.lbl_page_header = BaseElement(self.page_frame.locator("h1"))

    def click_on_docs(self):
        """
        Click on the docs button.
        """
        self.lnk_docs.click()

    def get_header_text(self) -> str:
        """
        Get the header text of the page.

        Returns:
            str: Header text of the page.
        """
        return self.lbl_page_header.get_text()