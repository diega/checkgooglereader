from egg.trayicon import TrayIcon as eggTrayIcon
from checkgooglereader import RESOURCE_PATH
import gtk
import os

skin = "default"
skins_folder= "skins"

class TrayIcon(eggTrayIcon):

	def __init__(self):
		eggTrayIcon.__init__(self, "googlereadernotifier")
                eventbox = gtk.EventBox()
		tray_hbox = gtk.HBox(0,0)
		tray_hbox.set_border_width(2)
		eventbox.add(tray_hbox)
		self.icon = gtk.Image()
		self.set_all_read_status()
		tray_hbox.pack_start(self.icon, False, False, padding = 0)

		eggTrayIcon.add(self, eventbox)
		eventbox.connect("enter-notify-event", self.__on_enter_event)
		eventbox.connect("leave-notify-event", self.__on_leave_event)
		eventbox.connect("button-press-event", self.__on_button_event)
		
		self.tooltip_status = ""
		self.props.has_tooltip = True
		eggTrayIcon.connect(self, "query-tooltip", self.__query_tooltip_callback)

	def set_unread_status(self):
		self.icon.set_from_file(os.path.join(RESOURCE_PATH, skins_folder, skin, "new.png"))
	
	def set_all_read_status(self):
		self.icon.set_from_file(os.path.join(RESOURCE_PATH, skins_folder, skin, "none.png"))

	def __query_tooltip_callback(self, widget, x, y, keyboard_mode, tooltip):
		tooltip.set_text(self.tooltip_status)
		return self.show_tooltip()
	
	def __on_button_event(self, widget, event):
		self.on_button_event(self, event)

	def __on_enter_event(self, widget, event):
		self.on_enter_event(self, event)

	def __on_leave_event(self, widget, event):
		self.on_leave_event(self, event)

	def on_button_event(self, widget, event):
		pass

	def on_enter_event(self, widget, event):
		pass

	def on_leave_event(self, widget, event):
		pass
