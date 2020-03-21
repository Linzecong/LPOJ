/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: pass3.c,v 2.43 2017-12-15 17:15:21 dick Exp $
*/

#include	<stdio.h>
#include	<string.h>

#include	"system.par"
#include	"debug.par"
#include	"sim.h"
#include	"options.h"
#include	"fname.h"
#include	"utf8.h"
#include	"text.h"
#include	"token.h"
#include	"runs.h"
#include	"percentages.h"
#include	"pass3.h"

#ifdef	DB_RUN
#include	"tokenarray.h"
#include	"pass3_db.i"
#endif

/* Positioning UTF-8 non-ASCII characters is a problem. Even if we use
   a much finer grain than just 10 Courier characters to the inch, which is
   easy to do, and even if we accessed UTF-8 character width tables, which are
   not readily available, the problem still cannot be solved because we have
   no way to position the middle bar over non-integer character widths.
   Users can avoid the problem by using the -d option, so we just do
   reasonable best effort, based on a granularity of 1 pt and a
   font size of 10 pts.
*/

typedef int pts;
#define	ASCII_WIDTH	(10)
/* It turns out that fairly precisely
      9 Courier chars = 5 Hangul chars == 15 UTF-8 bytes
   in length. Since 9 Courier chars occupy 90 pts, this makes 1 UTF-8 byte
   equal to 6 pts. This is a heuristic, for want of something better.
*/
#define	UTF8_WIDTH	(6)

#define	is_ascii_byte(bt)		((bt&0200) == 0000)
#define	is_leading_utf8_byte(bt)	((bt&0300) == 0300)
#define	is_continuation_utf8_byte(bt)	((bt&0300) == 0200)

							/* AUXILIARIES */

static pts
print_string(const char *str) {
	/* assumes str to be UTF-8-correct */
	const char *s = str;

	fprintf(Output_File, "%s", str);

	/* compute the printed length */
	pts len = 0;
	while (*s) {
		len += (is_ascii_byte(*s) ? ASCII_WIDTH : UTF8_WIDTH);
		s++;
	}
	return len;
}

static pts
width_of_size_t(size_t u) {
	pts res = ASCII_WIDTH;

	while (u > 9) {
		u /= 10, res += ASCII_WIDTH;
	}
	return res;
}

static pts
print_size_t(size_t u) {
	fprintf(Output_File, "%s", size_t2string(u));
	return width_of_size_t(u);
}

							/* CHUNK PRINTING */

static pts
print_header(const struct chunk *cnk) {
	pts width = 0;

	width += print_string(cnk->ch_text->tx_fname);
	width += print_string(": line ");
	width += print_size_t(cnk->ch_first.ps_nl_cnt);
	width += print_string("-");
	width += print_size_t(cnk->ch_last.ps_nl_cnt);
	return width;
}

static void
print_spaces(pts n) {
	while (n > 0) {
		n -= print_string(" ");
	}
}

static void
print_char(char ch) {
	fprintf(Output_File, "%c", ch);
}

static void
print_2_headers(
    const struct chunk *cnk0, const struct chunk *cnk1,
    pts max_line_length, size_t size
) {
	if (!is_set_option('d')) {
		/* no assumptions about the lengths of the file names! */
		pts width = print_header(cnk0);
		print_spaces(max_line_length - width);
		print_char('|');
		width = print_header(cnk1);
		/* add width of the print to come */
		width += ASCII_WIDTH + width_of_size_t(size) + ASCII_WIDTH;
		print_spaces(max_line_length - width);
		fprintf(Output_File, "[%s]\n", size_t2string(size));
	}
	else {
		/* diff-like format */
		(void)print_header(cnk0);
		fprintf(Output_File, " [%s]\n", size_t2string(size));
		(void)print_header(cnk1);
		print_char('\n');
	}
}

static FILE *
open_chunk(const struct chunk *cnk) {
	/* Opens the file in which the chunk resides, positions the file
	   at the beginning of the chunk and returns the file pointer.
	*/

	const char *fname = cnk->ch_text->tx_fname;
	FILE *f = Fopen(str2Fname(fname), "r");
	/* ^ Note that we use [Ff]open() here, which opens a character stream,
	   rather than Open_Text(), which opens a token stream.
	*/

	if (!f) {
		fprintf(stderr, ">>>> File %s disappeared <<<<\n", fname);
		f = fopen(NULLFILE, "r");
	}

	/* skip ch_first.ps_nl_cnt newlines */
	size_t nl_cnt = cnk->ch_first.ps_nl_cnt;
	while (nl_cnt > 1) {
		int ch = getc(f);
		if (ch < 0) break;

		if (ch == '\n') {
			nl_cnt--;
		}
	}

	return f;
}

static int
fill_ubox(FILE *f, utf8_box *u) {
	int len = 0;
	while (len == 0) {
		do {	int byte = getc(f);
			if (byte < 0) return 0;
			len = box_utf8(byte, u);
		} while (len <= 0);		/* reject bad UTF-8 */
		if (!is_valid_utf8(u)) len = 0;	/* reject non-Unicode */
	}
	return len;
}

static pts
print_line(FILE *f, pts max_line_length) {
	/* Reads one line from f and prints it in condensed form, up to a
	   maximum length of max_line_length.
	*/
	pts width = 0;
	int at_beginning_of_line = 1, last_was_space = 0;
	utf8_box u; clear_utf8_box(&u);

	int len;
	while (len = fill_ubox(f, &u)) {
		/* take a critical look at what we've got */
		char u0 = u.text[0];
		if (u0 == '\n') break;			/* stop on end of line*/
		if (u0 == '\t') u0 = u.text[0] = ' ';	/* reduce tab to space*/
		if ('\0' <= u0 && u0 < ' ') continue;	/* skip non-printables*/

		/* condense spaces where appropriate */
		if (!at_beginning_of_line && u0 == ' ') {
			if (last_was_space) continue;
			last_was_space = 1;
		} else {
			at_beginning_of_line = 0;
			last_was_space = 0;
		}

		/* UTF8 char ok, print it? */
		pts ch_width = (len == 1 ? ASCII_WIDTH : len * UTF8_WIDTH);
		if (width + ch_width <= max_line_length) {
			fprintf(Output_File, "%s", u.text);
			width += ch_width;
		}
	}
	return width;
}

static void
print_1_line(FILE *f, const char *marker) {
	/* displays one line from f, preceded by the marker */
	/* there is no length limitation, so we do not bother with UTF-8 */

	fprintf(Output_File, "%s ", marker);

	int ch;
	while ((ch = getc(f)), ch > 0 && ch != '\n') {
		print_char(ch);
	}
	print_char('\n');
}

static void
print_2_chunks(
    const struct chunk *cnk0, const struct chunk *cnk1,
    pts max_line_length
) {
	/* open the files holding the chunks at the positions of those chunks */
	FILE *f0 = open_chunk(cnk0);
	FILE *f1 = open_chunk(cnk1);

	/* display the chunks in the required format */
	size_t nl_cnt0 = cnk0->ch_last.ps_nl_cnt - cnk0->ch_first.ps_nl_cnt + 1;
	size_t nl_cnt1 = cnk1->ch_last.ps_nl_cnt - cnk1->ch_first.ps_nl_cnt + 1;

	if (!is_set_option('d')) {
		/* print 2-column format */
		while (nl_cnt0 != 0 || nl_cnt1 != 0) {
			pts width = 0;
			if (nl_cnt0) {
				width = print_line(f0, max_line_length);
				nl_cnt0--;
			}
			print_spaces(max_line_length - width);
			print_char('|');
			if (nl_cnt1) {
				(void)print_line(f1, max_line_length);
				nl_cnt1--;
			}
			print_char('\n');
		}
	}
	else {
		/* display the chunks in a diff(1)-like format */
		while (nl_cnt0--) {
			print_1_line(f0, "<");
		}
		(void)print_string("---\n");
		while (nl_cnt1--) {
			print_1_line(f1, ">");
		}
	}

	/* close the pertinent files */
	fclose(f0);
	fclose(f1);
}

static void
print_run(const struct run *run) {
	pts max_line_length = (Page_Width / 2 - 1) * ASCII_WIDTH;

	const struct chunk *cnk0 = &run->rn_chunk0;
	const struct chunk *cnk1 = &run->rn_chunk1;

	print_2_headers(cnk0, cnk1, max_line_length, run->rn_size);

	/* stop if that suffices */
	if (is_set_option('n'))	return;

	print_2_chunks(cnk0, cnk1, max_line_length);
}

							/* PRINT RUNS */

void
Print_Runs(void) {
#ifdef	DB_RUN
	fprintf(Debug_File, "Starting Print_Runs()\n");
#endif	/* DB_RUN */
	const struct run *run =
		(is_set_option('u') ? unsorted_runs() : sorted_runs());

	while (run) {
#ifdef	DB_RUN
		db_run(run);
#endif	/* DB_RUN */
		print_run(run);
		print_char('\n');
		fflush(Output_File);
		run = run->rn_next;
	}

	discard_runs();
}
