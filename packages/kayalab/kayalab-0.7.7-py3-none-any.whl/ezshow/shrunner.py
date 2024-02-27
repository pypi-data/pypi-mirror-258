from nicegui import app

# from ezinfra.remote import ssh_run_command

appstore = app.storage.general["demo"]

HOST = appstore.get("host", "")
USERNAME = appstore.get("username", "")
PASSWORD = appstore.get("password", "")
# TODO: change this to reflect the correct location
KEYFILE = app.storage.general["config"].get("privatekeyfile", "")

def run_command(command):

    # for out in ssh_run_command(HOST, USERNAME, KEYFILE, command):
    #     print(out)

    return f"[ {HOST} ] RUN: {command}"
