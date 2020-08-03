import unittest
import unittest.mock

import os
import json

import service

class MockRedis(object):

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.channel = None
        self.messages = []

    def pubsub(self):

        return self

    def subscribe(self, channel):

        self.channel = channel

    def get_message(self):

        return self.messages.pop(0)


class MockgTTS(object):

    def __init__(self, text, lang=None):

        self.text = text
        self.lang = lang
        self.saved = None

    def save(self, file_name):

        self.saved = file_name


class TestService(unittest.TestCase):

    @unittest.mock.patch.dict(os.environ, {
        "NODE_NAME": "noisy",
        "REDIS_HOST": "most.com",
        "REDIS_PORT": "667",
        "REDIS_CHANNEL": "stuff",
        "SPEECH_FILE": "blah.mp3",
        "SLEEP": "7"
    })
    @unittest.mock.patch("redis.StrictRedis", MockRedis)
    def setUp(self):

        self.daemon = service.Daemon()

    @unittest.mock.patch.dict(os.environ, {
        "NODE_NAME": "noisy",
        "REDIS_HOST": "most.com",
        "REDIS_PORT": "667",
        "REDIS_CHANNEL": "stuff",
        "SPEECH_FILE": "blah.mp3",
        "SLEEP": "7"
    })
    @unittest.mock.patch("redis.StrictRedis", MockRedis)
    def test___init___(self):

        daemon = service.Daemon()

        self.assertEqual(daemon.node, "noisy")
        self.assertEqual(daemon.redis.host, "most.com")
        self.assertEqual(daemon.redis.port, 667)
        self.assertEqual(daemon.channel, "stuff")
        self.assertEqual(daemon.speech_file, "blah.mp3")
        self.assertEqual(daemon.sleep, 7)
        self.assertIsNone(daemon.pubsub)

    def test_subscribe(self):

        self.daemon.subscribe()

        self.assertEqual(self.daemon.redis, self.daemon.pubsub)
        self.assertEqual(self.daemon.redis.channel, "stuff")

    @unittest.mock.patch("gtts.gTTS", MockgTTS)
    @unittest.mock.patch("os.system")
    def test_speak(self, mock_system):

        self.daemon.speak("hey", "murican")

        self.assertEqual(self.daemon.tts.text, "hey")
        self.assertEqual(self.daemon.tts.lang, "murican")
        self.assertEqual(self.daemon.tts.saved, "blah.mp3")
        mock_system.assert_called_once_with("mpg123 -q blah.mp3")

    @unittest.mock.patch("gtts.gTTS", MockgTTS)
    @unittest.mock.patch("os.system")
    def test_process(self, mock_system):

        self.daemon.subscribe()

        self.daemon.redis.messages = [
            {
                "data": json.dumps({
                    "timestamp": 7,
                    "text": "hey",
                    "node": "noisy"
                })
            },
            {
                "data": json.dumps({
                    "timestamp": 7,
                    "text": "hey",
                    "language": "murican",
                    "node": "*"
                })
            }
        ]

        self.daemon.process()
        self.assertEqual(self.daemon.tts.text, "hey")
        self.assertEqual(self.daemon.tts.lang, "en")

        self.daemon.process()
        self.assertEqual(self.daemon.tts.text, "hey")
        self.assertEqual(self.daemon.tts.lang, "murican")

    @unittest.mock.patch("gtts.gTTS", MockgTTS)
    @unittest.mock.patch("os.system")
    @unittest.mock.patch("service.time.sleep")
    def test_run(self, mock_sleep, mock_system):

        self.daemon.redis.messages = [
            {
                "data": json.dumps({
                    "timestamp": 7,
                    "text": "hey",
                    "language": "murican",
                    "node": "noisy"
                })
            },
            None,
            None
        ]

        mock_sleep.side_effect = [None, Exception("whoops")]

        self.assertRaisesRegex(Exception, "whoops", self.daemon.run)

        self.assertEqual(self.daemon.tts.text, "hey")
        self.assertEqual(self.daemon.tts.lang, "murican")
        self.assertEqual(self.daemon.tts.saved, "blah.mp3")

        mock_system.assert_called_with("mpg123 -q blah.mp3")
