Checkgooglereader is based in the GUI and user experience aquired using checkgmail (http://checkgmail.sourceforge.net).

It's my first 'real' project using python+gtk+gobject and try to be done using good POO practices (of course I'm open to suggestions in this field)

Features:
  * set label/s to check
  * preview feeds
  * manage each element from the compact GUI (read/unread, star/unstar, share/unshre, mark as read)
  * navigate through your unread elements (forward only, we're working in backward :P)

Depends:
  * python 2.5
ATM the configuration and password storage is managed using...
  * python-gconf
  * python-gnomekeyring
...but this is totally extensible