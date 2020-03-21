/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: pass2.c,v 2.30 2017-12-10 16:00:04 dick Exp $
*/

/* Note that this is pass 2 over the files, not phase 2 of the sim process. */

#include	<stdio.h>

#include	"debug.par"
#include	"sim.h"
#include	"token.h"
#include	"text.h"
#include	"lang.h"
#include	"pass2.h"

#ifdef	DB_POS
#include	"pass2_db.i"
#endif

/* begin instantiate */
static void sort_pos_list(struct position **);
#define	SORT_STRUCT		position
#define	SORT_NAME		sort_pos_list
#define	SORT_BEFORE(p1,p2)	((p1)->ps_tk_cnt < (p2)->ps_tk_cnt)
#define	SORT_NEXT		ps_next
#include	"sortlist.bdy"
/* end instantiate sort_pos_list() */

static void
match_pos_list_of(struct text *txt) {
	struct position *pos = txt->tx_pos;

	while (pos) {
		/* we scan the pos list and the file in parallel */

		/* find the corresponding line */
		while (pos->ps_tk_cnt >= lex_tk_cnt) {
			/* pos does not refer to this line, try the next */
			/* >= because of TK_CNT_HORROR */

			/* get the next eol position */
			int ok = 0;
			while (Next_Text_Token_Obtained()) {
				if (Token_EQ(lex_token, End_Of_Line)) {
					ok = 1;
					break;
				}
			}
			if (!ok) {
				/* reached end of file without obtaining EOL */
				if (!txt->tx_EOL_terminated) {
					/* that's OK then */
				} else {
					fprintf(stderr,
						">>>> File %s modified <<<<\n",
						txt->tx_fname
					);
				}
				break;
			}
#ifdef	DB_POS
			db_print_lex(txt->tx_fname);
#endif	/* DB_POS */
		}

		/* fill in the pos */
		pos->ps_nl_cnt = lex_nl_cnt - 1;	/* TK_CNT_HORROR */

		/* and get the next pos */
		pos = pos->ps_next;
	}
}

static void
pass2_txt(struct text *txt) {
	if (!txt->tx_pos)	/* no need to scan the file */
		return;

	/* Open_Text() initializes lex_nl_cnt and lex_tk_cnt */
	if (!Open_Text(txt)) {
		fprintf(stderr, ">>>> File %s disappeared <<<<\n",
			txt->tx_fname
		);
		return;
	}

	/* Sort the positions so they can be matched to the file; the linked
	   list of struct positions snakes through the struct positions in the
	   struct chunks in the struct runs.
	*/
#ifdef	DB_POS
	db_print_pos_list("before sorting", txt);
#endif	/* DB_POS */

	sort_pos_list(&txt->tx_pos);

#ifdef	DB_POS
	db_print_pos_list("after sorting", txt);
#endif	/* DB_POS */

#ifdef	DB_POS
	fprintf(Debug_File, "\n**** DB_PRINT_SCAN of %s ****\n", txt->tx_fname);
#endif	/* DB_POS */

	match_pos_list_of(txt);

#ifdef	DB_POS
	db_print_pos_list("after scanning", txt);
#endif	/* DB_POS */

	Close_Text();
}

void
Retrieve_Runs(void) {
	int n;

	for (n = 0; n < Number_of_Texts; n++) {
		pass2_txt(&Text[n]);
	}
}
