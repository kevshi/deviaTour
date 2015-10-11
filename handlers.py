import jinja2, datetime
import webapp2, uuid, time, logging, urllib, base64, os
import requests

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class BaseHandler(webapp2.RequestHandler):

	def render_template(self, view_filename, params=None):
		if not params:
			params = {}
		template = JINJA_ENVIRONMENT.get_template(view_filename)

		params['botcurtime'] = str(datetime.datetime.utcnow())
		self = addResponseHeaders(self)
		self.response.out.write(template.render(params))

class MainHandler(BaseHandler):
	def get(self):
		params = {}
		self.render_template('templates/home.html', params)

class AboutHandler(BaseHandler):
	def get(self):
		params = {}
		self.render_template('templates/about.html', params)

def addResponseHeaders(self):
	self.response.headers["X-Frame-Options"] = "sameorigin"
	self.response.headers["X-Content-Type-Options"] = "nosniff"
	self.response.headers["Strict-Transport-Security"] = "max-age=31536000"
	self.response.headers["Content-Type"] = "text/html; charset=utf-8"
	self.response.headers["X-XSS-Protection"] = "1; mode=block"
	self.response.headers["Cache-Control"] = "no-cache"
	self.response.headers["Set-Cookie"] = "secure; httponly;"
	self.response.headers["Pragma"] = "no-cache"
	self.response.headers["X-Permitted-Cross-Domain-Policies"] = "master-only"
	self.response.headers["Expires"] = "-1"
	return self