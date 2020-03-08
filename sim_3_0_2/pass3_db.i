/*	This file is part of the software similarity tester SIM.    -*-mode:C-*-
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: pass3_db.i,v 2.1 2017-11-27 20:15:53 dick Exp $
*/

/* activated by macro DB_RUN */

static void
db_run_info(const char *msg, const struct run *run, int lines_too) {
	const struct chunk *cnk0 = &run->rn_chunk0;
	const struct chunk *cnk1 = &run->rn_chunk1;

	if (msg) {
		fprintf(Debug_File, "%s: ", msg);
	}
	fprintf(Debug_File, "\"%s\" / \"%s\":\n",
		cnk0->ch_text->tx_fname, cnk1->ch_text->tx_fname
	);
	fprintf(Debug_File, "from %s %s/%s to %s/%s:", Token_Name,
		size_t2string(cnk0->ch_first.ps_tk_cnt),
		size_t2string(cnk1->ch_first.ps_tk_cnt),
		size_t2string(cnk0->ch_last.ps_tk_cnt),
		size_t2string(cnk1->ch_last.ps_tk_cnt)
	);
	if (lines_too) {
		fprintf(Debug_File, " from lines %s/%s to %s/%s:",
			size_t2string(cnk0->ch_first.ps_nl_cnt),
			size_t2string(cnk1->ch_first.ps_nl_cnt),
			size_t2string(cnk0->ch_last.ps_nl_cnt),
			size_t2string(cnk1->ch_last.ps_nl_cnt)
		);
	}
	fprintf(Debug_File, " %s %s%s\n",
		size_t2string(run->rn_size),
		Token_Name, (run->rn_size == 1 ? "" : "s")
	);
}

static void
db_chunk(const struct chunk *cnk) {
	/* print the tokens in the chunk, with a one-char margin */
	size_t i;
	const struct position *first = &cnk->ch_first;
	const struct position *last = &cnk->ch_last;
	size_t start = cnk->ch_text->tx_start;

	if (first->ps_tk_cnt > 0) {
		fprintf(Debug_File, "...");
		fprint_token(Debug_File,
			Token_Array[start + first->ps_tk_cnt - 1]);
		fprintf(Debug_File, "  ");
	}
	else {	/* create same offset as above */
		fprintf(Debug_File, "       ");
	}

	for (i = first->ps_tk_cnt; i <= last->ps_tk_cnt; i++) {
		fprintf(Debug_File, " ");
		fprint_token(Debug_File, Token_Array[start + i]);
	}

	if (start + last->ps_tk_cnt + 1 < cnk->ch_text->tx_limit) {
		fprintf(Debug_File, "  ");
		fprint_token(Debug_File,
			Token_Array[start + last->ps_tk_cnt + 1]);
		fprintf(Debug_File, "...");
	}

	fprintf(Debug_File, "\n");
}

static void
db_run(const struct run *run) {
	/* prints detailed data about a run */
	const struct chunk *cnk0 = &run->rn_chunk0;
	const struct chunk *cnk1 = &run->rn_chunk1;

	db_run_info(0, run, 1);
	db_chunk(cnk0);
	db_chunk(cnk1);
}
