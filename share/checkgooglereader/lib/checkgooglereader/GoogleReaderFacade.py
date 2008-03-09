import gobject
import threading
import time
import logging
from checkgooglereader import VERSION
from GoogleReader import GoogleReader
from GoogleReader import CONST

class GoogleReaderFacade(gobject.GObject):
	"""Google Reader Facade that wraps all calls to GoogleReader API in an asynchronous way"""
	__gsignals__ = {
			'logged-in': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
			'login-error': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
			'new-elements': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_INT, )),
			'elements-fetched': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))
			}

	def __init__(self):
		gobject.GObject.__init__(self)
		self.reader = GoogleReader(agent="pyrfeed-googlereader-api:googlereadernotifier/%s" % VERSION)
		self.cache_pool = {}
		self.has_unread_elements = False

	def login(self, username, password):
		logging.getLogger().debug("username: %s | password: %s" % (username, "*"*len(password)))
		self.reader.identify(username, password)
		def login_run():
			if not self.reader.login():
				gobject.GObject.emit(self, "login-error")
				return
			gobject.GObject.emit(self, "logged-in")
		login_thread = threading.Thread(name="Login thread")
		login_thread.run = login_run
		login_thread.start()

	def check_unread_elements(self, tags=None):
		"""checks for unreaded elements in the specified tags, setting the has_unread_elements property"""
		def check_unread_elements_run():
			unread_elements_size = 0
			subscriptions, self.subscriptions_names = self.__get_subscriptions_dic()
			for label in self.reader.get_unread_count_list()["unreadcounts"]:
				if label["id"].startswith("feed"):
					if tags == None or self.__has_common_elements(tags, subscriptions[label["id"]]):
						unread_elements_size += label["count"]
			self.has_unread_elements = unread_elements_size > 0
			gobject.GObject.emit(self, "new-elements", unread_elements_size)
		check_thread= threading.Thread(name="Unread elements thread")
		check_thread.run = check_unread_elements_run
		check_thread.start()
	
	def __has_common_elements(self, list1, list2):
		for elem in list1:
			if elem in list2:
				return True
		return False

	def __get_subscriptions_dic(self):
		subscription_label = {}
		subscription_name = {}
		subscriptions = self.reader.get_subscription_list()["subscriptions"]
		for subscription in subscriptions:
			for category in subscription["categories"]:
				if subscription_label.has_key(subscription["id"]):
					subscription_label[subscription["id"]].append(category["label"])
				else:
					subscription_label[subscription["id"]] = [(category["label"])]
			subscription_name[subscription["id"]] = subscription["title"]
		return subscription_label, subscription_name

	def fetch_elements(self, fetch_size, tags=[None]):
		def fetch_elements_run():
			next_elements = []
			for tag in tags:
				try:
					cache = self.cache_pool[tag]
				except KeyError:
					self.cache_pool[tag] = GoogleReaderCache(self.reader, tag)
					cache = self.cache_pool[tag]
				cached_list = cache.get_next(fetch_size - len(next_elements))
				duplicated_elements_count = count_duplicated_elements(next_elements, cached_list)
				while duplicated_elements_count != 0:
					cache.remove_from_cache(next_elements)
					cached_list = cache.get_next(duplicated_elements_count)
					duplicated_elements_count = count_duplicated_elements(next_elements, cached_list)
				next_elements.extend(cached_list)
				if len(next_elements) >= fetch_size:
					break
			gobject.GObject.emit(self, "elements-fetched", next_elements)
		fetch_thread = threading.Thread(name="Fetch thread")
		fetch_thread.run = fetch_elements_run
		fetch_thread.start()

	def get_subscriptions_names(self):
		self.subscriptions_names

class GoogleReaderCache:

	def __init__(self, reader, tag=None):
		self.reader = reader
		self.tag = tag
		self.cache = []
		self.max_fetch_size = 0
		self.last_cache_index = 0
		self.continuation_token = None
		self.refreshing = False
	
	def has_previous(self):
		return False

	def get_previous(self, fetch_size):
		return []

	def get_next(self, fetch_size):
		if fetch_size > self.max_fetch_size:
			logging.getLogger().debug("Growing %s cache from %d to %d", self.tag, self.max_fetch_size*5, fetch_size*5)
			self.max_fetch_size = fetch_size
			self.cache = self.__fetch_query(fetch_size*5)
		result = self.cache[:fetch_size]
		if (len(result) < fetch_size) and self.refreshing:
			logging.getLogger().debug("waiting for %s cache is refresh", self.tag)
			while self.refreshing:
				time.sleep(1)
			result.extend(self.cache[fetch_size-len(result):])

		self.cache = self.cache[len(result):]

		#this has to be done because threads cannot be restarted >_<
		def cache_extend_run():
			self.refreshing = True
			self.cache.extend(self.__fetch_query(len(result)))
			self.refreshing = False
		cache_fetch_thread = threading.Thread(name=self.tag)
		cache_fetch_thread.run = cache_extend_run
		cache_fetch_thread.start()
		logging.getLogger().debug("fetched %d elements for tag %s" % (len(result), self.tag))
		return result
		
	def remove_from_cache(self, exclude):

		def on_dupe_element(dupe_element):
			self.cache.remove(dupe_element)
		excluded_count = count_duplicated_elements(self.cache, exclude, on_dupe_element)
		if excluded_count > 0:
			logging.getLogger().debug("Removing %d elements from %s cache" % (excluded_count, self.tag))
			extended_elements = self.__fetch_query(excluded_count)
			self.cache.extend(extended_elements)

	def __fetch_query(self, size):
		out = []
		if self.continuation_token == None:
			logging.getLogger().debug("Fetching %d elements for tag %s", size, self.tag)
			feed_iterator = self.reader.get_feed(feed=CONST.ATOM_PREFIXE_LABEL + (self.tag if self.tag != None else ""), exclude_target = CONST.ATOM_STATE_READ, count = size) 
		else:
			logging.getLogger().debug("Fetching %d elements for tag %s using continuation token = %s", size, self.tag, self.continuation_token)
			feed_iterator = self.reader.get_feed(feed=CONST.ATOM_PREFIXE_LABEL + (self.tag if self.tag != None else ""), exclude_target = CONST.ATOM_STATE_READ, count = size, continuation= self.continuation_token)
		if feed_iterator == None:
			logging.getLogger().error("An unespected error has ocurred fetching %d elements from %d cache using %s continuation token", size, self.tag, self.continuation_token)
			return out

		for entry in feed_iterator.get_entries():
			out.append(entry)
		self.continuation_token = feed_iterator.get_continuation()
		return out

def count_duplicated_elements(list1, list2, action=None):
	"""count elements that has the same google_id and you can make some action when a duplicated element is found"""
	dupe_count = 0
	list1_id_list = map(lambda e: e["google_id"], list1)
	for element in list2:
		if element["google_id"] in list1_id_list:
			dupe_count += 1
			if (action != None):
				action(element)
	return dupe_count
