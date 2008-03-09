import gtk
from styler import *

class ActionLabel(gtk.EventBox):

	def __init__(self, state, pre="| ", post=" "):
		gtk.EventBox.__init__(self)
		self.pre = pre
		self.post = post
		self.label = gtk.Label()
		self.current_state = state
                self.label.set_markup(text_norm(state.state_text(), self.pre, self.post))

		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(65000, 65000, 65000))

                def enter_text_callback(widget, event):
	                widget.get_child().set_markup(text_u(self.current_state.state_text(), pre, post))
		def leave_text_callback(widget, event):
	                widget.get_child().set_markup(text_norm(self.current_state.state_text(), pre, post))
                self.connect("enter-notify-event", enter_text_callback)
		self.connect("leave-notify-event", leave_text_callback)
		self.connect("button-press-event", self.__on_button_press_event)
		self.add(self.label)

	def __on_button_press_event(self, widget, event):
		self.on_action_executed(self)
