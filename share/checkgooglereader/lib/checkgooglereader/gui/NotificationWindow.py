import gtk
import re
import logging
from NotificationItem import NotificationItem
from styler import *

class NotificationWindow(gtk.Window):

	def __init__(self):
		gtk.Window.__init__(self, gtk.WINDOW_POPUP)
		self.processor = ElementProcessor()
		self.current_entries = []
		
		notifybox_b = gtk.EventBox()
		notifybox_b.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0, 0,))
		gtk.Window.add(self, notifybox_b)

		notify_vbox_b = gtk.VBox(0, 0)
		notify_vbox_b.set_border_width(1)
		notifybox_b.add(notify_vbox_b)

		notifybox = gtk.EventBox()
		notifybox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(65000, 65000, 65000))
		notify_vbox_b.pack_start(notifybox, 0, 0, 0)

		self.notify_vbox = gtk.VBox(0, 0)
		self.notify_vbox.set_border_width(4)
		notifybox.add(self.notify_vbox)

		status_hbox = gtk.HBox(0,0)
		self.notify_vbox.pack_start(status_hbox, 0, 0, 0)

		self.status_label = gtk.Label()
		self.set_unread_elements_count(0)
		status_hbox.pack_start(self.status_label, 0, 0, 0)

		mark_all_text = _("Mark all this as read")
		mark_all_label = gtk.Label()
		mark_all_label.set_markup(text_norm(mark_all_text, "", ""))

		mark_all_ebox = gtk.EventBox()
		mark_all_ebox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(65000, 65000, 65000))
		def mark_all_enter(widget, event):
			mark_all_label.set_markup(text_u(mark_all_text, "", ""))
		mark_all_ebox.connect("enter-notify-event", mark_all_enter)
		def mark_all_leave(widget, event):
			mark_all_label.set_markup(text_norm(mark_all_text, "", ""))
		mark_all_ebox.connect("leave-notify-event", mark_all_leave)
		mark_all_ebox.add(mark_all_label)

		status_hbox.pack_end(mark_all_ebox, 0, 0, 0)

		spacer = gtk.Label()
		spacer.set_markup("<small></small>")
		self.notify_vbox.pack_start(spacer, 0, 0, 0)
		
		gtk.Window.connect(self, "leave-notify-event", self.__on_leave_event)
		gtk.Window.connect(self, "enter-notify-event", self.__on_enter_event)

	def set_unread_elements_count(self, count):
		self.status_label.set_markup("<span foreground=\"#000000\"><small><span foreground=\"#000000\">%s</span></small></span>" % (_n("There is %d new feed ...", "There are %d new feeds ...", count) % count))

	def add_elements(self, elements, preprocessor=None):
		self.current_entries = elements
		for element in elements:
			self.add_element(self.processor.process(element))
			carry_return = gtk.Label()
			carry_return.set_markup("<small></small>")
			self.notify_vbox.pack_start(carry_return, 0, 0, 0)

	def add_element(self, element):
		self.notify_vbox.pack_start(NotificationItem(element))

	def set_feedname_resolver(self, labels):
		self.processor.label_resolver = labels

        def __on_leave_event(self, widget, event):
		gtk.Window.hide(self)

	def __on_enter_event(self, widget, event):
		self.on_enter_event(self, event)

class ElementProcessor:
	def __init__(self):
		self.label_resolver = None

	def process(self, element):
		element["labels"] = self.get_labels(element)
		element["summary"] = self.get_summary(element)
		element["subscription"] = self.get_subscription(element)
		element["shared"] = self.is_shared(element)
		element["starred"] = self.is_starred(element)
		return element

	def get_labels(self, element):
	        out = ""
	        for category in element["categories"].keys():
		        if not category.startswith("user/-/state/com.google/"):
			        out += element["categories"][category]
			        out += ", "
		return out[:len(out)-2]

	def get_summary(self, element):
                processed_text = re.sub("<(.|\n)+?>", "", element["summary"].replace("<br>","\n")).strip()
                return processed_text[:400] + ("..." if len(processed_text)>400 else "")

	def get_subscription(self, element):
		if self.label_resolver != None:
			return self.label_resolver[element["sources"].keys()[0]]
		return "fetching feed name..." 

	def is_shared(self, element):
		return "user/-/state/com.google/broadcast" in element["categories"].keys()

	def is_starred(self, element):
		return "user/-/state/com.google/starred" in element["categories"].keys()
