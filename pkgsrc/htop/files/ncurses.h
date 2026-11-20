/* compatibility shim: netbsd-curses provides curses.h, not ncurses.h.
 * htop's unicode detection only looks for ncurses*-style headers, so this
 * makes the wide netbsd-curses API visible to its configure script. */
#include <curses.h>
