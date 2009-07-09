import os
from google.appengine.ext.webapp import template


def get_template_url(endpoint, format):
	template_url = "templates/" + endpoint + "." + format 
	return template_url


def render_template(self, endpoint, templatevalues, format):
	if format == "xml":
		self.response.headers['Content-Type'] = 'application/xml'
	path = os.path.join(os.path.dirname(__file__), get_template_url(endpoint, format))
	self.response.out.write(template.render(path, templatevalues))


