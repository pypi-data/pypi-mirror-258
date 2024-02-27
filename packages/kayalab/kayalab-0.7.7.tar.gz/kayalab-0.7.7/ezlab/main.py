#!/usr/bin/env python3
"""
DESCRIPTION:
    Deploy VMs on my lab and configure them for Ezmeral
USAGE EXAMPLE:
    > ezlab for GUI, ezlabctl for command line
"""

import logging
import os
from nicegui import ui, app, native
import requests

from ezlab.parameters import DF, SUPPORTED_HVES, UA
from ezlab.pages import ezmeral
from ezlab.pages import settings
from ezlab.pages import targets
from ezshow import main as ezshow

# Disable annoying messages in log view
# Thanks to: https://sam.hooke.me/note/2023/10/nicegui-binding-propagation-warning/
import nicegui.binding


# Increase threshold for binding propagation warning from 0.01 to 0.02 seconds
nicegui.binding.MAX_PROPAGATION_TIME = 0.1

logger = logging.getLogger()
# hdlr = logging.FileHandler("ezapp.log")
# formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.WARNING)
requests_log.propagate = True
faker_log = logging.getLogger("faker.factory")
faker_log.setLevel(logging.INFO)
faker_log.propagate = True


class LogElementHandler(logging.Handler):
    """A logging handler that emits messages to a log element."""

    def __init__(self, element: nicegui.ui.log, level: int = logging.NOTSET) -> None:
        self.element = element
        super().__init__(level)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.element.push(msg)
        except Exception:
            self.handleError(record)


# Module Globals
logger = logging.getLogger()


# Initialize
# Top-level keys in config
for key in ["target", "ui", "config", UA, DF, *SUPPORTED_HVES]:
    if key not in app.storage.general.keys():
        app.storage.general[key] = {}

# Set initial connection
app.storage.general["target"]["connected"] = False
# DEBUG for passed args
app.native.start_args["debug"] = True

# Main page
@ui.page("/")
def home():
    # initial status
    app.storage.user["busy"] = False

    # Header
    with ui.header(elevated=True).classes("items-center justify-between") as header:
        # home button
        ui.label("Ezlab").classes("text-bold text-lg")

        ui.space()

        with ui.row().classes("items-center"):
            ui.label("Settings")
            ui.button(icon="download", on_click=settings.config_show().open)
            ui.button(icon="upload", on_click=settings.config_load().open)

    # Footer
    with ui.footer() as footer:
        with ui.row().classes("w-full"):
            ui.label("Log")
            ui.space()
            ui.spinner("ios", size="2em", color="red").bind_visibility_from(
                app.storage.user, "busy"
            )
            ui.icon("check_circle", size="2em", color="green").bind_visibility_from(
                app.storage.user, "busy", lambda x: not x
            )
        log = ui.log().classes("w-full h-48 text-accent")
        logger.addHandler(LogElementHandler(log))

    # Content

    # README section
    with (
        ui.expansion(
            "Readme",
            icon="description",
            caption="how to use this app?",
        )
        .classes("w-full")
        .classes("text-bold")
    ):
        readme = ""
        with open(os.path.dirname(__file__) + "/USAGE.md", "r") as readmefile:
            readme = readmefile.read()

        ui.markdown(readme)

    # Settings section
    settings.menu()

    ui.separator()

    # Infrastructure section
    targets.menu()

    ui.separator()

    # Ezmeral Products section
    ezmeral.menu()

    ui.separator()
    
    # Demo section
    ezshow.menu()

# Entry point for the module
def enter():
    # ui.run(
    #     ezmeral_icon = """
    #     <svg width="48" height="24" viewBox="0 0 48 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    #         <path d="M7 8H41V16H7V8Z" fill="#01A982"/>
    #         <path d="M1 8H7V16H1V8Z" fill="#00775B"/>
    #         <path d="M41 8H47V16H41V8Z" fill="#00775B"/>
    #         <path d="M7 16H41V22H7V16Z" fill="#00775B"/>
    #         <path d="M7 2H41V8H7V2Z" fill="#00C781"/>
    #         <path d="M1 8L7 2V8H1Z" fill="#01A982"/>
    #         <path d="M1 16L7 22V16H1Z" fill="#01A982"/>
    #         <path d="M47 8L41 2V8H47Z" fill="#01A982"/>
    #         <path d="M47 16L41 22V16H47Z" fill="#01A982"/>
    #     </svg>
    #     """
    #     title="Ezlab",
    #     dark=None,
    #     favicon=ezmeral_icon,
    #     storage_secret = ("ezmeralr0cks",)
    #     show=True,
    #     # reload=False,
    # )
    ui.run(
        title="Ezlab",
        dark=None,
        native=True,
        window_size=(1024, 1024),
        # frameless=True,
        storage_secret="ezmeralr0cks",
        reload=False,
        port=native.find_open_port(),
    )

# For development and debugs
if __name__ in {"__main__", "__mp_main__"}:
    # INSECURE REQUESTS ARE OK in DEV
    requests.packages.urllib3.disable_warnings()
    # Adjust logging
    urllib_logger = logging.getLogger("urllib3.connectionpool")
    urllib_logger.setLevel(logging.INFO)
    faker_log = logging.getLogger("faker.factory")
    faker_log.setLevel(logging.INFO)
    # faker_log.propagate = True
    watcher_logger = logging.getLogger("watchfiles.main")
    watcher_logger.setLevel(logging.FATAL)
    print("EZLAB RUNNING IN DEV MODE")
    ui.run(
        title="Ezlab",
        dark=None,
        native=True,
        window_size=(1024, 1024),
        # frameless=True,
        storage_secret="ezmeralr0cks",
        reload=True,
        port=native.find_open_port(),
    )
