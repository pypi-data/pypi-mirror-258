import asyncio
import nicegui
from proxmoxer import ProxmoxAPI
from libvirt import virConnect
import ezlab.utils as utils

from ezlab.parameters import KVM, PVE, SUPPORTED_HVES

from ezlab.pages.vms import new_vm_ui
from ezinfra import kvm, pve

appstore = nicegui.app.storage.general

@nicegui.ui.refreshable
def menu():
    userstore = nicegui.app.storage.user

    with (
        nicegui.ui.expansion("VMs", icon="computer", caption="create and configure")
        .classes("w-full")
        .classes("text-bold") as virtualmachines
    ):
        with nicegui.ui.row().classes("w-full items-center justify-between"):
            # Login dialog
            with nicegui.ui.dialog() as dialog, nicegui.ui.card():
                t = (
                    nicegui.ui.radio(options=SUPPORTED_HVES)
                    .classes("w-full")
                    .props("inline")
                    .bind_value(appstore["target"], "hve")
                )

                h = (
                    nicegui.ui.input("Host")
                    .classes("w-full")
                    .bind_value(appstore["target"], "host")
                )

                u = (
                    nicegui.ui.input("Username")
                    .classes("w-full")
                    .bind_value(appstore["target"], "username")
                )

                p = (
                    nicegui.ui.input(
                        "Password",
                        password=True,
                        password_toggle_button=True,
                    )
                    .classes("w-full")
                    .bind_value(appstore["target"], "password")
                    .bind_enabled_from( # disable password entry for kvm, only ssh key authorisation works (or user need to enter password at the cli)
                        appstore["target"], "hve", backward=lambda x: x != KVM
                    )
                )

                nicegui.ui.button(
                    "Login",
                    on_click=lambda: dialog.submit((t.value, h.value, u.value, p.value)),
                )

            # Connection view
            with nicegui.ui.row():
                nicegui.ui.button(icon="cloud_done", on_click=lambda: loginbuttonaction(dialog)).bind_visibility_from(
                    appstore["target"],
                    "connected",
                )
                nicegui.ui.button(
                    icon="cloud_off", on_click=lambda: loginbuttonaction(dialog)
                ).bind_visibility_from(
                    appstore["target"],
                    "connected",
                    lambda x: not x,
                )

            # new vm button
            nicegui.ui.label().bind_text_from(
                appstore["target"],
                "hve",
                backward=lambda x: f"{x} connected",
            ).bind_visibility_from(appstore["target"], "connected")
            nicegui.ui.button("New VM", on_click=new_vm_ui).bind_visibility_from(
                appstore["target"], "connected"
            ).bind_enabled_from(userstore, "busy", backward=lambda x: not x)

    virtualmachines.bind_value(appstore["ui"], "virtualmachines")


async def loginbuttonaction(loginform: nicegui.ui.dialog):
    if appstore["target"]["connected"]:
        # TODO: disconnect process/cleanup
        appstore["target"]["connected"] = False
   
    else:
        result = await loginform

        # modify password field if target is KVM, so emptiness check below can proceed without password
        if result[0] == KVM:
            result[3] == "nopasswordsupportforkvm"

        # emptiness check
        if result and all(result):
            connection = await connect(result)
            if connection: 
                utils.ezapp.connection = connection
                appstore["target"]["connected"] = True

        else:
            nicegui.ui.notify("Missing information", type='warning')


async def connect(params: set):
    target, host, username, password = params
    try:
        if target == PVE:
            result = await asyncio.to_thread(pve.connect, host, username, password)

        elif target == KVM:
            result = await asyncio.to_thread(kvm.connect, host, username)

        # elif target == VMWARE:
        #     return await asyncio.to_thread(vmw.connect, host, username, password)

        else:
            result = None

        if isinstance(result, ProxmoxAPI) or isinstance(result, virConnect):
            appstore["target"]["connected"] = True
            return result
        else:
            appstore["target"]["connected"] = False
            nicegui.ui.notify(f"FAILED: {result}", type="negative")

    except Exception as error:
        nicegui.ui.notify(f"CONNECT ERROR: {error}", type="negative")
