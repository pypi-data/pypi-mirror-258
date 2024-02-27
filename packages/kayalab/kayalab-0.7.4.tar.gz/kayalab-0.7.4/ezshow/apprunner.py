from datetime import datetime, timedelta
import logging
from random import random
from time import sleep
from urllib.parse import quote, urlparse
from faker import Faker
from nicegui import app
import json

from ezlab.parameters import TASK_FINISHED
from ezlab.utils import getdemo

from ezshow import restrunner

logger = logging.getLogger("apprunner")


def send_transactions(params: list, count: int):
    # there should be single parameter (topic) for this function
    topic = params[0]

    fake = Faker("en_US")
    transactions = []
    for i in range(count):
        transactions.append(
            {
                "id": i + 1,
                "sender_account": fake.iban(),
                "receiver_account": fake.iban(),
                "amount": round(fake.pyint(0, 10_000), 2),
                "currency": "GBP", #fake.currency_code(),
                "transaction_date": fake.past_datetime(start_date="-12M").timestamp(),
            }
        )

    # logger.debug("Creating monitoring table")
    demo = getdemo(app.storage.general["demo"]["name"])
    table_path = f"{demo['volume']}/{demo['table']}"
    stream_path = f"{demo['volume']}/{demo['stream']}"
    create_monitoring_table(table_path=table_path)

    logger.info("Sending %s messages to %s", len(transactions), topic)
    import timeit
    tic = timeit.default_timer()

    stream_publish(
        stream=stream_path,
        topic=topic,
        messages=transactions,
    )
    toc = timeit.default_timer()
    logger.info("It took %i seconds", toc - tic)


def process_transactions(params: list):
    topic = params[0]
    demo = getdemo(app.storage.general["demo"]["name"])
    stream_path = f"{demo['volume']}/{demo['stream']}"
    
    count = 0
    
    import timeit
    tic = timeit.default_timer()
    for message in stream_consume(
        stream=stream_path,
        topic=topic,
    ):

        if message == TASK_FINISHED:
            break

        # logger.debug(f"CONSUMING TRANSACTION: {message}")
        # yield message
        print(f"Simulating txn processing for {message['id']}")
        sleep(0.1)
        count += 1

    toc = timeit.default_timer()
    logger.info(f"Processed %s transactions in %i seconds", count, toc - tic)


def generate_calls(params: list, count: int):
    print(f"To be implemented for {params} to generate {count} messages")


def push_to_monitorDB(stats_json_str: str):
    stats_json = json.loads(stats_json_str)
    stats_json["_id"] = str(stats_json['ts'])
    # logger.debug(f"_ID: {stats_json['_id']}")

    ts = stats_json["ts"] / 1_000_000
    logger.debug(
        "Submit metrics at %s",
        datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"),
    )

    response = restrunner.dagpost(
        "/api/v2/table/%2Fapps%2Fezshowmonitor", json_obj=stats_json
    )

    # logger.debug("MONITOR PUSH RESPONSE: %s", response)

    if isinstance(response, Exception):
        logger.warning("MONITOR PUSH FAILED: %s", response)
        return


def create_monitoring_table(table_path):
    # create monitoring table if not exist
    path = quote(table_path, safe="")
    response = restrunner.dagput(f"/api/v2/table/{path}")
    if isinstance(response, Exception):
        if response.response.status_code != 409:
            logger.warning(f"MonitorDB creation FAILED: {response}")


def kafka_publish(host: str, username: str, password: str, topic: str, messages: list):
    from confluent_kafka import Producer

    # logger.info("Sending %d messages to %s topic", len(messages), topic)
    logger.info(f"Sending {len(messages)} messages to {topic} topic")

    conf = {
        "bootstrap.servers": f"{host}:9092",
        "security.protocol": "SASL_PLAINTEXT",
        "sasl.mechanism": "PLAIN",
        # "enable.ssl.certificate.verification": "false", # if needed with SASL_SSL
        "sasl.username": username,
        "sasl.password": password,
        "client.id": "ezshow",
        "queue.buffering.max.ms": 100,
        "statistics.interval.ms": 1000,
        "stats_cb": push_to_monitorDB,
        "socket.timeout.ms": 1000,
        "message.send.max.retries": 2,
        "default.topic.config": {"message.timeout.ms": 1000, "request.timeout.ms": 1000},
    }

    producer = Producer(**conf)

    # process messages that are already in the queue
    producer.flush()

    # update progress on each poll
    def delivery_report(err, msg):
        if err is None:
            app.storage.general["demo"]["counting"] += 1
            # logger.debug(f"KAFKA DELIVERY: {msg.value().decode()}")
        else:
            logger.debug(f"{err}")

    for msg in messages:
        # process the queue
        producer.poll(0)

        # send the message
        producer.produce(
            topic, key="id", value=json.dumps(msg).encode(), on_delivery=delivery_report
        )

        # logger.debug(f"KAFKA PRODUCED {msg}")

    # process the remaining messages in the queue
    producer.flush()


def kafka_consume(host: str, username: str, password: str, topic: str):
    from confluent_kafka import Consumer, KafkaError, KafkaException

    # logger.info(f"Getting messages from {topic}")
    logger.info(f"Getting messages from %s", topic)

    conf = {
        "bootstrap.servers": f"{host}:9092",
        "group.id": "ezshow",
        "auto.offset.reset": "earliest",
        "security.protocol": "SASL_PLAINTEXT",
        "sasl.mechanism": "PLAIN",
        # "enable.ssl.certificate.verification": "false", # if needed with SASL_SSL
        "sasl.username": username,
        "sasl.password": password,
        "statistics.interval.ms": 500,
        "stats_cb": push_to_monitorDB,  # collect statistics
    }

    c = Consumer(conf)

    # Subscribe to topics
    c.subscribe([topic])

    # return the messages, log the errors
    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:  # we break when there are no more messages in the topic,
                # in real life, you would keep waiting even when there are no messages
                logger.debug(f"Nothing left in the topic {topic} for consumption")
                # continue
                break
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logging.info(
                        "%% %s [%d] reached end at offset %d\n"
                        % (msg.topic(), msg.partition(), msg.offset())
                    )
                elif msg.error():
                    raise KafkaException(msg.error())
                logger.warning(msg.error())
                yield False  # provide feedback on failed message processing
            else:
                logger.debug("Consumer sending message %s", msg.value().decode())
                yield msg.value().decode()

    except Exception as error:
        logger.warning("KAFKA CONSUME ERROR %s", error)

    finally:
        c.close()
        yield TASK_FINISHED


def stream_publish(stream: str, topic: str, messages: list):
    topic_path = quote(f"{stream}:{topic}", safe="")
    for msg in messages:
        response = restrunner.kafkapost(path=f"/topics/{topic_path}", data={"records": [{"value": msg}]})
        if isinstance(response, Exception):
            logger.info(f"Message failed to push: {response}")
        else:
            # logger.debug(f"STREAM PUSH {msg}")
            app.storage.general["demo"]["counting"] += 1
    
    logger.info("%s messages are sent to %s:%s", len(messages), stream, topic)


def stream_consume(stream: str, topic: str):
    topic_path = f"{stream}:{topic}"

    try:
        # Create consumer instance
        response = restrunner.kafkapost(
            f"/consumers/{topic}_consumer_group",
            data={
                "name": f"{topic}_consumer_instance",
                "format": "json",
                "auto.offset.reset": "earliest",
            },
        )

        if not response:
            yield TASK_FINISHED
            return

        # logger.debug("CONSUMER INSTANCE CREATED: %s", response.text)

        # Expected output from preceding command
        # {
        # "instance_id":"my_consumer_instance",
        # "base_uri":"http://localhost:8082/consumers/my_json_consumer_group/instances/my_consumer_instance"
        # }
        consumer_instance = response.json()
        consumer_instance_path = urlparse(consumer_instance['base_uri']).path
        # logger.debug("CONSUMER INSTANCE PATH: %s", consumer_instance_path)

        # subscribe to consumer
        restrunner.kafkapost(f"{consumer_instance_path}/subscription", data={ "topics": [ topic_path ] })
        # No content in response

        # get records
        records = restrunner.kafkaget(f"{consumer_instance_path}/records")
        if records.ok:
            for message in records.json():
                # logger.debug("CONSUMER GOT MESSAGE: %s", message)
                yield message["value"]

        # Expected output from preceding command
        # [
        # {"key":null,"value":{"foo":"bar"},"partition":0,"offset":0,"topic":"jsontest"}
        # ]
    except Exception as error:
        logger.warning("STREAM CONSUMER ERROR %s", error)

    finally:
        # Unsubscribe from consumer instance
        restrunner.kafkadelete(
            f"/consumers/{topic}_consumer_group/instances/{topic}_consumer_instance"
        )

    yield TASK_FINISHED


# MONITOR FUNCTIONS SHOULD RETURN
# "name": dict_item["type"],
# "time": dict_item["time"],
# "values": [
#     {"Tx": dict_item["tx"]},
#     {"Rx": dict_item["rx"]},
# ],

def dt_from_iso(timestring: str):
    # Workaround since received timestring with " AM"/" PM" suffix is not parsed properly
    isPM = " PM" in timestring
    dt = datetime.strptime(
        timestring.replace(" AM", "").replace(" PM", ""), "%Y-%m-%dT%H:%M:%S.%f%z"
    )
    return dt + timedelta(hours=12) if isPM else dt


def topic_stats(topic: str):
    demo = getdemo(app.storage.general["demo"]["name"])
    stream_path = f"{demo['volume']}/{demo['stream']}"
    # topic_path = quote(f"{stream_path}:{topic}", safe="")

    response = restrunner.get(f"/rest/stream/topic/info?path={stream_path}&topic={topic}")
    if isinstance(response, Exception):
        logger.warning(f"Failed to get metrics for {topic}: {response}")
    else:
        metrics = response.json()
        # logger.debug("GOT METRICS %s", metrics)
        series = []
        for m in metrics["data"]:
            series.append({"publishedMsgs": m["maxoffset"]})
            series.append({"consumedMsgs": m["minoffsetacrossconsumers"]})
            series.append(
                {
                    "latestAgo(s)": (
                        datetime.now().astimezone() - dt_from_iso(m["maxtimestamp"])
                    ).total_seconds()
                }
            )
            series.append(
                {
                    "consumerLag(s)": (
                        dt_from_iso(m["maxtimestamp"])
                        - dt_from_iso(m["mintimestampacrossconsumers"])
                    ).total_seconds()
                }
            )
        # logger.info("Metrics %s", series)
        return {
            "name": topic,
            "time": datetime.fromtimestamp(metrics["timestamp"]/(10**3)).strftime("%H:%M:%S"),
            "values": series,
        }


def consumer_stats(topic: str):
    demo = getdemo(app.storage.general["demo"]["name"])
    stream_path = f"{demo['volume']}/{demo['stream']}"

    response = restrunner.get(
        f"/rest/stream/cursor/list?path={stream_path}&topic={topic}"
    )
    if isinstance(response, Exception):
        logger.warning(f"Failed to get metrics for {topic}: {response}")
    else:
        metrics = response.json()
        # logger.debug("GOT METRICS %s", metrics)
        series = []
        for m in metrics["data"]:
            series.append({ f"{m['consumergroup']}_{m['partitionid']}_lag(s)": float(m["consumerlagmillis"])/1000})
            series.append({ f"{m['consumergroup']}_{m['partitionid']}_offsetBehind": int(m["produceroffset"]) - int(m['committedoffset'])})
        # logger.info("Metrics %s", series)
        return {
            "name": "Consumer",
            "time": datetime.fromtimestamp(metrics["timestamp"]/(10**3)).strftime("%H:%M:%S"),
            "values": series,
        }


# Dummy function for informational steps
def noop():
    return True

# def get_jmx_metrics():
#     buffertimestamp = (
#         datetime.now() - timedelta(minutes=0)
#     ).timestamp() * 10**6  # convert to microseconds

#     # logger.debug(
#     #     "Getting metrics from %s",
#     #     datetime.utcfromtimestamp(buffertimestamp/1_000_000).strftime("%Y-%m-%d %H:%M:%S"),
#     # )

#     response = restrunner.dagget(
#         f"/api/v2/table/%2Fapps%2Fezshowmonitor?orderBy=ts&fromId={buffertimestamp}"
#     )

#     # logger.debug("MONITOR GET RESPONSE: %s", response)

#     if isinstance(response, Exception):
#         logger.warning("MONITOR GET FAILED: %s", response)
#         return

#     if response is not None:
#         docs = response.json().get("DocumentStream", list())
#         if len(docs) > 0:
#             # print(docs)
#             for dict_item in sorted(docs, key=lambda x: x['ts']):
#                 yield {
#                     "name": dict_item["type"],
#                     "time": datetime.fromtimestamp(dict_item["time"]).time(),
#                     "values": [
#                         {"name": "Messages", "value": dict_item["msg_cnt"]},
#                         # {"name": "Rx", "value": dict_item["rx"]},
#                     ],
#                 }
#                 # yield { "x_axis": dict_item['time'], "y_axis": [ dict_item['tx'], dict_item['rx'] ] }
#             ######

#             # write to kafta stream, get json, return specific metrics/fields

#             ######
#             # import pandas as pd
#             # df = pd.json_normalize(docs)

#             # # print(df['type'])
#             # # print(df['time'])
#             # # print(df['msg_cnt'])
#             # # print(df['topics.banking.partitions.0.txmsgs'])

#             # metrics = df.pivot(index="ts", columns=["type"], values="msg_cnt")
#             # print(metrics)
#             # yield metrics


# def null_metrics():
#     # fake = Faker()
#     df = pd.DataFrame(columns=("timestamp", "metricA", "metricB"))
#     df.loc[0] = [datetime().now().timestamp(), 10*10, 5*10]
#     yield df
