/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: options.c,v 1.22 2017-11-26 18:10:15 dick Exp $
*/

#include	<stdio.h>
#include	<stdlib.h>

#include	"sim.h"
#include	"token.h"
#include	"lang.h"
#include	"options.h"

static char options[128];

static void bad_option_exit(
	const char *progname, const struct option *optlist,
	char *msg, int c
);
static int opt_value(
	const char *progname, const struct option *op,
	const char *arg, const char *argv[]
);

static int do_arg(
	const char *progname, const struct option *optlist,
	const char *arg, const char *argv[]
);

int
do_options(
	const char *progname, const struct option *optlist,
	int argc, const char *argv[]
) {
	int skips = 0;

	while (argc > 0 && argv[0][0] == '-') {
		int consumed = do_arg(progname, optlist, &argv[0][1], argv);

		argc -= consumed, argv += consumed, skips += consumed;
	}

	return skips;
}

void
set_option(char ch) {
	options[(int)ch]++;
}

int
is_set_option(int ch) {
	return options[ch];
}

static int
do_arg(
	const char *progname, const struct option *optlist,
	const char *arg, const char *argv[]
) {
	int consumed = 0;

	while (*arg) {
		/* treat argument character */
		char opc = *arg++;
		const struct option *op;

		for (op = optlist; op->op_char; op++) {
			if (opc == op->op_char) {
				set_option(opc);
				if (op->op_type != None) {
					consumed = opt_value(
						progname, op, arg, argv
					);
				}
				break;
			}
		}
		if (!op->op_char) {
			bad_option_exit(progname, optlist,
				   "option -%c unknown", opc
			);
			/*NOTREACHED*/
		}
		if (consumed) break;
	}
	if (!consumed) {
		consumed = 1;
	}

	return consumed;
}

static int
opt_value(
	const char *progname, const struct option *op,
	const char *arg, const char *argv[]
) {
	/* get the string and the number of args consumed */
	const char *string;
	int consumed;
	if (*arg) {
		string = arg, consumed = 1;
	}
	else if (argv[1]) {
		string = argv[1], consumed = 2;
	} else {
		string = 0, consumed = 0;
	}
	if (!string || !*string) {
		bad_option_exit(progname, (struct option *)0,
			"option -%c requires another argument", op->op_char
		);
		/*NOTREACHED*/
	}

	switch (op->op_type) {
	case Number:
		*(int *)op->op_value = atoi(string);
		break;
	case String:
		*(const char **)op->op_value = string;
		break;
	}

	return consumed;
}

void
allow_at_most_one_option_out_of(const char *opts) {
	const char *first;
	for (first = opts; *first; first++) {
		const char *second;
		for (second = first + 1; *second; second++) {
			if (is_set_option(*first) &&is_set_option(*second)) {
				char msg[256];
				sprintf(msg,
					"options -%c and -%c are incompatible",
					*first, *second
				);
				fatal(msg);
			}
		}
	}
}

static void
bad_option_exit(
    const char *progname, const struct option *optlist, char *msg, int c
) {
	fprintf(stderr, "%s: ", progname);
	fprintf(stderr, msg, c);
	fprintf(stderr, "\n");

	fprintf(stderr, "Possible options are:\n");
	const struct option *op;
	for (op = optlist; op->op_char; op++) {
		if (op->op_char == ' ') {
			fprintf(stderr, "\n\t\t%s\n", op->op_text);
		} else {
			fprintf(stderr, "\t-%c%c\t%s\n",
				op->op_char,
				(	op->op_type == Number ? 'N' :
					op->op_type == String ? 'F' :
					' '
				),
				op->op_text
			);
		}
	}
	exit(1);
}

static int
is_essential_option(char op_char) {
	if (op_char == 'r') return 1;
	if (op_char == 'w') return 1;
	if (is_set_option('p') && op_char == 't') return 1;
	return 0;
}

void
print_options(const char *progname, const struct option *optlist) {
	const struct option *op;

	if (!is_set_option('T')) {
		fprintf(stdout, "%s (%s)\n", progname, Version);
		fprintf(stdout, "Subject: %s\n", Subject);
	}
	fprintf(stdout, "Option settings:");
	if (!is_set_option('T')) fprintf(stdout, "\n");
	for (op = optlist; op->op_char; op++) {
		if (	is_set_option(op->op_char)
		||	is_essential_option(op->op_char)
		) {
			fprintf(stdout, " -%c", op->op_char);
			switch (op->op_type) {
			case None:	break;
			case Number:
				fprintf(stdout, "%d",
					*(int *)op->op_value);
				break;
			case String:
				fprintf(stdout, " %s",
					*(const char **)op->op_value);
				break;
			}
			if (!is_set_option('T')) {
				fprintf(stdout, " (%s)\n", op->op_text);
			}
		}
	}
	if (is_set_option('T')) fprintf(stdout, "\n");
}
