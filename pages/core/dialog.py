class Dialog:
    def __init__(self, page):
        self.page = page
        self.message = None

    def _accept(self, dialog, text: str | None = None):
        """
        Accept the next dialog that opens, typing `text` first.

        Args:
            (Dialog) dialog: The dialog to accept.
            (str, optional) text: The text to show in the dialog.
        """
        self.message = dialog.message
        dialog.accept(text) if text is not None else dialog.accept()

    def _dismiss(self, dialog):
        """
        Dismiss the next dialog that opens.
        Args:
            (Dialog) dialog: The dialog to dismiss.
        """
        self.message = dialog.message
        dialog.dismiss()

    def accept_next(self, text: str | None = None):
        """
        Accept the next dialog that opens, typing `text` first if it is a prompt.

        Args:
            text (str, optional): The text to show in the dialog.
        """
        self.page.once("dialog", lambda dialog: self._accept(dialog, text))

    def dismiss_next(self):
        """
        Dismiss the next dialog that opens.
        """
        self.page.once("dialog", self._dismiss)