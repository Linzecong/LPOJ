/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: idf.c,v 2.21 2017-12-11 14:12:34 dick Exp $
*/

#include	<string.h>
#include	<stdint.h>

#include	"system.par"
#include	"token.h"
#include	"idf.h"

Token
idf_in_list(
	const char *str,
	const struct idf list[],
	size_t list_size,
	Token default_token
) {
	int first = 0;
	int last = (int) (list_size / sizeof (struct idf)) - 1;

	while (first < last) {
		int middle = (first + last) / 2;

		if (strcmp(str, list[middle].id_tag) > 0) {
			first = middle + 1;
		}
		else {
			last = middle;
		}
	}
	return (strcmp(str, list[first].id_tag) == 0
	?	list[first].id_tr
	:	default_token
	);
}

#define	HASH(h,ch)	(((h) * 8209) + (ch)*613)

Token
idf_hashed(const char *str) {
	int32_t h = 0;

	/* let's be careful about ranges; if done wrong it's hard to debug */
	while (*str) {
		int ch = *str++ & 0377;

		/* ignore spaces in spaced words */
		if (ch == ' ') continue;

		/* -1 <= h <= 2^31-1 */
		h = HASH(h, ch);
		/* -2^31 <= h <= 2^31-1 */
		if (h < 0) {
			/* -2^31 <= h <= -1 */
			h += 2147483647;	/* 2^31-1 */
			/* -1 <= h <= 2^31-2 */
		}
		else {
			/* 0 <= h <= 2^31-1 */
		}
		/* -1 <= h <= 2^31-1 */
	}
	/* -1 <= h <= 2^31-1 */
	if (h < 0) {
		/* h = -1 */
		h = 0;
	}
	/* 0 <= h <= 2^31-1 */
	h %= (N_TOKENS - N_REGULAR_TOKENS - 1);
	/* 0 <= h < N_TOKENS - N_REGULAR_TOKENS - 1 */
	h += N_REGULAR_TOKENS;
	/* N_REGULAR_TOKENS <= h < N_TOKENS - 1 */
	return int2Token(h);
	/* this avoids the regular tokens and End_Of_Line */
}

void
lower_case(char *str) {
	char *s;

	for (s = str; *s; s++) {
		if ('A' <= *s && *s <= 'Z') {
			*s += (-'A' + 'a');
		}
	}
}
