"""
Data Fabric operations user interface
"""

import re
import nicegui
import random
import string
import time

from ezlab.ezmeral.ezdf import client_install, cluster_install, xcluster

from ezlab.parameters import DF
from ezinfra.queue import process_queue
from ezinfra.vms import prepare
from ezlab.utils import ezapp

appstore = nicegui.app.storage.general

@nicegui.ui.refreshable
def add_remove_host(hosts: list):
    if hosts is None:
        hosts = []
    for host in hosts:
        with nicegui.ui.row().classes("w-full items-center no-wrap"):
            nicegui.ui.input(
                "Hostname",
                placeholder="Host shortnames, ie, ezvm1,ezvm2...",
            ).bind_value(host, "name")
            nicegui.ui.input(
                "IP Address",
                placeholder="10.1.1.x",
            ).bind_value(host, "ip")


def get_doc(content: dict):

    random_eof = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def indent(strings: str, spaces: int):
        return strings.strip().replace("\n", f"\n{' '*spaces}")

    settings = ""

    for key, value in content["settings"].items():
        settings += f"""
    #   {key}: {value if len(str(value)) < 80 else value[:77] + '...'}"""

    files = ""
    for filepath, filecontent in content["files"].items():
        files += f"""
    sudo cat <<{random_eof}>{filepath}
    {indent(filecontent,4)}
    {random_eof}
    """

    commands = ""
    for command in content["commands"]:
        commands += f"""
    {indent(command,4)}
    """

    doc = f"""
    #!/usr/bin/env bash

    # Ezlab Run {time.strftime('%Y%m%d%H%M%z')}
    
    # {content["task"]}

    # Settings
        {settings}

    # Write Files
        {files}
    
    # Run Commands
        {commands}

    # End of {content['task']}

"""

    with (
        nicegui.ui.dialog().props("full-width") as dialog,
        nicegui.ui.card().classes("w-full"),
    ):
        nicegui.ui.code(doc, language="bash").classes("w-full text-wrap")
        with nicegui.ui.row():
            nicegui.ui.button(
                "Save (useless on app mode)",
                icon="save",
                on_click=lambda: nicegui.ui.download(doc.encode(), "ezlab-runbook.sh"),
            )
            nicegui.ui.button(
                "Close",
                icon="cancel",
                on_click=dialog.close,
            )
    dialog.open()


async def prepare_action(pager: nicegui.ui.stepper):
    hosts = appstore[DF]["hosts"]
    userstore = nicegui.app.storage.user

    # deep check list[dict] for missing values (if any host's name or IP is missing)
    if not (
        len(hosts) > 0
        and all(
            [values for values in [all(host) for host in [h.values() for h in hosts]]]
        )
    ):
        nicegui.ui.notify("Missing values", type="warning")
        return False

    ezapp.queue.put("Starting configuration for DF")
    for host in hosts:
        result = prepare(
            hostname=host["name"],
            hostip=host["ip"],
            config=dict(appstore["config"]),
            addhosts=[h for h in hosts if h["name"] != host["name"]],
            add_to_noproxy=(
                re.split(
                    ":|/", appstore[DF].get("maprlocalrepo").split("://")[1]
                )[0]
                if appstore[DF].get("maprrepoislocal", False)
                else None
            ),
            prepare_for=DF,
            dryrun=appstore["config"]["dryrun"],
        )
        if appstore["config"]["dryrun"]:
            get_doc(await result)
        elif result:
            pass
        else:
            nicegui.ui.notify(f"[{host}] preparation failed!", type="warning")

    userstore["busy"] = True
    result = await nicegui.run.io_bound(process_queue, len(hosts))
    userstore["busy"] = False

    if result:
        nicegui.ui.notify(f"Finished with {len(hosts)} host(s)", type="positive")
        pager.next()
        return True
    else:
        return False


def prepare_menu():
    if not "hosts" in appstore[DF].keys():
        appstore[DF]["hosts"] = [{"name": "", "ip": ""}]
    with nicegui.ui.row().classes("w-full items-center items-stretch") as prep_view:
        nicegui.ui.label("Hosts")
        nicegui.ui.space()
        with nicegui.ui.row():

            def add_host():
                try:
                    appstore[DF]["hosts"].append({"name": "", "ip": ""})
                except (KeyError, AttributeError):
                    appstore[DF]["hosts"] = [{"name": "", "ip": ""}]
                finally:
                    add_remove_host.refresh(appstore[DF]["hosts"])

            def remove_host():
                if len(appstore[DF]["hosts"]) > 0:
                    appstore[DF]["hosts"].pop()
                    add_remove_host.refresh()

            nicegui.ui.button(icon="add_box", color=None, on_click=add_host).props(
                "flat"
            )
            nicegui.ui.button(icon="delete", color=None, on_click=remove_host).props(
                "flat"
            )

    # Hosts
    add_remove_host(appstore[DF]["hosts"])


async def install_action(hosts_string: str, pager: nicegui.ui.stepper):
    userstore = nicegui.app.storage.user

    ezapp.queue.put("Starting DF cluster installation")

    result = cluster_install(
        hosts=hosts_string.split(","),
        settings=dict(appstore["config"]),
        config=dict(appstore[DF]),
        dryrun=appstore["config"]["dryrun"],
    )

    if appstore["config"]["dryrun"]:
        get_doc(await result)

    elif not result:
        nicegui.ui.notify(f"Cluster creation failed!", type="negative")

    userstore["busy"] = True
    result = await nicegui.run.io_bound(process_queue, 1)
    userstore["busy"] = False
    if result:
        nicegui.ui.notify(f"Finished cluster creation", type="positive")
        pager.next()
        return True
    else:
        return False


async def xcluster_action(pager: nicegui.ui.stepper):
    userstore = nicegui.app.storage.user
    
    ezapp.queue.put("Starting DF cross-cluster setup")

    if not xcluster(
        config=dict(appstore["config"]),
        settings=dict(appstore[DF]),
    ):
        nicegui.ui.notify(f"Cluster creation failed!", type="negative")

    userstore["busy"] = True
    res = await nicegui.run.io_bound(process_queue, 1)
    userstore["busy"] = False
    if res:
        nicegui.ui.notify(f"Finished cross-cluster setup", type="positive")
        pager.next()
        return True
    else:
        return False


async def client_action(pager: nicegui.ui.stepper):
    userstore = nicegui.app.storage.user
    
    ezapp.queue.put("Starting DF client configuration")

    result = client_install(
        username=appstore["config"]["username"],
        keyfile=appstore["config"]["privatekeyfile"],
        config=dict(appstore[DF]),
    )

    if not result:
        nicegui.ui.notify("Client configuration failed", type="negative")

    userstore["busy"] = True
    result = await nicegui.run.io_bound(process_queue, 1)
    userstore["busy"] = False
    if result:
        nicegui.ui.notify(f"Finished client configuration", type="positive")
        pager.next()
        return True
    else:
        return False
