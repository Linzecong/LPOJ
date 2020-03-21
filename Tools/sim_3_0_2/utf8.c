/*	This file is part of the auxiliaries library.
	Written by Dick Grune, dick@dickgrune.com
	$Id: utf8.c,v 1.13 2017-12-14 15:39:22 Gebruiker Exp $
*/

#include	<stdio.h>
#include	<stdlib.h>

#include	"utf8.h"

/* Library utf8 source prelude */
#undef	_UTF8_CODE_
#ifndef	lint
#define	_UTF8_CODE_
#endif
#ifdef	LIB
#define	_UTF8_CODE_
#endif

#ifdef	_UTF8_CODE_

/* Library utf8 source code */

/* Although Unicode is usually given in hexadecimal, UTF-8 is easier
   understood in octal: UTF-8 has 2 mark bit + 6 data bits to a byte,
   octal has 2 data bits + 3 data bits + 3 data bits to a byte.
   So we get: 03XX is a leading byte, 02xx is a continuation byte,
   and 00xx and 01xx are ASCII characters.
*/
#define	BYTE_MASK		(0377)
#define	MARK_MASK		(0300)
#define	CONTINUATION_BYTE_MARK	(0200)
#define	CONTINUATION_BYTE_VALUE	(0077)

void
clear_utf8_box(utf8_box *u) {
	u->_pos = 0;
	u->_saved_pending = 0;
}

/* All returns to the user must either return 0 or go through
   finished_sequence() or process_first_byte().
*/
static int
finished_sequence(utf8_box *u, int len) {
	/* prepares the finished utf8_box for being passed to the user and then
	   returns the length of the recognized UTF-8 sequence, correct or not
	*/
	/* Note: since len may be  u->_pos, this routine uses the call-by-value
	   mechanism in a sneaky way.
	*/
	if (u->text[0] == '\0') {
		/* we implement Modified UTF-8, in which the NULL byte is not
		   a valid UTF-8 encoding
		 */
		len = -1;
	}
	u->_pos = 0;
	return len;
}

static int
process_first_byte(utf8_box *u, int byte) {
	/* processes the first byte of a UTF-8 sequence or a single ASCII char;
	   returns +1: done, OK; 0: wait for more; -1 done, not OK
	*/
	u->_pos = 0; u->text[u->_pos++] = byte; u->text[u->_pos] = '\0';

	/* it must either be an ASCII char or a good leading UTF-8 byte */
	switch (byte & MARK_MASK) {
	case 0000: case 0100:
		/* ASCII: we are done */
		u->_size = 1;
		u->codepoint = byte;	/* no sign extension for ASCII */
		return finished_sequence(u, 1);

	case 0300:
		/* leading byte: if it is correct we return 0 */
		switch (byte & BYTE_MASK) {
		case 0300: case 0301: case 0302: case 0303:
		case 0304: case 0305: case 0306: case 0307:
		case 0310: case 0311: case 0312: case 0313:
		case 0314: case 0315: case 0316: case 0317:
		case 0320: case 0321: case 0322: case 0323:
		case 0324: case 0325: case 0326: case 0327:
		case 0330: case 0331: case 0332: case 0333:
		case 0334: case 0335: case 0336: case 0337:
			u->_size = 2;
			u->codepoint = byte & 0077;
			return 0;

		case 0340: case 0341: case 0342: case 0343:
		case 0344: case 0345: case 0346: case 0347:
		case 0350: case 0351: case 0352: case 0353:
		case 0354: case 0355: case 0356: case 0357:
			u->_size = 3;
			u->codepoint = byte & 0037;
			return 0;

		case 0360: case 0361: case 0362: case 0363:
		case 0364: case 0365: case 0366: case 0367:
			u->_size = 4;
			u->codepoint = byte & 0017;
			return 0;


		case 0370: case 0371: case 0372: case 0373:
			u->_size = 5;
			u->codepoint = byte & 0007;
			return 0;

		case 0374: case 0375:
			u->_size = 6;
			u->codepoint = byte & 0003;
			return 0;
		}
	default:
		/* a drop-out; it is either a continuation byte or
		   a bad leading byte; either way we return it as garbage
		*/
		return finished_sequence(u, -1);
	}
}

int
box_utf8(char ch, utf8_box *u) {
	int byte = ch & BYTE_MASK;

	/* is there a byte left over from last time? */
	if (u->_saved_pending) {
		/* there seems to be a left-over byte but ... */
		if (u->_pos != 0) {
			/* that can't be; conclusion: uninitialized utf8_box */
			clear_utf8_box(u);
		} else {
			/* the saved byte is genuine */
			/* retrieve it from _saved to text */
			int b =  u->_saved; u->_saved_pending = 0;
			/* box it */
			int len = box_utf8(b, u);
			if (len != 0) {
				/* the box is done; save the incoming byte */
				u->_saved = byte; u->_saved_pending = 1;
				/* and return to user */
				return finished_sequence(u, len);
			} else {
				/* there is more room in the box; continue */
			}
		}
	}

	if (u->_pos == 0) {
		/* the box is still empty, so this is the first byte */
		return process_first_byte(u, byte);
	}

	/* there is already a part of an UTF8 sequence present, so we need
	   a continuation byte
	*/
	switch (byte & MARK_MASK) {
	case CONTINUATION_BYTE_MARK:
		/* a good continuation byte; incorporate it */
		u->text[u->_pos++] = byte; u->text[u->_pos] = '\0';
		u->codepoint =
			(u->codepoint << 6) | (byte & CONTINUATION_BYTE_VALUE);

		if (u->_pos == u->_size) {
			/* full UTF8 sequence seen */
			return finished_sequence(u, u->_size);
		} else {
			/* sequence still incomplete; wait for more */
			return 0;
		}

	default:
		/* not a continuation byte, so the box cannot be completed;
		   we save the byte
		*/
		u->_saved = byte; u->_saved_pending = 1;
		/* and return the box as garbage */
		return finished_sequence(u, -u->_pos);
	}
}

int
is_valid_utf8(utf8_box *u) {
	if (u->_pos != 0) return 0;	/* unfinished box */
	/* since we have the code point, this is easy */
	int cp = u->codepoint;
	int sz = u->_size;
	if (cp == 0) return sz == 2; 	/* modified UTF-8 exception */
	if (cp < 0200) return sz == 1;
	if (cp < 04000) return sz == 2;
	if (cp < 0154000) return sz == 3;
	if (cp < 0160000) return 0;	/* UTF-16 surrogate halves (2048) */
	if (cp < 0200000) return sz == 3;
	if (cp < 04200000) return sz == 4;
	return 0;			/* too large for Unicode */
}
int
flush_utf8_box(utf8_box *u) {
	if (u->_saved_pending) {
		/* retrieve _saved to text */
		int b =  u->_saved; u->_saved_pending = 0;
		switch (process_first_byte(u, b)) {
		case 1:	/* it's a real character */
			return finished_sequence(u, 1);
		case 0:	/* it's a lonely leading byte */
		case -1:/* it's garbage; return as garbage */
			return finished_sequence(u, -1);
		}
	}

	return finished_sequence(u, -u->_pos);	/* u->_pos may be 0 here */
}

/* End library utf8 source code */
#endif	/* _UTF8_CODE_ */

#ifdef	lint
static void
satisfy_lint(void *x) {
	/* calls of all external entries of utf8 */
	clear_utf8_box(0);
	box_utf8(0, 0);
	flush_utf8_box(0);

	satisfy_lint(x);
}
#endif	/* lint */
