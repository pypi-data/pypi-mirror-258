import nicegui
from ezlab.parameters import EZNODES, KVM, PVE
from ezinfra.queue import process_queue
from ezinfra.vms import clone
from ezinfra import kvm, pve
from ezlab.utils import ezapp

appstore = nicegui.app.storage.general

def pve_newvm_dialog():
    userstore = nicegui.app.storage.user

    userstore["busy"] = True

    templates = [
        x for x in pve.vms(ezapp.connection) if x["template"] and x["type"] == "qemu"
    ]
    networks = pve.networks(ezapp.connection)
    storage = pve.storage(ezapp.connection)

    userstore["busy"] = False

    if "template" not in userstore.keys():
        userstore["template"] = templates[0]

    def set_template(name):
        userstore["template"] = [
            t for t in templates if t["name"] == name
        ].pop()

    # vm settings dialog
    with nicegui.ui.dialog() as dialog, nicegui.ui.card():
        template_selector = (
            nicegui.ui.select(
                options=[x["name"] for x in templates],
                label="Template",
                on_change=lambda e: set_template(e.value),
            )
            .classes("w-full")
            .props("inline")
            .bind_value(appstore[PVE], "template")
        )
        storage_selector = (
            nicegui.ui.select(
                options=[
                    x["storage"]
                    for x in storage
                    if x["node"] == userstore["template"]["node"]
                ],
                label="Storage",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(appstore[PVE], "storage")
        )
        network_selector = (
            nicegui.ui.select(
                options=[
                    x["sdn"]
                    for x in networks
                    if x["node"] == userstore["template"]["node"]
                ],
                label="Network",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(appstore[PVE], "network")
        )

        bridge_selector = (
            nicegui.ui.select(
                options=[
                    x["iface"]
                    for x in pve.bridges(
                        ezapp.connection, userstore["template"]["name"]
                    )
                ],
                label="Bridge",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(appstore[PVE], "bridge")
        )

        eznode_selector = (
            nicegui.ui.select(
                options=[x["name"] for x in EZNODES],
                label="Node Type",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(appstore[PVE], "eznode")
        )

        host_selector = (
            nicegui.ui.input(label="VM Name", placeholder="ezvm")
            .classes("w-full")
            .props("inline")
            .bind_value(appstore[PVE], "hostname")
        )

        firstip_selector = (
            nicegui.ui.input(
                label="First IP",
                placeholder=appstore["config"]["gateway"],
            )
            .classes("w-full")
            .props("inline")
            .bind_value(appstore[PVE], "firstip")
        )

        nicegui.ui.button(
            "Create",
            on_click=lambda: dialog.submit(
                (
                    next(
                        (i for i in templates if i["name"] == template_selector.value),
                        None,
                    ),
                    next(
                        (i for i in storage if i["storage"] == storage_selector.value),
                        None,
                    ),
                    bridge_selector.value,
                    next(
                        (i for i in EZNODES if i["name"] == eznode_selector.value),
                        None,
                    ),
                    host_selector.value,
                    firstip_selector.value,
                )
            ),
        )

    return dialog


def kvm_newvm_dialog():
    userstore = nicegui.app.storage.user

    @nicegui.ui.refreshable
    def volume_selector():
        userstore["busy"] = True
        vols = kvm.volumes(
            appstore[KVM].get("pool", "default")
        )
        selector = (
            nicegui.ui.select(
                options=vols,
                label="Base Image",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(appstore[KVM], "baseimg")
        )
        userstore["busy"] = False
        return selector

    # select dialog
    with nicegui.ui.dialog() as dialog, nicegui.ui.card():

        userstore["busy"] = True

        pools = kvm.pools()
        bridges = kvm.bridges()

        userstore["busy"] = False

        pool = (
            nicegui.ui.select(
                options=[p.name() for p in pools],
                label="Pool",
                on_change=volume_selector.refresh,
            )
            .classes("w-full")
            .props("inline")
            .bind_value(appstore[KVM], "pool")
        )

        baseimg = volume_selector()

        bridge = (
            nicegui.ui.select(
                options=bridges,
                label="Bridge",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(appstore[KVM], "bridge")
        )

        eznode_selector = (
            nicegui.ui.select(
                options=[x["name"] for x in EZNODES],
                label="Node Type",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(appstore[KVM], "eznode")
        )

        host_selector = (
            nicegui.ui.input(label="VM Name", placeholder="ezvm")
            .classes("w-full")
            .props("inline")
            .bind_value(appstore[KVM], "hostname")
        )

        firstip_selector = (
            nicegui.ui.input(
                label="First IP",
                placeholder="10.1.1.21",
            )
            .classes("w-full")
            .props("inline")
            .bind_value(appstore[KVM], "firstip")
        )

        nicegui.ui.button(
            "Create",
            on_click=lambda: dialog.submit(
                (
                    pool.value,
                    baseimg.value,
                    bridge.value,
                    next(
                        (i for i in EZNODES if i["name"] == eznode_selector.value),
                        None,
                    ),
                    host_selector.value,
                    firstip_selector.value,
                )
            ),
        )
    return dialog


async def new_vm_ui():
    userstore = nicegui.app.storage.user 

    if appstore["target"]["hve"] == PVE:
        dialog = pve_newvm_dialog()
    elif appstore["target"]["hve"] == KVM:
        dialog = kvm_newvm_dialog()
    else:
        nicegui.ui.notify("not implemented")

    resources = await dialog

    if resources and all(resources):
        vmcount = resources[3]["count"]

        ezapp.queue.put(f"Cloning {vmcount} VM(s)...")
        for count in range(vmcount):
            try:
                result = clone(
                    target=appstore["target"]["hve"],
                    resources=resources,
                    settings=dict(appstore["config"]),
                    vm_number=(
                        0 if vmcount == 1 else count + 1
                    ),  # start from 1 not 0, use 0 for single vm
                    dryrun=appstore["config"].get("dryrun", True),
                )
                if result:
                    pass
                else:
                    nicegui.ui.notify(f"Clone failed for {count}!", type="warning")

            except Exception as error:
                nicegui.ui.notify(error, type="negative")

        userstore["busy"] = True
        res = await nicegui.run.io_bound(process_queue, vmcount)
        userstore["busy"] = False
        if res:
            nicegui.ui.notify(f"Finished with {vmcount} clone(s)", type="positive")
        else:
            nicegui.ui.notify("Failed with clones", type="negative")

    else:
        nicegui.ui.notify("VM creation cancelled", type="info")
