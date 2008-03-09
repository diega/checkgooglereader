import gtk
from checkgooglereader import VERSION

class ContextMenu(gtk.Menu):

	def __init__(self):
		gtk.Menu.__init__(self)
		menu_login = gtk.ImageMenuItem(_("Login..."))
		menu_login.set_image(gtk.image_new_from_stock(gtk.STOCK_HOME, gtk.ICON_SIZE_MENU))
		def menu_login_activate(menuitem):
			self.login()
		menu_login.connect("activate", menu_login_activate)

		menu_check = gtk.ImageMenuItem(_("Check feeds"))
		menu_check.set_image(gtk.image_new_from_stock(gtk.STOCK_REFRESH, gtk.ICON_SIZE_MENU))
		def menu_check_activate(menuitem):
			self.refresh()
		menu_check.connect("activate", menu_check_activate)

		menu_quit = gtk.ImageMenuItem(_("Quit"))
		menu_quit.set_image(gtk.image_new_from_stock(gtk.STOCK_QUIT, gtk.ICON_SIZE_MENU))
		def menu_quit_activate(menuitem):
			gtk.main_quit()
		menu_quit.connect("activate", menu_quit_activate)

		menu_about = gtk.ImageMenuItem(_("About"))
		menu_about.set_image(gtk.image_new_from_stock(gtk.STOCK_ABOUT, gtk.ICON_SIZE_MENU))
		def menu_about_activate(menuitem):
			dialog = gtk.AboutDialog()
			dialog.set_name('Google Reader Notifier')
			dialog.set_version(VERSION)
			dialog.set_comments('Checks you Google Reader account looking for unread elements')
			dialog.set_website('http://code.google.com/checkgooglereader')
			dialog.run()
			dialog.destroy()
		menu_about.connect("activate", menu_about_activate)

		gtk.Menu.append(self, menu_login)
		gtk.Menu.append(self, menu_check)
		gtk.Menu.append(self, menu_about)
		gtk.Menu.append(self, menu_quit)

