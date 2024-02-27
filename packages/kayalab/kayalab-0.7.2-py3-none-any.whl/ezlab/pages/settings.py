# Config show dialog
import json
import nicegui
from ezlab.parameters import DF
from ezlab.pages import ezmeral

from ezlab.pages.sshkeys import ssh_keys_ui
from ezlab.pages import targets
from ezlab.pages import settings

appstore = nicegui.app.storage.general

def save_config(val: str, dialog):
    try:
        for key, value in json.loads(val.replace("\n", "")).items():
            appstore[key] = value
        for m in (ezmeral.menu, targets.menu, settings.menu):
            m.refresh()
        dialog.close()
        nicegui.ui.notify("Settings loaded", type="positive")
    except (TypeError, json.decoder.JSONDecodeError, ValueError) as error:
        nicegui.ui.notify("Not a valid json", type="negative")
        print(error)


def config_show():
    with nicegui.ui.dialog() as config_show, nicegui.ui.card().classes("w-full h-full"):
        config_json = json.dumps(appstore, indent=2)
        nicegui.ui.code(config_json, language="json").classes("w-full text-wrap")
        with nicegui.ui.row():
            nicegui.ui.button(
                "Save (useless on app mode)",
                icon="save",
                on_click=lambda: nicegui.ui.download(
                    config_json.encode(), "ezlab-settings.json"
                ),
            )
            nicegui.ui.button(
                "Close",
                icon="cancel",
                on_click=config_show.close,
            )
    return config_show


# Config load dialog
def config_load():
    with nicegui.ui.dialog() as config_load, nicegui.ui.card().classes("w-full h-full"):
        jsontext = (
            nicegui.ui.textarea()
            .props("stack-label=json autogrow filled")
            .classes("h-dvh w-full text-wrap")
        )
        with nicegui.ui.row():
            nicegui.ui.button(
                "Save",
                on_click=lambda _: save_config(
                    jsontext.value,
                    config_load,
                ),
                icon="save",
            )
            nicegui.ui.button(
                "Close",
                icon="cancel",
                on_click=config_load.close,
            )

    return config_load

@nicegui.ui.refreshable
def menu():
    with (
        nicegui.ui.expansion(
            "Settings",
            icon="settings",
            caption="for your environment",
        )
        .classes("w-full")
        .classes("text-bold") as settings
    ):
        nicegui.ui.checkbox("Dry Run", value=False).bind_value(
            appstore["config"], "dryrun"
        )
        nicegui.ui.label("Network Settings").classes("text-bold")
        with nicegui.ui.row():
            nicegui.ui.input("VM Network", placeholder="10.1.1.0/24").bind_value(
                appstore["config"], "cidr"
            )
            nicegui.ui.input("Gateway", placeholder="10.1.1.1").bind_value(
                appstore["config"], "gateway"
            )
            nicegui.ui.input("Name Server", placeholder="10.1.1.1").bind_value(
                appstore["config"], "nameserver"
            )
            nicegui.ui.input("Domain", placeholder="ez.lab").bind_value(
                appstore["config"], "domain"
            )
            nicegui.ui.input("HTTP Proxy", placeholder="").bind_value(
                appstore["config"], "proxy"
            )

        nicegui.ui.label("Repositories").classes("text-bold")
        with nicegui.ui.row().classes("w-full"):
            # YUM Repo
            nicegui.ui.input("YUM Repo", placeholder="").bind_value(
                appstore["config"], "yumrepo"
            )

            nicegui.ui.input("EPEL Repo", placeholder="").bind_value(
                appstore["config"], "epelrepo"
            )

        # MapR Repository Configuration
        with nicegui.ui.row().classes("w-full"):
            nicegui.ui.label("MapR Repo").classes("self-center")
            switch = (
                nicegui.ui.switch("Use local", value=False)
                .props("left-label")
                .bind_value(appstore[DF], "maprrepoislocal")
            )

            # Using default HPE repository
            with (
                nicegui.ui.row()
                .bind_visibility_from(switch, "value", lambda x: not x)
                .classes("w-full items-justify")
            ):
                nicegui.ui.input("HPE Passport e-mail").bind_value(
                    appstore[DF], "maprrepouser"
                )
                nicegui.ui.input(
                    "HPE Passport token", password=True, password_toggle_button=True
                ).bind_value(appstore[DF], "maprrepotoken")

            # Using local repository
            with nicegui.ui.row().bind_visibility_from(switch, "value"):
                nicegui.ui.input(
                    "MapR Repo",
                    placeholder="https://repo.ez.lab/mapr/",
                ).bind_value(appstore[DF], "maprlocalrepo")
                authlocal = nicegui.ui.switch("Authenticate", value=True).bind_value(
                    appstore[DF], "maprlocalrepoauth"
                )
                with nicegui.ui.row():
                    nicegui.ui.input("Username", password=True).bind_value(
                        appstore[DF], "maprlocalrepousername"
                    ).bind_visibility(authlocal, "value")
                    nicegui.ui.input("Password", password=True).bind_value(
                        appstore[DF], "maprlocalrepopassword"
                    ).bind_visibility(authlocal, "value")

        nicegui.ui.label("Cloudinit Settings").classes("text-bold")
        with nicegui.ui.row():
            nicegui.ui.input("username", placeholder="ezmeral").bind_value(
                appstore["config"], "username"
            )
            nicegui.ui.input("password", password=True, password_toggle_button=True).bind_value(
                appstore["config"], "password"
            )

        nicegui.ui.label("SSH Key").classes("text-bold")
        ssh_keys_ui()

    settings.bind_value(appstore["ui"], "settings")
