import gui.NotificationWindow
import gui.TrayIcon
import gui.ContextMenu
import gtk
import gobject
import sys
import logging
from GoogleReaderFacade import GoogleReaderFacade
from manager.login import LoginManager
from manager.preferences import PreferencesManager

GTK_GDK_ANY_BUTTON_MASK = gtk.gdk.BUTTON1_MASK | gtk.gdk.BUTTON2_MASK | gtk.gdk.BUTTON3_MASK | gtk.gdk.BUTTON4_MASK | gtk.gdk.BUTTON5_MASK

class GoogleReaderNotifier:
	def __init__(self, facade):
                gobject.threads_init()
		self.loginManager = LoginManager(facade)
		self.prefsManager = PreferencesManager()
		self.facade = facade

		self.win_popup = gui.NotificationWindow.NotificationWindow()
		self.win_popup.on_enter_event = self.on_win_popup_enter_notify
		self.win_popup.hide()

		self.menu = gui.ContextMenu.ContextMenu()
		self.menu.login = self.loginManager.new_login
		self.menu.refresh = self.check_new_elements
		self.menu.show_all()
		
		self.trayicon = gui.TrayIcon.TrayIcon()
		self.trayicon.on_button_event = self.on_trayicon_button_press
		self.trayicon.tooltip_status = _("Please Log In")
		def show_tooltip():
			return not self.loginManager.logged_in or not self.facade.has_unread_elements
		self.trayicon.show_tooltip = show_tooltip
		self.trayicon.show_all()

		facade.connect("new-elements", self.on_new_elements_checked)
		facade.connect("elements-fetched", self.on_elements_fetched)

	def on_trayicon_button_press(self, widget, event):
		self.win_popup.hide() 
		if event.button == 1:
			print "abrir firefox"
		else:
			self.menu.popup(None, None, None, event.button, event.time)

	def on_trayicon_enter_notify(self, widget, event):
		if event.get_state() & GTK_GDK_ANY_BUTTON_MASK or self.menu.props.visible:
			return
		def show_win_popup():
			move_x, move_y = self.get_popup_location(widget, self.win_popup)
			self.win_popup.move(move_x, move_y)
			self.win_popup.show_all()
			return False
		self.show_win_popup_event = gobject.timeout_add(250, show_win_popup)

	def on_trayicon_leave_notify(self, widget, event):
		if event.get_state() & GTK_GDK_ANY_BUTTON_MASK or self.menu.props.visible:
			return
		if self.win_popup.props.visible:
			def hide_win_popup():
				self.win_popup.hide()
			self.hide_win_popup_event = gobject.timeout_add(100, hide_win_popup)
		else:
			gobject.source_remove(self.show_win_popup_event)
	
	def on_win_popup_enter_notify(self, widget, event):
		gobject.source_remove(self.hide_win_popup_event)

	def get_popup_location(self, widget, win_popup):
		boxx, boxy = widget.window.get_origin()
		icon_height = widget.allocation.height
		monitor, rect, width, height = self.get_screen_parameters(widget, boxx, boxy)

		notify_width = win_popup.allocation.width
		notify_height = win_popup.allocation.height

		x_border = 4
		y_border = 5
		move_x = width - notify_width - x_border if boxx + notify_width + x_border > width else boxx
		move_y = boxy - notify_height - y_border if boxy > height / 2 else boxy + icon_height + y_border

		return move_x, move_y

	def get_screen_parameters(self, widget, boxx, boxy):
	        monitor = widget.get_screen().get_monitor_at_point(boxx, boxy)
	        rect = widget.get_screen().get_monitor_geometry(monitor)
	        height = rect.height
	        width = 0;
	        for i in range(monitor+1):
	                width += widget.get_screen().get_monitor_geometry(i).width
	        return monitor, rect, width, height

	def login(self):
		self.loginManager.on_logged_in = self.on_login
		self.loginManager.on_login_error = self.on_login_error
		if self.loginManager.login():
			self.trayicon.tooltip_status = _("Logging in...")

	def check_new_elements(self):
		self.trayicon.tooltip_status = _("Checking for new elements")
		self.facade.check_unread_elements(self.prefsManager.managed_tags)

	def on_login(self):
		logging.getLogger().info("Logged in: %s" % self.loginManager.username)
		self.check_new_elements()

	def on_new_elements_checked(self, facade, new_elements_size):
		if new_elements_size == 0:
			import time
			self.trayicon.set_all_read_status()
			self.trayicon.tooltip_status = _("No new feeds (%s)") % time.ctime()
		else:
			logging.getLogger().info("There are %d unread elements" % new_elements_size)
			self.trayicon.tooltip_status = _("Fetching elements...")
			self.win_popup.set_unread_elements_count(new_elements_size)
			self.win_popup.set_feedname_resolver(self.facade.subscriptions_names)
			self.facade.fetch_elements(self.prefsManager.fetch_size, self.prefsManager.managed_tags) 

	def on_elements_fetched(self, facade, fetched_elements):
		logging.getLogger().info("fetched %d elements" % len(fetched_elements))
		self.win_popup.add_elements(fetched_elements)
		self.trayicon.on_enter_event = self.on_trayicon_enter_notify
		self.trayicon.on_leave_event = self.on_trayicon_leave_notify
		self.trayicon.set_unread_status()


	def on_login_error(self):
		logging.getLogger.info("Login error")
		self.trayicon.tooltip_status = _("Login error")
		self.loginManger.new_login()

	def on_subscription_list_ready(self, facade, subscriptions):
		self.win_popup.set_label_resolver(subscriptions)


def main():
	try:
		facade = GoogleReaderFacade()
		notifier = GoogleReaderNotifier(facade)
		notifier.login()
		gtk.main()
	except:
		sys.exit(0)
