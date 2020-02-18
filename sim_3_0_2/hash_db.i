/*	This file is part of the software similarity tester SIM.    -*-mode:C-*-
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: hash_db.i,v 2.1 2017-11-27 20:15:52 dick Exp $
*/

/* activated by macro DB_FORW_REF */

static void
db_print_forward_references(void) {
	/* also determines the lengths of the chains, for statistics */
	size_t n;
	size_t n_frw_chains = 0;
	size_t tot_frwc_len = 0;
	size_t *print_loc_of =
		(size_t *)Calloc(Token_Array_Length(), sizeof (size_t));
	size_t *number_of_chains_of_length =
		(size_t *)Calloc(Token_Array_Length(), sizeof (size_t));

	/* print the references */
	for (n = 1; n < Token_Array_Length(); n++) {
		size_t fw = forward_reference[n];
		if (fw == 0) continue;

		/* we have a chain */
		fprintf(Debug_File, "FWR[%s]:", any_uint2string(n, 0));

		/* is it old? */
		if (print_loc_of[n]) {
			fprintf(Debug_File, " see %s\n",
				any_uint2string(print_loc_of[n], 0));
			continue;
		}

		/* no, we have the beginning of a new chain */
		size_t count = 0;
		do {
			count++;
			fprintf(Debug_File, " %s",
				any_uint2string(fw, 0));
			print_loc_of[fw] = n;
			fw = forward_reference[fw];
		} while(fw && fw != n);	/* continuing and not circular */
		if (fw) {	/* circular */
			fprintf(Debug_File, " C");
			count++;
		}
		n_frw_chains++;
		tot_frwc_len += count;
		number_of_chains_of_length[count]++;
		fprintf(Debug_File, "\n");
	}

	/* print the chain lengths */
	for (n = 1; n < Token_Array_Length(); n++) {
		if (number_of_chains_of_length[n]) {
			fprintf(Debug_File, "length[%d]:\t%d\n",
				n, number_of_chains_of_length[n]);
		}
	}

	fprintf(Debug_File,
		"text length = %s, # forward chains = %s, av. frw chain length = %.2f\n\n",
		any_uint2string(Token_Array_Length(), 0),
		any_uint2string(n_frw_chains, 0),
		(n_frw_chains ? 1.0 * tot_frwc_len / n_frw_chains : 0.0)
	);

	Free(number_of_chains_of_length);
	Free(print_loc_of);
}

static void
db_frw_chain(size_t n, char *crossed_out) {
	if (forward_reference[n] == 0) {
		fprintf(Debug_File,
			">>>> db_frw_chain() forward_reference[n] == 0 <<<<\n"
		);
		return;
	}

	size_t n_entries = 0;
	size_t fw;

	for (fw = n; fw; fw = forward_reference[fw]) {
		if (crossed_out[fw]) {
			fprintf(Debug_File,
				">>>> error: forward references cross <<<<\n"
			);
		}
		n_entries++;
		crossed_out[fw] = 1;
	}
#ifdef	DB_FORW_REF_PRINT
	fprintf(Debug_File, "chain_start = %s, n_entries = %s\n",
		any_uint2string(n, 0), any_uint2string(n_entries, 0));
#endif	/* DB_FORW_REF_PRINT */
}

static void
db_forward_reference_check(const char *msg) {
	/*	Each forward_reference[n] starts in principle a new
		chain, and these chains never touch each other.
		We check this property by marking the positions in each
		chain in an array; if we meet a marked entry while
		following a chain, it must have been on an earlier chain
		and we have an error.
	*/
	size_t n;
	char *crossed_out = (char *)Calloc(Token_Array_Length(), sizeof (char));

	fprintf(Debug_File, "\n\n**** DB_FORWARD_REFERENCES, %s ****\n", msg);
	fprintf(Debug_File, "latest_index_table_size = %s\n",
		any_uint2string(latest_index_table_size, 0));

	if (forward_reference[0]) {
		fprintf(Debug_File,
			">>>> forward_reference[0] is not zero <<<<\n"
		);
	}
	for (n = 1; n < Token_Array_Length(); n++) {
		if (forward_reference[n] && !crossed_out[n]) {
			/* start of a new chain */
			db_frw_chain(n, crossed_out);
		}
	}
#ifdef	DB_FORW_REF_PRINT
	db_print_forward_references();
#endif	/* DB_FORW_REF_PRINT */

	Free(crossed_out);
}
