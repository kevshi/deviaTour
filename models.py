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
from google.appengine.ext import ndb
from webapp2_extras import security
import webapp2_extras.appengine.auth.models
import webapp2_extras.appengine.sessions_ndb

class Newsletterinvite(ndb.Model):
	token = ndb.StringProperty()
	email = ndb.StringProperty()
	done = ndb.BooleanProperty(default=False)
	created = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def create(cls, email, done=False):
		newsletterinvite = cls(token=security.generate_password_hash(password=email, length=12),  # better than random string because of smaller possibility of duplicate token
		                 		email=email,
		                 		done=done)
		newsletterinvite.put()
		return newsletterinvite.token

	@classmethod
	def validate_token(cls,token):
		entry = cls.query(cls.token == token).get()
		if entry:
			entry.done = True
			entry.put()
		return cls.query(cls.token == token).get()

class Session(webapp2_extras.appengine.sessions_ndb.Session):
	user_id = ndb.IntegerProperty()

	@classmethod
	def get_by_sid(cls, sid):
		"""Returns a ``Session`` instance by session id.

		:param sid:
			A session id.
		:returns:
			An existing ``Session`` entity.
		"""
		data = memcache.get(sid)
		if not data:
			session = ndb.model.Key(cls, sid).get()
			if session:
				data = session.data
				memcache.set(sid, data)

		return data

	@classmethod
	def delete_by_user_id(cls, self, user_id):
		"""Returns a ``Session`` instance by session id.

		:param sid:
			A session id.
		:returns:
			An existing ``Session`` entity.
		"""
		usersessions = Session.query(Session.user_id == int(user_id)).fetch()
		logging.info(usersessions)
		for session in usersessions:
			sid = session._key.id()
			logging.info(sid)
			data = Session.get_by_sid(sid)
			logging.info(data)
			sessiondict = sessions.SessionDict(self, data=data)
			sessiondict['_user'] = None
			sessiondict['user_id'] = None
			sessiondict['token'] = None
			memcache.set(sid, '')
			ndb.model.Key(Session, sid).delete()
		usersessions = Session.query(Session.user_id == int(user_id)).fetch()
		logging.info(usersessions)
		return usersessions

class DataStoreSessionFactorExtended (webapp2_extras.appengine.sessions_ndb.DatastoreSessionFactory):
	"""A session factory that stores data serialized in datastore.

	To use datastore sessions, pass this class as the `factory` keyword to
	:meth:`webapp2_extras.sessions.SessionStore.get_session`::

	from webapp2_extras import sessions_ndb

	# [...]

	session = self.session_store.get_session(
		name='db_session', factory=sessions_ndb.DatastoreSessionFactory)

	See in :meth:`webapp2_extras.sessions.SessionStore` an example of how to
	make sessions available in a :class:`webapp2.RequestHandler`.
	"""

	#: The session model class.
	session_model = Session

	def _get_by_sid(self, sid):
		"""Returns a session given a session id."""
		if self._is_valid_sid(sid):
			data = self.session_model.get_by_sid(sid)
			if data is not None:
				self.sid = sid
				logging.info(sid)
				logging.info(sessions.SessionDict(self, data=data))
				return sessions.SessionDict(self, data=data)
		logging.info('new')
		self.sid = self._get_new_sid()
		return sessions.SessionDict(self, new=True)

	def save_session(self, response):
		if self.session is None or not self.session.modified:
			return
		#logging.info(self.session['user_id'])
		logging.info(self.session)
		logging.info(self.sid)
		if self.session:
			try:
				try:
					logging.info(self.session['user_pre_2FA'])
					userid = self.session['user_pre_2FA']['user_id']
				except:
					userid = self.session['_user'][0]
				logging.info('new session with user_id: '+str(self.sid))
				self.session_model(id=self.sid, data=dict(self.session), user_id = userid)._put()
			except:
				logging.info('new session no user_id: '+str(self.sid))
				self.session_model(id=self.sid, data=dict(self.session))._put()
		else:
			logging.info('new session no user_id: '+str(self.sid))
			self.session_model(id=self.sid, data=dict(self.session))._put()
		self.session_store.save_secure_cookie(
			response, self.name, {'_sid': self.sid}, **self.session_args)