"""
Main module for daemon
"""

import os
import time

import json
import yaml
import redis
import gtts
import patch

import klotio

class Daemon(object):
    """
    Main class for daemon
    """

    def __init__(self):

        self.node = os.environ['NODE_NAME']

        self.speech_file = os.environ['SPEECH_FILE']
        self.sleep = int(os.environ['SLEEP'])

        self.redis = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']))
        self.channel = os.environ['REDIS_CHANNEL']

        self.pubsub = None
        self.tts = None

        self.logger = klotio.logger("nandy-io-speech-daemon")

        self.logger.debug("settings", extra={
            "settings": {
                "node": self.node,
                "sleep": self.sleep,
                "redis": str(self.redis),
                "channel": self.channel
            }
        })

    def subscribe(self):
        """
        Subscribes to the channel on Redis
        """

        self.logger.info("subscribing")

        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(self.channel)

    def speak(self, text, language):
        """
        Speaks the text in the language
        """

        speak = {
            "text": text,
            "language": language
        }

        self.logger.info("speak", extra={"speak": speak})

        self.tts = gtts.gTTS(text, lang=language)
        self.tts.save(self.speech_file)
        os.system("mpg123 -q %s" % self.speech_file)

    def process(self):
        """
        Processes a message from the channel if later than the daemons start time
        """

        message = self.pubsub.get_message()

        self.logger.debug("get_message", extra={"get_message": message})

        if not message or not isinstance(message.get("data"), (str, bytes)):
            return

        data = json.loads(message['data'])

        self.logger.info("data", extra={"data": data})

        if data.get("node") in ["*", self.node]:
            self.speak(data["text"], data.get("language", "en"))

    def run(self):
        """
        Runs the daemon
        """

        self.subscribe()

        while True:
            self.process()
            time.sleep(self.sleep)
