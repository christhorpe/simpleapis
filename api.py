#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import wsgiref.handlers
import urllib


from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext import search
from google.appengine.api import memcache

import models
import helpers


def urldecode(value):
    return  urllib.unquote(urllib.unquote(value)).decode('utf8')



class ItemHandler(webapp.RequestHandler):
	def get(self, urn):
		key = "item_" + urn
		school = memcache.get(key)
		if not school:
			query = models.SchoolImport.all()
			query.filter("urn =", int(urn))
			school = query.get()
			memcache.add(key, school, 60)
		template_values = {
			"urn": urn,
			"school": school
		}
		helpers.render_template(self, "school", template_values, "xml")


class ItemsHandler(webapp.RequestHandler):
	def get(self, parameter_name, parameter_value):
		parameter_value = urldecode(parameter_value)
		queryfilter = parameter_name + " ="
		query = db.Query(models.SchoolImport)
		query.filter(queryfilter, parameter_value)
		schools = query.fetch(1000)
		template_values = {
			"list": True,
			"parameter_name": parameter_name,
			"parameter_value": parameter_value,
			"schools": schools
		}
		helpers.render_template(self, "schools", template_values, "xml")



class SearchHandler(webapp.RequestHandler):
  def get(self):
		query = search.SearchableQuery('SchoolImport')
		query.Search(self.request.get("query"))
		count = query.Count(100)  
		schools = query.Run()
		template_values = {
			"search": True,
			"query": self.request.get("query"),
			"count": count,
			"schools": schools
		}
		helpers.render_template(self, "schools", template_values, "xml")



def main():
  application = webapp.WSGIApplication([
	('/schools-api/item/(.*)', ItemHandler),
	('/schools-api/items/(.*)/(.*)', ItemsHandler),
	('/schools-api/search', SearchHandler)
  ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
