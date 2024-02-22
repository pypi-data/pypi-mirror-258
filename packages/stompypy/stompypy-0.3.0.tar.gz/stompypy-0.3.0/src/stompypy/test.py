import logging
import time

from stompypy import Listener
from stompypy import Stomp


class MyListener(Listener):
    def on_disconnect(self):
        print('Disconnected ')

    def on_connect(self):
        print('Connected')

    def on_message(self, frame) -> None:
        print('Message:', frame.body)


if __name__ == '__main__':
    logger = logging.getLogger('stompypy')
    logger.setLevel(logging.DEBUG)

    # Create a STOMP connection to the server
    connection = Stomp.create_connection(host='127.0.0.1', port=61613)

    # Add listener
    connection.add_listener(MyListener())

    # Connect to the STOMP server
    connection.connect()

    # Subscribe to a destination
    connection.subscribe(id='1', destination='/queue/example', ack_mode='auto')

    # Send a message to the destination
    connection.send(destination='/queue/example', content_type='text/plain', body='Hello World!')

    time.sleep(1)

    # Disconnect from the server
    connection.disconnect()
