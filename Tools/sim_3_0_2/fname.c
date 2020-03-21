/*	This file is part of the auxiliaries library.
	Written by Dick Grune, dick@dickgrune.com
	$Id: fname.c,v 1.10 2017-12-13 17:41:34 Gebruiker Exp $
*/

/*	Support for Unicode file names in Windows */

/*	Two data types are involved in Unicode file names in Windows:

		UTF16 strings, the file names as stored by Windows, and
		UTF8 strings, the names as they are displayed and stored.

	The conversion between these two proceeds through CodePoints,
	the 'real' values of the characters, of which UTF16 strings and
	UTF8 strings are the compressed representations.

	The module consists of two levels: a set of static routines

		int UTF8_sequence_to_CodePoint(const UTF8 *s, UTF32 *cp),
		int UTF16_sequence_to_CodePoint(const UTF16 *s, UTF32 *cp),
		const UTF8 *CodePoint_to_UTF8_sequence(UTF32 c),
		const Fchar *CodePoint_to_UTF16_sequence(UTF32 cp)

	which convert from and to CodePoints; and two global routines

		const char *Fname2str(const Fchar *fn),
		const Fchar *str2Fname(const char *s)

	which convert from Unicode file names to UTF-8 strings and vice versa.

	Unicode file names are obtained by calls of Opendir() and Readdir(),
	as defined in fname.h.
*/

#include	"fname.h"

/*Library module source prelude */
#undef	_FNAME_CODE_
#ifndef	lint
#define	_FNAME_CODE_
#endif
#ifdef	LIB
#define	_FNAME_CODE_
#endif

#ifdef	_FNAME_CODE_

/* Library module source code */

#ifdef	_UNICODE
typedef uint8_t UTF8;
typedef uint16_t UTF16;
typedef uint32_t UTF32;

#define	BAD_CodePoint	(UTF32)(-1)

/* mask of n left-aligned 1-s in a UTF8 */
#define	LMASK(n) (((1<<(n))-1)<<(8-(n)))
/* mask of n right-aligned 1-s */
#define	RMASK(n)	((1u<<(n))-1)

						/* SEQUENCE -> CODEPOINT */
static int
nmb_leading_ones_in_UTF8(UTF8 c) {
	int n = 0;

	while (c&LMASK(1)) {
		c <<= 1, n++;
	}

	return n;
}

static UTF32
get_UTF8_tail(const UTF8 *s, int n) {
	UTF32 res = 0;
	int i;

	/* scoop up n UTF-8s */
	for (i = 0; i < n; i++) {
		if ((s[i]&LMASK(2)) != LMASK(1)) return BAD_CodePoint;
		res = (res<<6) + (s[i]&RMASK(6));
	}

	return res;
}

static int /* number of UTF8s used; cp = BAD_CodePoint for error */
UTF8_sequence_to_CodePoint(const UTF8 *s, UTF32 *cp) {
	UTF8 head = s[0];
	int head_length = 1;
	const UTF8 *tail = &s[1];
	int tail_length;
	UTF32 tail_value;

	if ((head&LMASK(1)) == 0) {
		*cp = head;
		return head_length;
	}

	tail_length = nmb_leading_ones_in_UTF8(head) - 1;
	if (tail_length < 1 || tail_length > 3) goto error;

	tail_value = get_UTF8_tail(tail, tail_length);
	if (tail_value == BAD_CodePoint) goto error;

	*cp = ((head&RMASK(6-tail_length))<<(tail_length*6)) | tail_value;

	return head_length+tail_length;

 error:	{	int i = head_length;	/* skip the head */

		/* skip until new head */
		while ((s[i]&LMASK(1)) != 0) {
			i++;
		}
		*cp = BAD_CodePoint;

		return i;
	}
}

static int
is_in_BMP(UTF32 c) {	/* Basic Multilingual Plane */
	return c <= 0xD7FF || (0xE000 <= c && c < 0x10000);
}

static int
is_high_surrogate(UTF16 c) {
	return 0xD800 <= c && c <= 0xDBFF;
}

static int
is_low_surrogate(UTF16 c) {
	return 0xDC00 <= c && c <= 0xDFFF;
}

static int /* number of UTF16s used; cp = BAD_CodePoint for error */
UTF16_sequence_to_CodePoint(const UTF16 *s, UTF32 *cp) {
	/* adapted from code from http://unicode.org/faq/utf_bom.html */
	UTF32 plane_number;
	UTF32 position;

	if (is_in_BMP(s[0])) {
		*cp = s[0];
		return 1;
	}

	/* s[0:1] must be a surrogate pair */
	if (!is_high_surrogate(s[0])) goto error;
	if (!is_low_surrogate(s[1])) goto error;

	/* get the plane number */
	plane_number = (s[0] >> 6) & RMASK(5);
	plane_number = plane_number + 1; /* to offset it from the BMP */

	/* get the position in the plane */
	position = ((s[0] & RMASK(6)) << 10) | (s[1] & RMASK(10));

	/* combine them */
	*cp = plane_number << 16 | position;

	return 2;

 error:	{	int i = 1;	/* skip one UTF-16 */

		/* skip until acceptable UTF-16 */
		while (!is_in_BMP(s[i]) && !is_high_surrogate(s[0])) {
			i++;
		}
		*cp = BAD_CodePoint;

		return i;
	}
}

						/* CODEPOINT -> SEQUENCE */
static const UTF8 * /* transient */
CodePoint_to_UTF8_sequence(UTF32 c) {
	/* adapted from code by user R on stackoverflow.com */
	static UTF8 buff[6];
	UTF8 *bp = buff;

	if (c < 0x80) {
		/* it fits in 7 bits */
		*bp++ = (c>>0)&RMASK(7);
	}
	else if (c < 0x800) {
		/* it fits in 11 bits */
		*bp++ = 0xC0 | ((c>>6)&RMASK(5));
		*bp++ = 0x80 | ((c>>0)&RMASK(6));
	}
	else if (c < 0x10000) {
		/* it fits in 16 bits */
		if (!is_in_BMP(c)) {
			/* it is in the forbidden zone */
			return NULL;
		}
		*bp++ = 0xE0 | ((c>>12)&RMASK(4));
		*bp++ = 0x80 | ((c>>6)&RMASK(6));
		*bp++ = 0x80 | ((c>>0)&RMASK(6));
	}
	else if (c < 0x110000) {
		/* it fits in 21 bits */
		*bp++ = 0xF0 | ((c>>18)&RMASK(3));
		*bp++ = 0x80 | ((c>>12)&RMASK(6));
		*bp++ = 0x80 | ((c>>6)&RMASK(6));
		*bp++ = 0x80 | ((c>>0)&RMASK(6));
	}
	else return NULL;

	*bp = '\0';

	return buff;
}

static UTF16 *		/* transient */
CodePoint_to_UTF16_sequence(UTF32 cp) {
	/* adapted from code from http://unicode.org/faq/utf_bom.html */
	static UTF16 res[3];

	if (is_in_BMP(cp)) {
		res[0] = cp;
		res[1] = '\0';
		return res;
	}

	if (cp >= 0x10000) {
		UTF16 position = (UTF16) cp;
		UTF16 plane_number = ((cp >> 16) & RMASK(5)) - 1;

		res[0] = 0xD800 | (plane_number << 6) | (position >> 10);
		res[1] = 0xDC00 | (position & RMASK(10));
		res[2] = '\0';

		return res;
	}

	/* the CodePoint does not correspond to a UTF16 sequence */
	return NULL;
}

const char *	/* transient */
Fname2str(const Fchar *fn) {
	/* converts a Fchar (wchar_t) string to an UTF-8 string */
	static UTF8 res[1024];
	UTF8 *rp = &res[0];
	int i = 0;

	if (fn == NULL) return NULL;

	while (fn[i]) {
		UTF32 cp;
		const UTF8 *p;

		/* get Codepoint from one or two Fchar chars */
		i += UTF16_sequence_to_CodePoint(&fn[i], &cp);
		if (cp == BAD_CodePoint) goto error;

		/* convert code point to UTF8 sequence */
		p = CodePoint_to_UTF8_sequence(cp);
		if (p == NULL) goto error;

		/* append it to the output */
		while (*p) {
			*rp++ = *p++;
		}
		continue;
	error:
		*rp++ = '?';
	}

	*rp = '\0';
	return (const char *)res;
}

const Fchar *	/* transient */
str2Fname(const char *s) {
	/* converts a possibly UTF-8 string to an Fchar (wchar_t) string */
	static Fchar res[512];
	Fchar *rp = &res[0];
	int i = 0;

	if (s == NULL) return NULL;

	while (s[i]) {
		UTF32 cp;
		const Fchar *p;

		/* get Codepoint from one to four UTF-8s */
		i += UTF8_sequence_to_CodePoint((const UTF8 *)&s[i], &cp);
		if (cp == BAD_CodePoint) goto error;

		/* convert code point to UTF-16 sequence */
		p = CodePoint_to_UTF16_sequence(cp);
		if (p == NULL) goto error;

		/* append it to the output */
		while (*p) {
			*rp++ = *p++;
		}
		continue;
	error:
		*rp++ = '?';
	}

	*rp = '\0';
	return res;
}

						/* OTHER UTF-16 ROUTINES */
int
Stat(const Fchar *fn, struct stat *st) {
	/* why on earth does _wstat use a funny struct _stat ? */
	return _wstat(fn, (struct _stat *)st);
}

FILE *
Fopen(const Fchar *fn, const char *rb) {	/* stream is still char* */
	Fchar fn_copy[512];

	/* avoid possible transiency of fn */
	Fnamecpy(fn_copy, fn);
	return _tfopen(fn_copy, str2Fname(rb));
}

#endif	/* _UNICODE */

/* End library module source code */
#endif	/* _FNAME_CODE_ */

#ifdef	lint
static void
satisfy_lint(void *x) {
	/* lint cannot handle Fchar complications */
	satisfy_lint(x);
}
#endif	/* lint */
