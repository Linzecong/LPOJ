/*	This file is part of the module ANY_INT.
	Written by Dick Grune, dick@dickgrune.com
	$Id: any_int.c,v 1.4 2017-01-22 14:50:00 Gebruiker Exp $
*/

#include	"any_int.h"

#define	N_INDEPENDENT_CALLS	12
#define	MAX_ANY_UINT_DIGITS	40	/* good for 128 bits, including sign */

/*Library module source prelude */
#undef	_ANY_UINT_CODE_
#ifndef	lint
#define	_ANY_UINT_CODE_
#endif
#ifdef	LIB
#define	_ANY_UINT_CODE_
#endif

#ifdef	_ANY_UINT_CODE_

/* Library module source code */

/* circular list of buffers */
static char buff[N_INDEPENDENT_CALLS][MAX_ANY_UINT_DIGITS+1];
static int next_buff_cnt = 0;

static char *
next_buff(void) {
	if (next_buff_cnt == N_INDEPENDENT_CALLS) next_buff_cnt = 0;
	return buff[next_buff_cnt++];
}

static const char *
int2string(vlong_uint val, int neg, int size) {
	char *res = next_buff() + MAX_ANY_UINT_DIGITS;	/* end of new buffer */
	*res = '\0';					/* insert EOS */

	/* protect size */
	if (size < 0 || size > MAX_ANY_UINT_DIGITS) size = 0;

	do {	/* one decimal character, the first always */
		*--res = "0123456789ABCDEF"[val % 10];
		size--;
		val = val / 10;
	} while (val > 0);

	if (neg) {
		*--res = '-';
		size--;
	}

	while (size > 0) {	/* fill up to size */
		*--res = ' ';
		size--;
	}

	return res;
}

const char *	/* transient * N_INDEPENDENT_CALLS */
any_int2string(vlong_int val, int size) {
	int neg = 0;
	if (val < 0) {
		val = - val;
		neg = 1;
	}
	return int2string((vlong_uint)val, neg, size);
}

const char *	/* transient * N_INDEPENDENT_CALLS */
any_uint2string(vlong_uint val, int size) {
	return int2string(val, 0, size);
}

/* End library module source code */
#endif	/* _ANY_UINT_CODE_ */

#ifdef	lint
static void
satisfy_lint(void *x) {
	any_int2string(0, 0);
	any_uint2string(0, 0);
	satisfy_lint(x);
}
#endif	/* lint */
