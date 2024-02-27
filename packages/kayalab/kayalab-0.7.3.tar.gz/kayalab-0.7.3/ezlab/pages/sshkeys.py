import os
import nicegui
from ezinfra.sshkeys import create_sshkey, save_sshkey

from ezlab.parameters import SSHKEYNAME
from ezlab.utils import is_file

appstore = nicegui.app.storage.general

async def confirm_overwrite(file):
    with nicegui.ui.dialog() as dialog, nicegui.ui.card():
        nicegui.ui.label(f"{file} will be overwritten, are you sure?")
        with nicegui.ui.row():
            nicegui.ui.button("Yes", on_click=lambda: dialog.submit("Yes"))
            nicegui.ui.button("No", on_click=lambda: dialog.submit("No"))
    return await dialog


async def handle_keyimport(key: str):

    if key is not None:

        if is_file(SSHKEYNAME):
            if await confirm_overwrite(SSHKEYNAME) != "Yes":
                nicegui.ui.notify("Cancelled", type="warning")
                return None

        (result, content) = save_sshkey(key)

        if result:

            appstore["config"]["privatekey"] = content
            appstore["config"]["privatekeyfile"] = os.path.abspath(
                SSHKEYNAME
            )

            nicegui.ui.notify(
                f"Key saved as {os.path.abspath(SSHKEYNAME)}", type="positive"
            )
            ssh_keys_ui.refresh()

        else:
            nicegui.ui.notify(content, type="negative")

    else:
        nicegui.ui.notify("Cancelled", type="warning")


@nicegui.ui.refreshable
def ssh_keys_ui():
    if is_file(SSHKEYNAME):
        nicegui.ui.label(f"Existing Key: {os.path.abspath(SSHKEYNAME)}")
    with nicegui.ui.row():
        nicegui.ui.upload(
            label="Import",
            on_upload=lambda e: handle_keyimport(e.content.read().decode("utf-8")),
            on_rejected=lambda x: nicegui.ui.notify("No file selected"),
            max_file_size=1_000_000,
            max_files=1,
            auto_upload=True,
        ).props("accept=*")

        nicegui.ui.button("Create New", on_click=create_sshkey)
