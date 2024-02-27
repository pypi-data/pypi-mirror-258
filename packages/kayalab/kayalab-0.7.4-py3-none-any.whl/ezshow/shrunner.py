from nicegui import app

# from ezinfra.remote import ssh_run_command

appstore = app.storage.general["demo"]

HOST = appstore["host"]
USERNAME = appstore["username"]
PASSWORD = appstore["password"]
# TODO: change this to reflect the correct location
KEYFILE = app.storage.general["config"]["privatekeyfile"]

def run_command(command):

    # for out in ssh_run_command(HOST, USERNAME, KEYFILE, command):
    #     print(out)

    return f"[ {HOST} ] RUN: {command}"
