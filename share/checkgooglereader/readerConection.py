import sys
from os.path import dirname, join
sys.path.insert(0, join(dirname(__file__), 'lib'))
from lib.GoogleReader import GoogleReader
from lib.GoogleReader.const import CONST
version = 0.1

class GoogleReaderConnection:

	def __init__(self):
		self._reader = GoogleReader(agent='pyrfeed-framework-contact:googlereadernotifier/%s' % version)

	def connect(self, username, password):
		self._reader.identify(username, password)
		self._reader.login()
	
	def print_unread_titles(self):
		deletable_entry = self._reader.get_feed(feed=CONST.ATOM_PREFIXE_LABEL+"deletable", exclude_target=CONST.ATOM_STATE_READ, count=3)
		deletable_list = deletable_entry.get_entries()
		count = 0
		print "="*20+"deletable"
		for elem in deletable_list:
			print elem["title"]
			count += 1
		deletable_cont = deletable_entry.get_continuation()
		noticias_entry = self._reader.get_feed(feed=CONST.ATOM_PREFIXE_LABEL+"noticias", exclude_target=CONST.ATOM_STATE_READ, count=3)
		noticias_list = noticias_entry.get_entries()
		print "="*20+"noticias"
		for elem in noticias_list:
			print elem["title"]
			count += 1
		noticias_cont = noticias_entry.get_continuation()
		deletable_entry = self._reader.get_feed(feed=CONST.ATOM_PREFIXE_LABEL+"deletable", exclude_target=CONST.ATOM_STATE_READ, count=3, continuation=deletable_cont)
		deletable_list = deletable_entry.get_entries()
		print "="*20+"deletable"
		print "continuation token %s" % deletable_cont
		for elem in deletable_list:
			print elem["title"]
			count += 1
		noticias_entry = self._reader.get_feed(feed=CONST.ATOM_PREFIXE_LABEL+"deletable", exclude_target=CONST.ATOM_STATE_READ, count=3, continuation=noticias_cont)
		noticias_list = noticias_entry.get_entries()
		print "="*20+"noticias"
		print "noticias token %s" % deletable_cont
		for elem in noticias_list:
			print elem["title"]
			count += 1


def main():
	connection = GoogleReaderConnection()
	connection.connect("dieguitoll@gmail.com", "cvzqpf4g")
	connection.print_unread_titles()

if __name__ == "__main__":
	main()
