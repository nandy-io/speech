import os
import sys
import time
import json
import yaml
import logging
import functools
import traceback

import redis
import flask
import flask_restful
import opengui
import requests

import klotio
import klotio_flask_restful


def app():

    app = flask.Flask("nandy-io-speech-api")

    app.redis = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']))
    app.channel = os.environ['REDIS_CHANNEL']

    api = flask_restful.Api(app)

    api.add_resource(klotio_flask_restful.Health, '/health')
    api.add_resource(Group, '/group')
    api.add_resource(Speak, '/speak')
    api.add_resource(Integrate, '/integrate')

    app.logger = klotio.logger(app.name)

    app.logger.debug("init", extra={
        "init": {
            "redis": {
                "connection": str(app.redis),
                "channel": app.channel
            }
        }
    })

    return app


class Group(klotio_flask_restful.Group):
    APP = "speech.nandy.io"


class Speak(flask_restful.Resource):

    name = "speak"

    @staticmethod
    def fields(values=None):

        fields = opengui.Fields(values, fields=[
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
                    "*"
                ],
                "labels": {
                    "*": "all"
                },
                "default": "",
                "optional": True
            }
        ])

        for node in klotio.settings()["speakers"]:
            fields["node"].options.append(node)
            fields["node"].content["labels"][node] = node

        return fields

    @klotio_flask_restful.logger
    def options(self):

        values = flask.request.json[self.name] if flask.request.json and self.name in flask.request.json else None

        fields = self.fields(values)

        if values and not fields.validate():
            return {"fields": fields.to_list(), "errors": fields.errors}
        else:
            return {"fields": fields.to_list()}

    @klotio_flask_restful.logger
    def post(self):

        if not flask.request.json or self.name not in flask.request.json:
            return {"errors": ["missing %s" % self.name]}, 400

        fields = self.fields(flask.request.json[self.name])

        if not fields.validate():
            return {"fields": fields.to_list(), "errors": fields.errors}, 400

        message = {
            "timestamp": time.time(),
            "text": fields["text"].value,
            "language": fields["language"].value
        }

        if fields["node"].value:
            message["node"] = fields["node"].value

        flask.current_app.redis.publish(flask.current_app.channel, json.dumps(message))

        return {"message": message}, 202

class Integrate(flask_restful.Resource):

    @klotio_flask_restful.logger
    def options(self):

        return {"fields": Speak.fields().to_list()[1:]}
