def text_u(body, pre, post):
	return "%s<small><span foreground=\"darkred\"><u>%s</u></span></small>%s" % (pre, body, post);

def text_norm(body, pre, post):
        return "%s<small><span foreground=\"darkred\">%s</span></small>%s" % (pre, body, post);

def add_italic(body):
	return "<i>%s</i>" % body
