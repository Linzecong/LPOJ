/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: add_run.c,v 2.18 2016-06-12 13:00:04 dick Exp $
*/

#include	"sim.h"
#include	"text.h"
#include	"runs.h"
#include	"percentages.h"
#include	"options.h"
#include	"add_run.h"

/* Sends the run info to add_to_percentages or to add_to_runs. */
void
add_run(struct text *txt0, size_t i0,
	struct text *txt1, size_t i1,
	size_t size
) {
	if (is_set_option('p')) {
		add_to_percentages(txt0, txt1, size);
	}
	else {
		add_to_runs(txt0, i0, txt1, i1, size);
	}
}
