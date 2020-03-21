/*	This file is part of the auxiliaries library.
	Written by Dick Grune, dick@dickgrune.com
	$Id: utf8.h,v 1.10 2017-12-14 15:39:23 Gebruiker Exp $
*/

/* Tracking (Modified) UTF-8 sequences */

#ifndef	_UTF8_H_
#define _UTF8_H_

/*****
Implements a type 'utf8_box'. Bytes can be put in a utf8_box, and when
a complete UTF-8 sequence has been received by the box the user is signalled
and the sequence + its code point can be found in the box.

void clear_utf8_box(utf8_box *u);
    Clears the box; needs to be called only once.

int box_utf8(char c, utf8_box *u);
    the byte c is put in the box.
    return value = 0:
        c is accepted and stored in the box; waiting for more bytes.
    return value > 0:
        c is accepted, completing a correct UTF-8 sequence;
	the complete sequence is in u->text ('\0'-terminated),
	the sequence value is in 'u->codepoint',
	and the length is 'return value'.
    return value < 0:
        c does not continue the UTF-8 sequence in the box and is stored for
	future use;
	the incomplete sequence is in u->text (not '\0'-terminated);
	its length is -'return value'.

bool is_valid_utf8(utf8_box *u);
    returns 1 if the box is finished and contains a valid Unicode UTF-8
    sequence, and 0 otherwise.

int flush_utf8_box(utf8_box *u);
    should be called at the end, to flush out any partial UTF-8 byes left.
    return value = 0:
        the box was empty.
    return value > 0:
        the box contains a complete UTF-8 sequence (actually a single ASCII95
	character); for values see above.
    return value < 0:
        the box contains an incomplete UTF-8 sequence; for values see above.

Since correct UTF-8 sequences cannot contain '\0', '\0' is treated as an
incorrect UTF-8 sequence, and yields a return value 0f -1. Valid encoding of
the codepoint 0 is 0300 0200.

The box accepts overlong encodings without indication; so decode to code point
followed by encode from code point need not give the same UTF-8 sequence back.

Utf8_box is fairly low-level; it may be convenient to wrap a layer around it.
See demo code below.
*****/

#if 	0	/* demo code */
/* This UTF-8 demo copies a file from standard input to standard output and
   then lists on standard error the frequency of the lengths of the UTF-8
   sequences and the frequency of bad UTF-8 sequences.
*/
#include	<stdio.h>

#include	"utf8.h"

int len_cnt[7];
int bad_cnt;

static void
do_utf8(int ch, utf8_box *u, int flushing) {
	int len = (flushing ? flush_utf8_box(u) : box_utf8(ch, u));
	if (len > 0) {
		/* good UTF-8: u->text is '\0'-terminated */
		len_cnt[len]++;
		printf("%s", u->text);
	}
	else
	if (len < 0) {
		len = -len;
		/* bad UTF-8: u->text may contain '\0', only len is reliable */
		bad_cnt++;
		int i; for (i = 0; i < len; i++) {
			putchar(u->text[i] & 0377);
		}
	}
}

int
main(void) {
	utf8_box u;
	int ch;

	clear_utf8_box(&u);
	while ((ch = getc(stdin)) != EOF) {
		do_utf8(ch, &u, 0);
	}
	do_utf8(0, &u, 1);	/* flush */

	fprintf(stderr, "bad UTF-8:      %d\n", bad_cnt);
	int i; for (i = 1; i < 7; i++) {
		fprintf(stderr, "UTF-8 length %d: %d\n", i, len_cnt[i]);
	}
	return 0;
}
#endif

/* UTF-8 is a marvellous invention, putting any character in the world in a
   sequence of 8-bit bytes. However, the world has not yet decided to put the
   byte into char[], unsigned char[], wchar, or whatever.

   This module keeps within the C realm by putting UTF-8 in char[],
   and is careful about suppressing sign extension.
*/

/* Private entries */

struct _utf8_box {
	char text[8];
	int codepoint;
	short _size;
	short _pos;
	short _saved_pending;/* _saved may be 0, so it cannot serve as marker */
	short _saved;
};

/* Public entries */

typedef struct _utf8_box utf8_box;

extern void clear_utf8_box(utf8_box *u);
extern int box_utf8(char c, utf8_box *u);
extern int is_valid_utf8(utf8_box *u);
extern int flush_utf8_box(utf8_box *u);

#endif	/* _UTF8_H_ */
