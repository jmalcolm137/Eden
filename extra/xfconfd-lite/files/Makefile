PREFIX ?= /usr
CC ?= cc
PKG_CONFIG ?= pkg-config
CFLAGS ?= -O2

all: xfconfd-lite

xfconfd-lite: main.c xbg.c xbg.h
	$(CC) $(CFLAGS) -o $@ main.c xbg.c $(shell $(PKG_CONFIG) --cflags --libs gio-2.0 gio-unix-2.0) $(LDFLAGS)

install:
	install -Dm755 xfconfd-lite $(DESTDIR)$(PREFIX)/lib/xfce4/xfconf/xfconfd
	install -Dm644 org.xfce.Xfconf.service $(DESTDIR)$(PREFIX)/share/dbus-1/services/org.xfce.Xfconf.service

clean:
	rm -f xfconfd-lite
