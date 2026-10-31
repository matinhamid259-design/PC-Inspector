import customtkinter as ctk
from core.localization import Localizer
from app.dashboard import DashboardPage
from app.processes import ProcessesPage
from app.performance import PerformancePage
from app.hardware import HardwarePage
from app.storage import StoragePage
from app.startup import StartupPage
from app.installed_apps import InstalledAppsPage
from app.temperature import TemperaturePage
from app.reports import ReportsPage
from app.settings import SettingsPage
from app.about import AboutPage


class PCInspectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PC Inspector")
        self.geometry("1500x900")
        self.minsize(1200, 760)
        self._lang = Localizer.get_language()
        self._theme = Localizer.get_theme()
        self.apply_theme()

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="PC Inspector",
            font=ctk.CTkFont(size=24, weight="bold"),
            pady=18,
        )
        self.logo.pack(fill="x", padx=12)

        self.nav = {}
        self.pages = {
            "dashboard": DashboardPage(self),
            "processes": ProcessesPage(self),
            "performance": PerformancePage(self),
            "hardware": HardwarePage(self),
            "storage": StoragePage(self),
            "startup": StartupPage(self),
            "installed_apps": InstalledAppsPage(self),
            "temperature": TemperaturePage(self),
            "reports": ReportsPage(self),
            "settings": SettingsPage(self),
            "about": AboutPage(self),
        }

        menu_order = [
            ("dashboard", "Dashboard"),
            ("processes", "Processes"),
            ("performance", "Performance"),
            ("hardware", "Hardware"),
            ("storage", "Storage"),
            ("startup", "Startup Apps"),
            ("installed_apps", "Installed Apps"),
            ("temperature", "Temperature"),
            ("reports", "PC Report"),
            ("settings", "Settings"),
            ("about", "About"),
        ]

        for key, label in menu_order:
            button = ctk.CTkButton(
                self.sidebar,
                text=self.translate(label),
                command=lambda k=key: self.show_page(k),
                height=38,
                anchor="w",
                fg_color="transparent",
                hover_color=("#2d2d2d", "#d0d0d0"),
                border_width=0,
            )
            button.pack(fill="x", padx=10, pady=4)
            self.nav[key] = button

        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

        for page in self.pages.values():
            page.pack_forget()

        self.show_page("dashboard")

    def translate(self, text):
        return Localizer.translate(text, self._lang)

    def apply_theme(self):
        ctk.set_appearance_mode(self._theme)
        ctk.set_default_color_theme("dark-blue")

    def show_page(self, key):
        for name, frame in self.pages.items():
            frame.pack_forget()
        self.pages[key].pack(fill="both", expand=True)
        self.pages[key].refresh_data()


if __name__ == "__main__":
    app = PCInspectorApp()
    app.mainloop()
