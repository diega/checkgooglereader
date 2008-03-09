from os.path import abspath, dirname, join, pardir

VERSION = '0.0.1'

# here we define the path constants so that other modules can use it.
# this allows us to get access to the shared files without having to
# know the actual location, we just use the location of the current
# file and use paths relative to that.
SHARED_FILES = abspath(join(dirname(__file__), pardir, pardir))
LOCALE_PATH = join(SHARED_FILES, 'i18n')
RESOURCE_PATH = join(SHARED_FILES, 'res')

# the name of the gettext domain. because we have our translation files
# not in a global folder this doesn't really matter, setting it to the
# application name is a good idea tough.
GETTEXT_DOMAIN = 'checkgooglereader'

# setup PyGTK by requiring GTK2
import pygtk
pygtk.require('2.0')

# set up the gettext system and locales
from gtk import glade
import gettext
import locale

locale.setlocale(locale.LC_ALL, '')
for module in glade, gettext:
	module.bindtextdomain(GETTEXT_DOMAIN, LOCALE_PATH)
	module.textdomain(GETTEXT_DOMAIN)

# register the gettext function for the whole interpreter as "_"
import __builtin__
__builtin__._ = gettext.gettext
__builtin__._n = gettext.ngettext

# import the main function
from checkgooglereader.GoogleReaderNotifier import main



