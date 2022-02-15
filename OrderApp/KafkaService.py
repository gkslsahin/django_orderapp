from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import loads, dumps
import threading
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from OrderApp.serializers import OrderSerializer


class KafkaService:
    def __init__(
        self,
        bootstrap_servers="kafka:9092",
        topic="channel",
    ) -> None:
        print("creating KafkaService...")
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.consumer = None
        self.value_serializer = lambda x: dumps(x).encode("utf-8")
        self.value_deserializer = lambda x: loads(x.decode("utf-8"))
        self.topic = topic
        self.consumer_thread = None
        self.process_order_status = ""

        self.create_topic()
        self.init_consumer()
        self.init_producer()

    def init_consumer(self):
        print("initializing consumer...")
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=self.value_deserializer,
        )
        self.consumer_thread = threading.Thread(target=self.consumer_thread_func)
        self.consumer_thread.start()

    def init_producer(self):
        print("initializing producer...")
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=self.value_serializer,
        )

    def create_topic(self):
        admin_client = KafkaAdminClient(
            bootstrap_servers=self.bootstrap_servers, client_id="test"
        )
        topic_list = []
        topic_list.append(
            NewTopic(name="example_topic", num_partitions=1, replication_factor=1)
        )
        try:
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
        except TopicAlreadyExistsError:
            print(self.topic + " is alreadly exist.")
        except Exception as err:
            print(str(err))

    def send_to_topic(self, msg):
        self.producer.send(self.topic, msg)

    def consumer_thread_func(self):
        print("starting consumer thread...")
        for msg in self.consumer:
            print(msg)
            # self.process_order_func(msg)
            self.process_order(msg)

    def stop_consumer_thread(self):
        self.consumer_thread.terminate()
        self.consumer_thread.join()

    def process_order(self, order_data):
        order_serializer = OrderSerializer(data=order_data.value)
        if order_serializer.is_valid(True):
            order_serializer.save()
