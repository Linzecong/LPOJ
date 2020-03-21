/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: runs.h,v 1.14 2017-11-27 20:15:54 dick Exp $
*/

/*	Although all other segments of data in this program are described by
	giving the position of the first in the segment and that of the
	first not in the segment (so the size is the difference of the two),
	a `chunk' is given by first and last. This is done because later on we
	are interested in the actual position of the last token of it, and
	the position of the first token not in the segment gives no
	indication about that.
*/

struct chunk {
	/* a chunk of text */
	const struct text *ch_text;	/* pointer to the file */
	struct position ch_first;	/* first in chunk */
	struct position ch_last;	/* last in chunk */
};

struct run {				/* a 'run' of coincident tokens */
	struct run *rn_next;
	struct chunk rn_chunk0;		/* chunk in left file */
	struct chunk rn_chunk1;		/* chunk in right file */
	size_t rn_size;
};

extern void add_to_runs(
    struct text *txt0, size_t i0, struct text *txt1, size_t i1,
    size_t size);
extern struct run *sorted_runs(void);
extern struct run *unsorted_runs(void);
extern void discard_runs(void);
