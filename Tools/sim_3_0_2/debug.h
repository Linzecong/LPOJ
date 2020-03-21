/*	This file is part of the debugging module DEBUG.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: debug.h,v 1.9 2014-09-25 06:58:26 Gebruiker Exp $
*/

#ifndef	_DEBUG_H_
#define	_DEBUG_H_

/****
The module DEBUG defines one routine,

	extern void wr_info(const char *str, int val);

which, when compiled with a -DDEBUG option, writes the string str, a space
character, the value val in decimal, and a newline to standard error output
(file descriptor 2), without interfering with other program activities.

This allows debugging info to be obtained in the presence of sudden crashes
and other nefarious program activity.

Compiled without the -DDEBUG option wr_info does nothing. This allows easy
switching off of the debugging feature by recompiling debug.c.
****/

/* Public entries */
extern void wr_info(const char *s, int v);

#endif	/* _DEBUG_H_ */
