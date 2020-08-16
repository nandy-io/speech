import unittest
import unittest.mock
import klotio_unittest

import os
import json

import service

class TestRestful(klotio_unittest.TestCase):

    @unittest.mock.patch.dict(os.environ, {
        "REDIS_HOST": "most.com",
        "REDIS_PORT": "667",
        "REDIS_CHANNEL": "stuff"
    })
    @unittest.mock.patch("redis.Redis", klotio_unittest.MockRedis)
    @unittest.mock.patch("klotio.logger", klotio_unittest.MockLogger)
    def setUp(self):

        self.app = service.build()
        self.api = self.app.test_client()


class TestAPI(TestRestful):

    @unittest.mock.patch.dict(os.environ, {
        "REDIS_HOST": "most.com",
        "REDIS_PORT": "667",
        "REDIS_CHANNEL": "stuff"
    })
    @unittest.mock.patch("redis.Redis", klotio_unittest.MockRedis)
    @unittest.mock.patch("klotio.logger", klotio_unittest.MockLogger)
    def test_app(self):

        app = service.build()

        self.assertEqual(app.name, "nandy-io-speech-api")
        self.assertEqual(app.redis.host, "most.com")
        self.assertEqual(app.redis.port, 667)
        self.assertEqual(app.channel, "stuff")

        self.assertEqual(app.logger.name, "nandy-io-speech-api")

        self.assertLogged(app.logger, "debug", "init", extra={
            "init": {
                "redis": {
                    "connection": "MockRedis<host=most.com,port=667>",
                    "channel": "stuff"
                }
            }
        })


class TestHealth(TestRestful):

    def test_get(self):

        self.assertStatusValue(self.api.get("/health"), 200, "message", "OK")


class TestGroup(TestRestful):

    @unittest.mock.patch("requests.get")
    def test_get(self, mock_get):

        mock_get.return_value.json.return_value = [{
            "name": "unit",
            "url": "test"
        }]

        self.assertStatusValue(self.api.get("/group"), 200, "group", [{
            "name": "unit",
            "url": "test"
        }])

        mock_get.assert_has_calls([
            unittest.mock.call("http://api.klot-io/app/speech.nandy.io/member"),
            unittest.mock.call().raise_for_status(),
            unittest.mock.call().json()
        ])

class TestSpeak(TestRestful):

    @unittest.mock.patch("klotio.settings")
    def test_options(self, mock_settings):

        mock_settings.return_value = {
            "speakers": [
                "unittest"
            ]
        }

        self.assertStatusFields(self.api.options("/speak"), 200, [
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
        ])

        self.assertLogged(self.app.logger, "debug", "request", extra={
            "request": {
                "method": "OPTIONS",
                "path": "/speak",
                "remote_addr": "127.0.0.1"
            }
        })

        self.assertLogged(self.app.logger, "debug", "response", extra={
            "response": {
                "status_code": 200,
                "json": {
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
                }
            }
        })

        self.assertStatusFields(self.api.options("/speak", json={"speak": {"node": "womp"}}), 200, [
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
        ], errors=[])

    @unittest.mock.patch("klotio.settings")
    @unittest.mock.patch("service.time.time", unittest.mock.MagicMock(return_value=7.0))
    def test_post(self, mock_settings):

        mock_settings.return_value = {
            "speakers": [
                "unittest"
            ]
        }

        self.assertStatusValue(self.api.post("/speak"), 400, "errors", ["missing speak"])

        self.assertLogged(self.app.logger, "debug", "request", extra={
            "request": {
                "method": "POST",
                "path": "/speak",
                "remote_addr": "127.0.0.1"
            }
        })

        self.assertLogged(self.app.logger, "debug", "response", extra={
            "response": {
                "status_code": 400,
                "json": {
                    "errors": ["missing speak"]
                }
            }
        })

        self.assertStatusFields(self.api.post("/speak", json={"speak": {"node": "womp"}}), 400, [
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
        ], errors=[])

        self.assertStatusValue(self.api.post("/speak", json={
            "speak": {
                "text": "hi",
                "language": "en-AU"
            }
        }), 202, "message", {
            "timestamp": 7,
            "text": "hi",
            "language": "en-AU"
        })
        self.assertEqual(self.app.redis.channel, "stuff")
        self.assertEqual(json.loads(self.app.redis.messages[0]), {
            "timestamp": 7,
            "text": "hi",
            "language": "en-AU"
        })

        self.assertStatusValue(self.api.post("/speak", json={
            "speak": {
                "text": "hi",
                "language": "en-AU",
                "node": "unittest"
            }
        }), 202, "message", {
                "timestamp": 7,
                "text": "hi",
                "language": "en-AU",
                "node": "unittest"
        })
        self.assertEqual(self.app.redis.channel, "stuff")
        self.assertEqual(json.loads(self.app.redis.messages[1]), {
            "timestamp": 7,
            "text": "hi",
            "language": "en-AU",
            "node": "unittest"
        })

class TestIntegrate(TestRestful):

    @unittest.mock.patch("klotio.settings")
    def test_options(self, mock_settings):

        mock_settings.return_value = {
            "speakers": [
                "unittest"
            ]
        }

        self.assertStatusFields(self.api.options("/integrate"), 200, [
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
        ])

        self.assertLogged(self.app.logger, "debug", "request", extra={
            "request": {
                "method": "OPTIONS",
                "path": "/integrate",
                "remote_addr": "127.0.0.1"
            }
        })

        self.assertLogged(self.app.logger, "debug", "response", extra={
            "response": {
                "status_code": 200,
                "json": {
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
                }
            }
        })
