import gtk
from ActionLabel import ActionLabel
from styler import *

class NotificationItem(gtk.VBox):
	def __init__(self, entry):
		gtk.VBox.__init__(self)
		self.item = entry
		hbox_t = gtk.HBox(False, 0)
		gtk.VBox.pack_start(self, hbox_t, False, False, 0)
		title_l = gtk.Label()
		title_markup = "<span foreground=\"#000000\"><b><u>%s</u></b></span><small> <span foreground=\"#006633\">%s</span></small>\n<b>%s: </b>%s"
		title_l.set_markup(title_markup % (entry["title"], 
						   entry["labels"], 
						   _("from"), 
						   entry["subscription"]))
		title_l.set_line_wrap(1)

		title_l_ebox = gtk.EventBox()
		title_l_ebox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(65000, 65000, 65000))
		def title_enter(widget, event):
			title_l.set_markup(title_markup % (add_italic(entry["title"]), entry["labels"], _("from"), entry["subscription"]))
		title_l_ebox.connect("enter-notify-event", title_enter)
		def title_leave(widget, event):
			title_l.set_markup(title_markup % (entry["title"], entry["labels"], _("from"), entry["subscription"]))
		title_l_ebox.connect("leave-notify-event", title_leave)
		title_l_ebox.add(title_l)
		hbox_t.pack_start(title_l_ebox, False, False,0)

		hbox_opt = gtk.HBox(False, 0)
		gtk.VBox.pack_start(self, hbox_opt, False, False, 0)

		open_label = ActionLabel(OpenState(), "")
		open_label.on_action_executed = self.__open_item_action
		hbox_opt.pack_start(open_label, False, False, 0)

		mark_label = ActionLabel(MarkState())
		mark_label.on_action_executed = self.__mark_item_action
		hbox_opt.pack_start(mark_label, False, False, 0)

		if entry["starred"]:
			star_label = ActionLabel(UnstarState())
		else:
			star_label = ActionLabel(StarState())
		star_label.on_action_executed = self.__star_item_action
		hbox_opt.pack_start(star_label, False, False, 0)

		if entry["shared"]:
			share_label = ActionLabel(ShareState())
		else:
			share_label = ActionLabel(UnshareState())
		share_label.on_action_executed = self.__share_item_action
		hbox_opt.pack_start(share_label, False, False, 0)

		hbox_b = gtk.HBox()
		gtk.VBox.add(self, hbox_b)

		body_l = gtk.Label()
		body_l.set_line_wrap(1)
		body_l.set_markup("<span foreground=\"grey25\">%s</span>" % entry["summary"])
		hbox_b.pack_start(body_l, False, False, 0)

	def __mark_item_action(self, action_label):
		pass

	def __share_item_action(self, action_label):
		pass

	def __star_item_action(self, action_label):
		action_label.current_state = action_label.current_state.next_state()

	def __open_item_action(self, action_label):
		pass
	
# ====== Share/Unshare label states

class SharingStates:
	def __init__(self):
		pass

class ShareState:

	def next_state(self):
		return SharingState()

	def state_text(self):
		return _("Share")

class SharingState:

	def next_state(self):
		return UnshareState()

	def state_text(self):
		return _("Sharing...")

class UnshareState:

	def next_state(self):
		return UnsharingState()

	def state_text(self):
		return _("Unshare")

class UnsharingState:

	def next_state(self):
		return ShareState()

	def state_text(self):
		return _("Unsharing...")

# ====== star/unstar label states
class StarState:
	def next_state(self):
		return StarringState()

	def state_text(self):
		return _("Add Star")

class StarringState:
	def next_state(self):
		return UnstarState()

	def state_text(self):
		return _("Adding star...")

class UnstarState:
	def next_state(self):
		return UnstarringState()

	def state_text(self):
		return _("Remove Star")

class UnstarringState:
	def next_state(self):
		return StarState()

	def state_text(self):
		return _("Unstarring...")
# ======= Open state
class OpenState:
	def next_state(self):
		return OpenState()

	def state_text(self):
		return _("Open")

# ======= Mark as read state
class MarkState():
	def next_state(self):
		return MarkingState()

	def state_text(self):
		return _("Mark as read...")

class MarkingState():
	def next_state(self):
		return None

	def state_text(self):
		return _("Marking as read...")
