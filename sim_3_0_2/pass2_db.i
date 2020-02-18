/*	This file is part of the software similarity tester SIM.    -*-mode:C-*-
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: pass2_db.i,v 2.1 2017-11-27 20:15:53 dick Exp $
*/

/* activated by macro DB_POS */

static void
db_print_pos(const struct position *pos) {
	fprintf(Debug_File, "pos type = %s; %s count = %u",
		(pos->ps_type == 0 ? "first" : " last"),
		Token_Name,
		pos->ps_tk_cnt
	);
	fprintf(Debug_File, ", line # = ");
	if (pos->ps_nl_cnt == (size_t) -1) {
		fprintf(Debug_File, "<NOT SET>");
	}
	else {
		fprintf(Debug_File, "%u", pos->ps_nl_cnt);
	}
	fprintf(Debug_File, "\n");
}

static void
db_print_pos_list(const char *msg, const struct text *txt) {
	fprintf(Debug_File, "\n**** DB_PRINT_POS_LIST of %s, %s ****\n",
		txt->tx_fname, msg);

	const struct position *pos = txt->tx_pos;
	while (pos) {
		db_print_pos(pos);
		pos = pos->ps_next;
	}
	fprintf(Debug_File, "\n");
}

static void
db_print_lex(const char *fn) {
	fprintf(Debug_File,
		"%s: lex_tk_cnt = %u, lex_nl_cnt = %u, lex_token = ",
		fn, lex_tk_cnt, lex_nl_cnt);
	fprint_token(Debug_File, lex_token);
	fprintf(Debug_File, "\n");
}
