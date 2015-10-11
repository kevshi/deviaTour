import jinja2, datetime
import webapp2, uuid, time, logging, urllib, base64, os
import requests
# from google.appengine.ext.webapp import template
# from google.appengine.api import urlfetch
# from google.appengine.api import mail, app_identity
# from google.appengine.api import memcache
# from googleplaces import GooglePlaces, types, lang, ranking

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

# API_KEY = 'AIzaSyBFbiJfl5b3SJPCJJnQ3ugCnG8MbCE9aiY'
# google_places = GooglePlaces(API_KEY)

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

# class AboutHandler(BaseHandler):
# 	def get(self):
# 		params = {}
# 		self.render_template('templates/about.html', params)

# class ProductHandler(BaseHandler):
# 	def get(self):
# 		params = {}
# 		self.render_template('templates/product.html', params)

# class PlaceHandler(BaseHandler):
# 	def get(self):
# 		place_id = self.request.GET['id']
# 		place = google_places.get_place(place_id)
# 		place.get_details()
# 		photos = []
# 		for photo in reversed(place.photos):
# 			photos.append("https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&key=" + API_KEY + "&photoreference=" + photo.photo_reference)
# 		hours = []
# 		for day in range(7):
# 			try:
# 			  open = place.opening_hours.periods[day].open.time
# 			except:
# 			  open='No work time';
# 			hours.append(open)
# 		params = {'place': place, 'photos': photos, 'hours': hours}
# 		self.render_template('templates/place.html', params)

# class ResultsHandler(BaseHandler):
# 	def post(self):
# 		self = addResponseHeaders(self)
# 		location = self.request.get('location')
# 		query = self.request.get('query')
# 		query_result = google_places.nearby_search(
#         location=location, keyword=query,
#         radius=50000, types=[types.TYPE_FOOD], rankby=ranking.DISTANCE)
# 		for place in query_result.places:
# 			place.get_details()
# 		params = {"places": query_result.places, "location": location, "query": query}
# 		self.render_template('templates/results.html', params)

# class ContactFormHandler(BaseHandler):
# 	def post(self):

# 		self = addResponseHeaders(self)
# 		name = self.request.get("name")
# 		email = self.request.get("email")
# 		message = self.request.get("message")

# 		cursite = 'Fresh Eats'
# 		if name and email and message and email:
# 			message_body = """
# 				Message from the %s Contact Form.

# 				Name: %s
# 				Email: %s

# 				Message:
# 				%s

# 				----
# 				Fresh Eats
# 			""" % (cursite, name.encode('utf-8').decode('utf-8'), email, message.encode('utf-8').decode('utf-8'))

# 			html_message_body = """
# 				<p>Message from the %s Contact Form.</p>

# 				<p>Name: %s</p>
# 				<p>Email: %s</p>

# 				<p>Message:</p>
# 				<p>%s</p>

# 				<p>----</p>
# 				<p>Fresh Eats</p>
# 			""" % (cursite, name.encode('utf-8').decode('utf-8'), email, message.encode('utf-8').decode('utf-8'))


# 			if len(message_body) > 500:
# 				self.response.out.write('No more than 500 characters allowed in message body. '
# 									'Please send an email to jusliu@berkeley.edu for longer messages.')
# 				return

# 			sendThroughMailgun("jusliu@berkeley.edu",  "New Message from {0} ({1})".format(name.encode('utf-8').decode('utf-8'), email),
# 							   message_body,  html_message_body)

# 			self.response.out.write('Thank you for your message. We will reply as soon as possible.')
# 			#self.display_message("Thank you for your message. We will reply as soon as possible.")
# 		else:

# 			self.response.out.write('One or more inputted fields to Contact Form were invalid. Please try again.')
# 			#self.display_message("One or more inputted fields to Contact Form were invalid. Please try again.")



# def sendThroughMailgun(to, subject, text, html, log=True, recipienttype="user"):
# 	logging.info("i got here")
# 	logging.info(app_identity.get_application_id())
# 	logging.info(os.environ['APPLICATION_ID'])

# 	if os.environ['APPLICATION_ID'].startswith('dev'):
# 		#localhost

# 		# form_fields={"from": "Fresh Eats <jusliu@berkeley.edu>",
# 		# 	"to": to,
# 		# 	"subject": subject,
# 		# 	"text": text,
# 		# 	"html": html,
# 		# 	"o:dkim":'yes'}
# 		# str_form_fields = {}
# 		# for k, v in form_fields.iteritems():
# 		# 	str_form_fields[k] = unicode(v).encode('utf-8')
# 		# form_data = urllib.urlencode(str_form_fields)
# 		# username = "postmaster@sandbox1c65e389cd3e414ea4fef7a5e5c8700c.mailgun.org"
# 		# pw = "e0eb18e8cc5fc0d81e9f5f5c956eb678"
# 		# encoded = base64.b64encode(username + ':' + pw)
# 		# authstr = "Basic "+encoded
# 		# mheaders = {'Authorization':authstr}
# 		# return urlfetch.fetch(
# 		# 	url="https://api.mailgun.net/v3/sandbox1c65e389cd3e414ea4fef7a5e5c8700c.mailgun.org/messages",
# 		# 	payload=form_data,
# 		# 	method=urlfetch.POST,
# 		# 	headers = mheaders,
# 		# 	deadline=10)
# 		key = 'key-4a6e4caf0c3c57a8d5407ab2f32854ea'
# 		sandbox = 'sandbox1c65e389cd3e414ea4fef7a5e5c8700c.mailgun.org'
# 		request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)
# 		# request = requests.post(request_url, auth=('api', key), data={
# 		# 	'from': 'Fresh Eats <jusliu@berkeley.edu>',
# 		# 	'to': to,
# 		# 	'subject': subject,
# 		# 	'text': text })
# 		# return request

# 	elif app_identity.get_application_id() == 'places-web':
# 		message = mail.EmailMessage(sender="Fresh Eats <{0}>".format("jusliu@berkeley.edu"), to=to, subject=subject, body=text, html=html)
# 		message.send()

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