import gtk
import logging
try:
	import gconf
	import gnomekeyring
	from config import GConfKeyringConfigProvider as ConfigProvider
except ImportError, ie:
	logging.getLogger().debug(ie.message)

class LoginDialog(gtk.Dialog):

	def __init__(self, configProvider):
		gtk.Dialog.__init__(self, _("Google Account"), None, gtk.DIALOG_MODAL, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		self.configProvider = configProvider		

                self.userEntry = gtk.Entry()
                self.passEntry = gtk.Entry()
                self.passEntry.set_visibility(False)
                loginTable = gtk.Table(2, 2)
                loginTable.attach(gtk.Label(_("Username:")), 0, 1, 0, 1)
                loginTable.attach(gtk.Label(_("Password:")), 0, 1, 1, 2)
                loginTable.attach(self.userEntry, 1, 2, 0, 1)
                loginTable.attach(self.passEntry, 1, 2, 1, 2)

		self.remember_me = gtk.CheckButton(_("Remember me"))
	        self.vbox.pack_start(loginTable)
		self.vbox.pack_start(self.remember_me)

		if self.configProvider.has_saved_data():
			password = self.configProvider.get_password()
			username = self.configProvider.get_username()
			if password != None:
				self.passEntry.set_text(password)
			if username != None:
				self.userEntry.set_text(username)
			self.remember_me.set_active(True)

	def run(self):
		response = gtk.Dialog.run(self)
		if response == gtk.RESPONSE_ACCEPT:
			if self.remember_me.get_active():
				self.configProvider.remember_me()
				self.configProvider.set_username(self.userEntry.get_text())
				self.configProvider.set_password(self.passEntry.get_text())
			else:
				self.configProvider.forget_me()
			return self.userEntry.get_text(), self.passEntry.get_text()
		else:
			return None


class LoginManager:

	def __init__(self, facade):
		self.facade = facade
		self.logged_in = False
		self.configProvider = ConfigProvider()
		self.facade.connect("logged-in", self.__on_logged_in)
		self.facade.connect("login-error", self.__on_login_error)
	
	def login(self):
		"""Log in user fetching it information from whetever it can. It returns True if the login process has started and False if cancel"""

		loginData = self.configProvider.get_login_data()
		if loginData == None :
			return self.new_login()
		else:
			self.__login(loginData)
			return True

	def new_login(self):
	        dialog = LoginDialog(self.configProvider)
        	dialog.show_all()
                loginData= dialog.run()
	        dialog.destroy()
		if loginData == None:
			print "no loguear"
			return False
		else:
			self.__login(loginData)
			return True
		
	def logout(self):
		self.logged_in = False

	def __login(self, login_data):
		self.username = login_data[0]
		self.facade.login(login_data[0], login_data[1])
	
	def __on_logged_in(self, facade):
		self.logged_in = True
		self.on_logged_in()
	
	def __on_login_error(self, facade, message):
		self.on_login_error()
