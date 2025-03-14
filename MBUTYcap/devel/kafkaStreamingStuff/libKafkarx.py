import time
import configargparse as argparse

import matplotlib.pyplot as plt
import numpy as np
from confluent_kafka import Consumer, TopicPartition
import RawReadoutMessage as rawmsg


def generate_config(brokers, staging):
    return {
        "bootstrap.servers": ",".join(brokers),
        "group.id": f"consumer-{time.time_ns()}",
        "auto.offset.reset": "latest",
    }


def _get_metadata_blocking(consumer):
    while True:
        try:
            return consumer.list_topics(timeout=1)
        except Exception:
            print("Cannot get topic metadata - broker(s) down?")
            time.sleep(0.1)


def main(kafka_config, topic):
    consumer = Consumer(kafka_config)

    metadata = _get_metadata_blocking(consumer)
    if topic not in metadata.topics:
        raise Exception("Topic does not exist")

    topic_partitions = [
        TopicPartition(topic, p) for p in metadata.topics[topic].partitions
    ]

    consumer.assign(topic_partitions)


    # Main Kafka receive loop
    while (True):
        while (msg := consumer.poll(timeout=0.5)) is None:
            time.sleep(0.1)

        # we have a message
        ar52 = rawmsg.RawReadoutMessage.GetRootAs(msg.value(), 0)
        npdata = ar52.RawDataAsNumpy()
        oq = npdata[8]
        datalen = npdata[7] * 256 +  npdata[6]
        print(f'OQ: {oq}, DataLen: {datalen}')
        print(npdata)
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-b", "--broker", type=str, help="the broker address", required=True
    )

    required_args.add_argument(
        "-t", "--topic", type=str, help="the config topic", required=True
    )

    args = parser.parse_args()

    kafka_config = generate_config(args.broker, True)

    main(kafka_config, args.topic)
