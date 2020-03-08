/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: runs.c,v 1.19 2017-11-27 20:15:54 dick Exp $
*/

#include	"sim.h"
#include	"text.h"
#include	"runs.h"
#include	"Malloc.h"
#include	"debug.par"

static struct run *runs;
static void set_chunk(
    struct chunk *cnk, struct text *txt, size_t start, size_t size);
static void set_pos(
    struct position *pos, int type, struct text *txt, size_t start);

void
add_to_runs(
    struct text *txt0, size_t i0, struct text *txt1, size_t i1,
    size_t size
) {
	struct run *r = new(struct run);
	/* This should always succeed, since releasing the forward_reference[]
	   and the last_index[] tables will have freed large amounts of memory,
	   and  massive comparisons as in percentage.c are not reasonable and
	   quite useless here, due to the enormous amount of output to be
	   expected.
	*/

	set_chunk(&r->rn_chunk0, txt0, i0 - txt0->tx_start, size);
	set_chunk(&r->rn_chunk1, txt1, i1 - txt1->tx_start, size);
	r->rn_size = size;

#ifdef	DB_RUN
	fprintf(Debug_File, "add_to_runs: %s, %s, %d\n",
		r->rn_chunk0.ch_text->tx_fname,
		r->rn_chunk1.ch_text->tx_fname,
		r->rn_size);
#endif
	r->rn_next = runs;
	runs = r;
}

static void
set_chunk(struct chunk *cnk, struct text *txt,
	  size_t start, size_t size
) {
	/*	Fill the chunk *cnk with info about the piece of text
		in txt starting at start extending over size tokens.
	*/
	cnk->ch_text = txt;
	set_pos(&cnk->ch_first, 0, txt, start);
	set_pos(&cnk->ch_last, 1, txt, start + size - 1);
}

static void
set_pos(struct position *pos, int type, struct text *txt, size_t start) {
	/* Fill a single struct position */
	pos->ps_next = txt->tx_pos;
	txt->tx_pos = pos;

	pos->ps_type = type;
	pos->ps_tk_cnt = start;
	pos->ps_nl_cnt = (size_t) -1;		/* uninitialized */
}

/* begin instantiate */
static void sort_run_list(struct run **listhook);
#define	SORT_STRUCT		run
#define	SORT_NAME		sort_run_list
#define	SORT_BEFORE(r0,r1)	((r0)->rn_size > (r1)->rn_size)
#define	SORT_NEXT		rn_next
#include	"sortlist.bdy"
/* end instantiate */

static void
reverse_runs(struct run **r_p) {
	struct run *r = *r_p;
	struct run *res = 0;

	while (r) {
		struct run *top = r;
		r = top->rn_next;
		top->rn_next = res;
		res = top;
	}
	*r_p = res;
}

struct run *
unsorted_runs(void) {
	reverse_runs(&runs);
	return runs;
}

struct run *
sorted_runs(void) {
	reverse_runs(&runs);
	sort_run_list(&runs);
	return runs;
}

void
discard_runs(void) {
	while (runs) {
		struct run *r = runs;
		runs = r->rn_next;
		Free(r);
	}
}
