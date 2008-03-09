import gconf
import gnomekeyring

class GConfKeyringConfigProvider:
	def has_saved_data(self):
		return gconf.client_get_default().get_bool("/apps/checkgooglereader/remember")

	def remember_me(self):
		return gconf.client_get_default().set_bool("/apps/checkgooglereader/remember", True)

	def forget_me(self):
		gconf.client_get_default().unset("/apps/checkgooglereader/remember")
		gconf.client_get_default().unset("/apps/checkgooglereader/username")
		gconf.client_get_default().unset("/apps/checkgooglereader/auth-key")

	def get_password(self):
		try: gnomekeyring.create_sync("login", None)
		except: pass
		auth_token = gconf.client_get_default().get_int("/apps/checkgooglereader/auth-key")
		if auth_token:
			return gnomekeyring.item_get_info_sync("login", auth_token).get_secret()
		return None		

	def get_username(self):
		return gconf.client_get_default().get_string("/apps/checkgooglereader/username")

	def set_username(self, username):
		gconf.client_get_default().set_string("/apps/checkgooglereader/username", username)

	def set_password(self, password):
		try: gnomekeyring.create_sync("login", None)
		except: pass
		auth_token = gnomekeyring.item_create_sync("login", gnomekeyring.ITEM_GENERIC_SECRET, "checkgooglereader pass", dict(appname="checkgooglereader"), password, True)
		gconf.client_get_default().set_int("/apps/checkgooglereader/auth-key", auth_token)

	def get_login_data(self):
		if self.has_saved_data():
			return self.get_username(), self.get_password()
		return None
