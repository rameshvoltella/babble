# -*- coding: utf-8 -*-
import base64
import random
import string
import urllib
from django.template import TemplateDoesNotExist
from models import *
import json, importer, data, random, utils

import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

LOG = logging.getLogger("pages")

class IndexPage(webapp.RequestHandler):
    def get(self):
        values = {
            "var1":"hallo",
        }
        self.response.out.write(template.render('templates/index.html', values))

class TempPage(webapp.RequestHandler):
    def get(self):
        importer.importSentences(data.list)
        self.response.out.write("Done ... ")

class AllSentencesPage(webapp.RequestHandler):
    def get(self):
        results = {}
        list = Sentence.all()

        for sentence in list:
            group = results.get(sentence.group)

            if not group:
                group = {}
                results[sentence.group] = group

            group[sentence.locale] = {
                "id": sentence.key().id(),
                "value": sentence.value
            }

        results2 = []
        for key, value in results.items():
            results2.append({"group":key, "values": value})

        random.shuffle(results2)
        self.response.headers["Content-Type"] = "text/plain; charset=utf-8"
        self.response.out.write(json.dumps({"list": results2}, indent=4))

class SingleSentencesPage(webapp.RequestHandler):
    def get(self, path):
        locale = string.replace(path, "/", "")
        results = []
        list = Sentence.gql("WHERE locale = :paramLocale", paramLocale = locale)

        for sentence in list:
            results.append({
                "id": sentence.key().id(),
                "group": sentence.group,
                "value": sentence.value,
                "locale": sentence.locale
            })

        random.shuffle(results)
        self.response.headers["Content-Type"] = "text/plain; charset=utf-8"
        self.response.out.write(json.dumps({"list": results}, indent=4))


class HistoryPage(webapp.RequestHandler):
    def get(self):
        values = {}

class SaveAssessment(webapp.RequestHandler):
    def get(self): # it's easier to test this functionality with a get method
        # self.response.out.write('TEST')
        self.post()

    def post(self):
        phoneId = self.request.get('phoneId')
        sentenceId = self.request.get('sentenceId')
        score = int(self.request.get('score'))
        resultFromTTS = self.request.get('resultFromTTS')
        date_created = self.request.get('date_created')

        self.response.out.write(phoneId)
        self.response.out.write(sentenceId)
        self.response.out.write(score)
        self.response.out.write(resultFromTTS)
        self.response.out.write(date_created)

        Assessment(phoneId = phoneId,sentenceId = sentenceId,resultFromTTS=resultFromTTS,score=score).save()

        self.response.headers["Content-Type"] = "text/plain; charset=utf-8"
        self.response.out.write('TEST') # json.dumps({"test": "d"}, indent=4))

