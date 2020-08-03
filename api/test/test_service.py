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

    def publish(self, channel, message):

        self.channel = channel
        self.messages.append(message)

class TestService(unittest.TestCase):

    maxDiff = None

    @unittest.mock.patch.dict(os.environ, {
        "REDIS_HOST": "most.com",
        "REDIS_PORT": "667",
        "REDIS_CHANNEL": "stuff"
    })
    @unittest.mock.patch("redis.StrictRedis", MockRedis)
    def setUp(self):

        self.app = service.app()
        self.api = self.app.test_client()

    @unittest.mock.patch.dict(os.environ, {
        "REDIS_HOST": "most.com",
        "REDIS_PORT": "667",
        "REDIS_CHANNEL": "stuff"
    })
    @unittest.mock.patch("redis.StrictRedis", MockRedis)
    def test_app(self):

        app = service.app()

        self.assertEqual(app.redis.host, "most.com")
        self.assertEqual(app.redis.port, 667)
        self.assertEqual(app.channel, "stuff")

    def test_health(self):

        self.assertEqual(self.api.get("/health").json, {"message": "OK"})

    @unittest.mock.patch("requests.get")
    def test_group(self, mock_get):

        mock_get.return_value.json.return_value = [{
            "name": "unit",
            "url": "test"
        }]

        self.assertEqual(self.api.get("/group").json, {"group": [{
            "name": "unit",
            "url": "test"
        }]})

        mock_get.assert_has_calls([
            unittest.mock.call("http://api.klot-io/app/speech.nandy.io/member"),
            unittest.mock.call().raise_for_status(),
            unittest.mock.call().json()
        ])

    @unittest.mock.patch("builtins.open", create=True)
    @unittest.mock.patch("service.time.time")
    def test_Speak(self, mock_time, mock_open):

        mock_open.side_effect = [
            unittest.mock.mock_open(read_data='speakers:\n- unittest').return_value,
            unittest.mock.mock_open(read_data='speakers:\n- unittest').return_value,
            unittest.mock.mock_open(read_data='speakers:\n- unittest').return_value,
            unittest.mock.mock_open(read_data='speakers:\n- unittest').return_value,
            unittest.mock.mock_open(read_data='speakers:\n- unittest').return_value
        ]

        response = self.api.options("/speak")
        self.assertEqual(response.status_code, 200, response.json)
        self.assertEqual(response.json, {
            "fields": [
                {
                    "name": "text"
                },
                {
                    "name": "language",
                    "options": [
                        "en-AU",
                        "en-CA",
                        "en-GH",
                        "en-GB",
                        "en-IN",
                        "en-IE",
                        "en-KE",
                        "en-NZ",
                        "en-NG",
                        "en-PH",
                        "en-SG",
                        "en-ZA",
                        "en-TZ",
                        "en-US"
                    ],
                    "labels": {
                        "en-AU": "English (Australia)",
                        "en-CA": "English (Canada)",
                        "en-GH": "English (Ghana)",
                        "en-GB": "English (United Kingdom)",
                        "en-IN": "English (India)",
                        "en-IE": "English (Ireland)",
                        "en-KE": "English (Kenya)",
                        "en-NZ": "English (New Zealand)",
                        "en-NG": "English (Nigeria)",
                        "en-PH": "English (Philippines)",
                        "en-SG": "English (Singapore)",
                        "en-ZA": "English (South Africa)",
                        "en-TZ": "English (Tanzania)",
                        "en-US": "English (United States)"
                    },
                    "default": "en-US",
                    "style": "select",
                    "optional": True
                },
                {
                    "name": "node",
                    "options": [
                        "*",
                        "unittest"
                    ],
                    "labels": {
                        "*": "all",
                        "unittest": "unittest"
                    },
                    "default": "",
                    "optional": True
                }
            ]
        })

        response = self.api.options("/speak", json={"speak": {"node": "womp"}})
        self.assertEqual(response.status_code, 200, response.json)
        self.assertEqual(response.json, {
            "fields": [
                {
                    "name": "text",
                    "errors": ["missing value"]
                },
                {
                    "name": "language",
                    "options": [
                        "en-AU",
                        "en-CA",
                        "en-GH",
                        "en-GB",
                        "en-IN",
                        "en-IE",
                        "en-KE",
                        "en-NZ",
                        "en-NG",
                        "en-PH",
                        "en-SG",
                        "en-ZA",
                        "en-TZ",
                        "en-US"
                    ],
                    "labels": {
                        "en-AU": "English (Australia)",
                        "en-CA": "English (Canada)",
                        "en-GH": "English (Ghana)",
                        "en-GB": "English (United Kingdom)",
                        "en-IN": "English (India)",
                        "en-IE": "English (Ireland)",
                        "en-KE": "English (Kenya)",
                        "en-NZ": "English (New Zealand)",
                        "en-NG": "English (Nigeria)",
                        "en-PH": "English (Philippines)",
                        "en-SG": "English (Singapore)",
                        "en-ZA": "English (South Africa)",
                        "en-TZ": "English (Tanzania)",
                        "en-US": "English (United States)"
                    },
                    "default": "en-US",
                    "style": "select",
                    "optional": True,
                    "value": "en-US"
                },
                {
                    "name": "node",
                    "options": [
                        "*",
                        "unittest"
                    ],
                    "labels": {
                        "*": "all",
                        "unittest": "unittest"
                    },
                    "default": "",
                    "optional": True,
                    "value": "womp",
                    "errors": ["invalid value 'womp'"]
                }
            ],
            "errors": []
        })

        response = self.api.post("/speak")
        self.assertEqual(response.status_code, 400, response.json)
        self.assertEqual(response.json["errors"], ["missing speak"])

        response = self.api.post("/speak", json={"speak": {"node": "womp"}})
        self.assertEqual(response.status_code, 400, response.json)
        self.assertEqual(response.json, {
            "fields": [
                {
                    "name": "text",
                    "errors": ["missing value"]
                },
                {
                    "name": "language",
                    "options": [
                        "en-AU",
                        "en-CA",
                        "en-GH",
                        "en-GB",
                        "en-IN",
                        "en-IE",
                        "en-KE",
                        "en-NZ",
                        "en-NG",
                        "en-PH",
                        "en-SG",
                        "en-ZA",
                        "en-TZ",
                        "en-US"
                    ],
                    "labels": {
                        "en-AU": "English (Australia)",
                        "en-CA": "English (Canada)",
                        "en-GH": "English (Ghana)",
                        "en-GB": "English (United Kingdom)",
                        "en-IN": "English (India)",
                        "en-IE": "English (Ireland)",
                        "en-KE": "English (Kenya)",
                        "en-NZ": "English (New Zealand)",
                        "en-NG": "English (Nigeria)",
                        "en-PH": "English (Philippines)",
                        "en-SG": "English (Singapore)",
                        "en-ZA": "English (South Africa)",
                        "en-TZ": "English (Tanzania)",
                        "en-US": "English (United States)"
                    },
                    "default": "en-US",
                    "style": "select",
                    "optional": True,
                    "value": "en-US"
                },
                {
                    "name": "node",
                    "options": [
                        "*",
                        "unittest"
                    ],
                    "labels": {
                        "*": "all",
                        "unittest": "unittest"
                    },
                    "default": "",
                    "optional": True,
                    "value": "womp",
                    "errors": ["invalid value 'womp'"]
                }
            ],
            "errors": []
        })

        mock_time.return_value = 7

        response = self.api.post("/speak", json={
            "speak": {
                "text": "hi",
                "language": "en-AU"
            }
        })
        self.assertEqual(response.status_code, 202, response.json)
        self.assertEqual(response.json, {
            "message": {
                "timestamp": 7,
                "text": "hi",
                "language": "en-AU"
            }
        })
        self.assertEqual(self.app.redis.channel, "stuff")
        self.assertEqual(json.loads(self.app.redis.messages[0]), {
            "timestamp": 7,
            "text": "hi",
            "language": "en-AU"
        })

        response = self.api.post("/speak", json={
            "speak": {
                "text": "hi",
                "language": "en-AU",
                "node": "unittest"
            }
        })
        self.assertEqual(response.status_code, 202, response.json)
        self.assertEqual(response.json, {
            "message": {
                "timestamp": 7,
                "text": "hi",
                "language": "en-AU",
                "node": "unittest"
            }
        })
        self.assertEqual(self.app.redis.channel, "stuff")
        self.assertEqual(json.loads(self.app.redis.messages[1]), {
            "timestamp": 7,
            "text": "hi",
            "language": "en-AU",
            "node": "unittest"
        })

    @unittest.mock.patch("builtins.open", create=True)
    def test_Integrate(self, mock_open):

        mock_open.side_effect = [
            unittest.mock.mock_open(read_data='speakers:\n- unittest').return_value
        ]

        response = self.api.options("/integrate")
        self.assertEqual(response.status_code, 200, response.json)
        self.assertEqual(response.json, {
            "fields": [
                {
                    "name": "language",
                    "options": [
                        "en-AU",
                        "en-CA",
                        "en-GH",
                        "en-GB",
                        "en-IN",
                        "en-IE",
                        "en-KE",
                        "en-NZ",
                        "en-NG",
                        "en-PH",
                        "en-SG",
                        "en-ZA",
                        "en-TZ",
                        "en-US"
                    ],
                    "labels": {
                        "en-AU": "English (Australia)",
                        "en-CA": "English (Canada)",
                        "en-GH": "English (Ghana)",
                        "en-GB": "English (United Kingdom)",
                        "en-IN": "English (India)",
                        "en-IE": "English (Ireland)",
                        "en-KE": "English (Kenya)",
                        "en-NZ": "English (New Zealand)",
                        "en-NG": "English (Nigeria)",
                        "en-PH": "English (Philippines)",
                        "en-SG": "English (Singapore)",
                        "en-ZA": "English (South Africa)",
                        "en-TZ": "English (Tanzania)",
                        "en-US": "English (United States)"
                    },
                    "default": "en-US",
                    "style": "select",
                    "optional": True
                },
                {
                    "name": "node",
                    "options": [
                        "*",
                        "unittest"
                    ],
                    "labels": {
                        "*": "all",
                        "unittest": "unittest"
                    },
                    "default": "",
                    "optional": True
                }
            ]
        })
