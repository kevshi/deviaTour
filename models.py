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