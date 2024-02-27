import json
import logging
import pathlib
import requests

from nicegui import app

logger = logging.getLogger("restrunner")

demostore = app.storage.general["demo"]

AUTH_CREDENTIALS = (demostore["username"], demostore["password"])


def get(path: str):
    REST_URL = f"https://{demostore['host']}:8443{path}"
    try:
        response = requests.get(url=REST_URL, auth=AUTH_CREDENTIALS, verify=False)
        # logger.debug("GET RESPONSE: %s", response.text)
        response.raise_for_status()
        return response

    except Exception as error:
        logger.warning("GET ERROR %s", error)
        return None


def post(path: str):
    REST_URL = f"https://{demostore['host']}:8443{path}"
    # logger.debug("POST URL: %s", REST_URL)
    try:
        response = requests.post(url=REST_URL, auth=AUTH_CREDENTIALS, verify=False)
        # logger.debug("POSTRESPONSE: %s", response)
        response.raise_for_status()
        return response

    except Exception as error:
        logger.warning("POST ERROR %s", error)
        return None


def postfile(demos: list, path: str):

    demo = [demo for demo in demos if demo["name"] == demostore["name"]].pop()

    basedir = (
        f"{pathlib.Path().resolve()}/ezshow/demos/{demo['name'].replace(' ', '-')}"
    )
    fileorfolder = f"{basedir}/{path}"
    volume = demo["volume"]

    if fileorfolder[-1] == "/":
        # Create the folder first
        yield post(f"/files{volume}/{path}")
        source_files = [p for p in pathlib.Path(fileorfolder).iterdir() if p.is_file()]
        target_dir = path
    else:
        source_files = [fileorfolder]
        target_dir = ""

    for file in source_files:
        filename = pathlib.Path(file).name
        destination = volume + "/" + target_dir + filename
        # files = {filename: open(file, "rb")}
        REST_URL = f"https://{demostore['host']}:8443/files{destination}"
        try:
            with open(file, "rb") as f:
                response = requests.put(
                    url=REST_URL,
                    auth=AUTH_CREDENTIALS,
                    verify=False,
                    data=f,
                    timeout=300,
                )
                response.raise_for_status()
                yield response

        except Exception as error:
            logger.warning("POSTFILE ERROR %s", error)
            return None


def dagget(path: str):
    REST_URL = f"https://{demostore['host']}:8243{path}"
    # logger.debug("DAG GET %s", REST_URL)
    try:
        response = requests.get(url=REST_URL, auth=AUTH_CREDENTIALS, verify=False)
        # logger.debug("DAG GET RESPONSE: %s", response)
        response.raise_for_status()
        return response

    except Exception as error:
        logger.warning("DAG GET ERROR %s", error)
        return None


def dagput(path: str, data=None):
    REST_URL = f"https://{demostore['host']}:8243{path}"
    # logger.debug("DAG PUT: %s", REST_URL)
    try:
        response = requests.put(url=REST_URL, auth=AUTH_CREDENTIALS, verify=False, data=data)
        # logger.debug("DAG PUT RESPONSE: %s", response)
        response.raise_for_status()
        return response

    except requests.exceptions.HTTPError as httperror:
        if httperror.response.status_code != 409:
            logger.warning("DAG PUT HTTP ERROR %s", httperror.response.text)

    except Exception as error:
        logger.warning("DAG PUT ERROR %s", error)
        return None


def dagpost(path: str, json_obj=None):
    REST_URL = f"https://{demostore['host']}:8243{path}"
    # logger.debug("DAGPOSTDATA: %s", type(json_obj))

    try:
        response = requests.post(
            url=REST_URL,
            auth=AUTH_CREDENTIALS,
            verify=False,
            json=json_obj,
            # headers={"Content-Type: application/json"},
        )
        # logger.debug("DAG POST RESPONSE: %s", response)
        response.raise_for_status()
        return response

    except Exception as error:
        logger.warning("DAG POST ERROR %s", error)
        return None


def kafkaget(path: str):
    REST_URL = f"https://{demostore['host']}:8082{path}"
    # logger.debug("KAFKA GET %s", REST_URL)
    try:
        response = requests.get(
            url=REST_URL,
            auth=AUTH_CREDENTIALS,
            verify=False,
            headers={
                "Content-Type": "application/vnd.kafka.json.v2+json",
                "Accept": "application/vnd.kafka.json.v2+json",
            },
        )
        # logger.debug("KAFKA GET RESPONSE: %s", response.text)
        response.raise_for_status()
        return response

    except Exception as error:
        # print(f"KAFKA GET ERROR {error}")
        logger.warning("KAFKA GET ERROR %s", error)
        return None


def kafkaput(path: str, data=None):
    REST_URL = f"https://{demostore['host']}:8082{path}"
    # logger.debug("KAFKA PUT: %s", REST_URL)
    try:
        response = requests.put(
            url=REST_URL,
            auth=AUTH_CREDENTIALS,
            verify=False,
            data=json.dumps({"records": [{"value": data}]}),
            headers={"Content-Type": "application/vnd.kafka.json.v2+json"},
        )
        # logger.debug("KAFKA PUT RESPONSE: %s", response)
        response.raise_for_status()
        return response

    except Exception as error:
        logger.warning("KAFKA PUT ERROR %s", error)
        return None


def kafkapost(path: str, data=None):
    REST_URL = f"https://{demostore['host']}:8082{path}"
    # logger.debug("KAFKA POST DATA: %s", data)

    try:
        response = requests.post(
            url=REST_URL,
            auth=AUTH_CREDENTIALS,
            verify=False,
            data=json.dumps(data),
            headers={ "Content-Type": "application/vnd.kafka.json.v2+json" },
        )
        # logger.debug("KAFKA POST RESPONSE: %s", response.content)
        response.raise_for_status()
        return response

    except Exception as error:
        # print(error.text)
        logger.warning("KAFKA POST ERROR %s", error)
        return None


def kafkadelete(path: str):
    REST_URL = f"https://{demostore['host']}:8082{path}"

    try:
        response = requests.delete(
            url=REST_URL,
            auth=AUTH_CREDENTIALS,
            verify=False,
            headers={"Content-Type": "application/vnd.kafka.v2+json"},
        )
        # logger.debug("KAFKA DELETE REQUEST: %s", response.request)
        # logger.debug("KAFKA DELETE RESPONSE FOR %s: %s", REST_URL, response.text)
        response.raise_for_status()
        return response

    except requests.exceptions.HTTPError as httperror:
        if httperror.response.status_code != 404:
            logger.warning("KAFKA DELETE HTTP ERROR %s", httperror.response.text)

    except Exception as error:
        # print(f"KAFKA DELETE ERROR {error}")
        logger.warning("KAFKA DELETE ERROR %s", error)
        return None


# Not used - basic auth used instead
# def get_session():
#     REST_URL = f"https://{demostore['target']}:8443/"
#     AUTH_CREDENTIALS = (
#         demostore["username"],
#         demostore["password"],
#     )
#     try:
#         return requests.get(url=REST_URL, auth=AUTH_CREDENTIALS, verify=False)

#     except Exception as error:
#         return error
