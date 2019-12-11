from all_functions import Methods
from variables import Variables


class Font(Methods):
    """Perform increase, decrease font size, change font style operations"""

    def increase_font(self, event=None):
        """Increase font of the editor and line number"""
        if self.font_size <= 40:
            self.font_size += 1
            self.customFont.config(size=self.font_size)
            self.get_current().config(font=self.customFont)
            self.pady += 1
            self.canvas.pack_configure(pady=(self.pady, 0))
            self.canvas.update()

    def decrease_font(self, event=None):
        """Decrease font of the editor and line number"""
        if self.font_size >= 10:
            self.font_size -= 1
            self.customFont.config(size=self.font_size)
            self.get_current().config(font=self.customFont)
            if self.pady > 1:
                self.pady -= 1
                self.canvas.pack_configure(pady=(self.pady, 0))
            self.canvas.update()

    def font_reset(self, event=None):
        """Reset the font size of editor and line number"""
        self.font_size = 15
        self.customFont.configure(size=self.font_size)
        self.get_current().config(font=self.customFont)

    def change_font(self):
        """Change the font of the editor"""
        pass