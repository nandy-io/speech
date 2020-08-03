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

class Daemon(object):
    """
    Main class for daemon
    """

    def __init__(self):

        self.node = os.environ['NODE_NAME']

        self.speech_file = os.environ['SPEECH_FILE']
        self.sleep = int(os.environ['SLEEP'])

        self.redis = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']))
        self.channel = os.environ['REDIS_CHANNEL']

        self.pubsub = None
        self.tts = None

    def subscribe(self):
        """
        Subscribes to the channel on Redis
        """

        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(self.channel)

    def speak(self, text, language):
        """
        Speaks the text in the language
        """

        self.tts = gtts.gTTS(text, lang=language)
        self.tts.save(self.speech_file)
        os.system("mpg123 -q %s" % self.speech_file)

    def process(self):
        """
        Processes a message from the channel if later than the daemons start time
        """

        message = self.pubsub.get_message()

        if not message:
            return

        data = json.loads(message['data'])

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
