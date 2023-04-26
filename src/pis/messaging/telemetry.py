import paho.mqtt.client as mqtt
from pis.utils.Event import Reactive
'''
    Example instance:
        conn = Connection("localhost", 1883)
        conn.connect("admin", "pass123")
        conn.subscribe("test/topic")

        # many-to-one default subscription
            conn.subscribe([("topic1", 0), ("topic2", 1)])

        # many-to-one anonymous subscriptions
            conn.subscribe([("topic1", 0), ("topic2", 1)], lambda client, userdata, message : (
                print("anonymous hook on all related topics")
            ))

        # many-to-many anoanymous subscriptions
            conn.subscribe_multiple([
                ("topic1/#", lambda client, userdata, message : (
                    print("hook on topic 1"))
                ),

                ("topic2/#", lambda client, userdata, message : (
                    print("hook on topic 2)
                )),

                (...) 
            ])


        conn.publish("test/topic", "Hello World")
        conn.disconnect()
'''

class Connection:
    
    def __init__(self, url, port, keepalive=60):
        self.hostname = url
        self.port = port
        self.keepalive = keepalive

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect 
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.topics = set()
        
        self.connectionEventHandler = Reactive(0)

    def __del__(self):
        self.disconnect()

    def connect(self, username=None, password=None):
        self.client.username_pw_set(username, password)
        self.client.connect(self.hostname, self.port, self.keepalive)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        print("Connection result: {}".format(mqtt.connack_string(rc)))
        if rc != mqtt.CONNACK_ACCEPTED:
           #raise IOError("couldn't establish connection to a broker")
           raise SystemExit("couldn't establish connection to a broker")
        self.connectionEventHandler.value = True
        
    def on_connection(self, event):
        if self.client.is_connected(): event()
        else:
            self.connectionEventHandler.watch(event)

    def on_disconnect(self, client, userdata, rc):
        print("client disconnected")

    def on_message(self, client, userdata, message):
        print("received message '" + message.topic + "': " + message.payload.decode("utf-8"))

    def subscribe(self, topics, callback=None, qos=0):
        """
        args:
            callback (callable, optional): The callback function should accept three arguments: client, userdata, and message. 
                If no callback is specified, messages will hoist on default :on_message method.
            qos (int, optional): The QoS level to use for the subscription (0, 1, or 2). Default is 0.

        callable example:
            client.subscribe("topic/#", lambda client, userdata, message : (
                print("received topic message '" + message.topic "'")
            ))

        """                                                  # TODO : Subscription overwrites from another object on same topic, when it should not
        if callable(callback):
            self.client.message_callback_add(topics, callback)

        self.client.subscribe(topics, qos)
                
        return self


    def subscribe_multiple(self, topics, qos=0):
        '''
        example usage:

            conn.subscribe_multiple([
                    ("topic1", lambda client, userdata, message : (
                        print("hook on topic 1"))
                    ),

                    ("topic2", lambda client, userdaa, message: (
                        print("hook on topic 2)
                    )),

                    (...) 
                ])
        '''
        tuples = []
        for topic, callback in topics:
            if callable(callback):
                self.client.message_callback_add(topic, callback)
            else: 
                print("expected a callable, received: " + str(type(callback)))       # TODO : Subscription overwrites from another object on same topic
            tuples.append((topic, qos))
                
       
           
            self.client.subscribe(tuples, qos)
            
        return self
    
    def unsubscribe(self, topic):
        self.client.unsubscribe(topic)

    def set_user_data(self, payload=None):
        ''' Set the private user data payload that will be passed to callbacks when events are generated. '''
        self.client.user_data_set(payload)
        return self

    def set_last_will(self, topic, payload=None, qos=0, retain=False):
        ''' Set a LWT message to be sent to the broker. If the client disconnects without calling disconnect(), the broker will publish the message on its behalf. '''
        self.client.will_set(topic, payload, qos, retain)
        return self

    def publish(self, topic, payload=None, qos=0, retain=False):
        '''
        args:
            qos (optional): QoS (The Quality Of Service) level to use for the subscription (0, 1, or 2).
            retain (optional): Keep the most recently published message with the same topic and QoS for this client.
        '''
        return self.client.publish(topic, payload, qos, retain)


'''
    def subscribe_multiple_x(self, topics, qos=0):
        tuples = []
        for topic, callback in topics:
            if callable(callback):
                self.client.message_callback_add(topic, callback)
            else: 
                print("expected a callable, received: " + str(type(callback)))

            tuples.append((topic, qos))

        self.client.subscribe(tuples, qos)

    def subscribe_x(self, topic, callback=None, qos=0):
        """
        args:
            callback (callable, optional): The callback function should accept three arguments: client, userdata, and message. 
                If no callback is specified, messages will hoist on default :on_message method.
            qos (int, optional): The QoS level to use for the subscription (0, 1, or 2). Default is 0.

        callable example:
            client.subscribe("topic/#", lambda client, userdata, message : (
                print("received topic message '" + message.topic "'")
            ))

        """
        if callable(callback):
            self.client.message_callback_add(topic, callback)
        return self.client.subscribe(topic, qos)
'''