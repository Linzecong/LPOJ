/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: sim.c,v 2.73 2017-12-10 16:00:05 dick Exp $
*/

#include	<stdio.h>
#include	<stdlib.h>
#include	<string.h>

#include	"system.par"
#include	"settings.par"
#include	"sim.h"
#include	"options.h"
#include	"newargs.h"
#include	"token.h"
#include	"tokenarray.h"
#include	"text.h"
#include	"runs.h"
#include	"hash.h"
#include	"compare.h"
#include	"pass1.h"
#include	"pass2.h"
#include	"pass3.h"
#include	"percentages.h"
#include	"stream.h"
#include	"lang.h"

#include	"Malloc.h"
#include	"any_int.h"

const char *Version;

							/* PARAMETERS */
/* Command-line parameters, with defaults */
int Min_Run_Size = DEFAULT_MIN_RUN_SIZE;
int Page_Width = DEFAULT_PAGE_WIDTH;
int Threshold_Percentage = 1;
FILE *Output_File;
FILE *Debug_File;

/* Language-specific parameters; may be changed in Init_Language() */
const char *Token_Name = "token";

static const char *progname;		/* for error reporting */
static const char *output_name;		/* for redirecting the output */

static const struct option optlist[] = {
	{'r', "set minimum run size to N", Number, &Min_Run_Size},

	{' ', "output runs as text (default)", None, 0},
	{'d', "output in a diff-like format", None, 0},
	{'n', "suppress the text of the runs", None, 0},
	{'T', "suppress reporting the input files", None, 0},
	{'p', "output similarity in percentages", None, 0},
	{'P', "main contributing file to percentages only", None, 0},
	{'t', "threshold level of percentages", Number, &Threshold_Percentage},

	{'e', "compare each file to each file separately", None, 0},

	{' ', "compare a file to files after it only (default)", None, 0},
	{'a', "compare to all files", None, 0},
	{'S', "compare to old files only", None, 0},
	{'s', "do not compare a file to itself", None, 0},

	{' ', "sorted output, most significant first (default)", None, 0},
	{'u', "unbuffered, unsorted output", None, 0},

	{' ', "miscellaneous options:", None, 0},
	{'f', "function-like forms only", None, 0},
	{'F', "keep function identifiers in tact", None, 0},
	{'R', "recurse into subdirectories", None, 0},
	{'i', "read arguments (file names) from standard input", None, 0},
	{'o', "write output to file F", String, &output_name},
	{'w', "set page width to N", Number, &Page_Width},
	{'O', "show command line options at start-up", None, 0},
	{'M', "show memory usage info at close-down", None, 0},
	{'v', "show version number and compilation date", None, 0},
	{'-', "lexical scan output only", None, 0},
	{0, 0, 0, 0}
};

							/* SERVICE ROUTINES */
int
is_new_old_separator(const char *s) {
	if (strcmp(s, "/") == 0) return 1;
	if (strcmp(s, "|") == 0) return 1;
	return 0;
}

const char *
size_t2string(size_t s) {
	return any_uint2string(s, 0);
}

void
fatal(const char *msg) {
	fprintf(stderr, "%s: %s\n", progname, msg);
	exit(1);
}

							/* PROGRAM */

#ifdef	ARG_TEST
static void
show_args(const char *msg, int argc, const char *argv[]) {
	fprintf(stdout, "%s: ", msg);

	int i;
	for (i = 0; i < argc; i++) {
		fprintf(stdout, "arg[%d] = %s; ", i, argv[i]);
	}
	fprintf(stdout, "\n");
}
#endif	/* ARG_TEST */

int
main(int argc, const char *argv[]) {

	/* The value of Version derives from the string macro VERSION in the
	   Makefile if present. If not, a build time stamp is created.
	*/
	char version[40];
#ifdef	VERSION
	sprintf(version, "Version %s", VERSION);
#else
	sprintf(version, "Build %s, %s", __DATE__, __TIME__);
#endif
	Version = version;

	/* Save program name */
	progname = argv[0];
	argv++, argc--;				/* and skip it */

	/* Set the default output and debug streams */
	Output_File = stdout;
	Debug_File = stdout;
	Threshold_Percentage = 1;

	/* Options, default string values given above */

	/* override from language file */
	Init_Language();

	/* override from command line */
	{	int n_op = do_options(progname, optlist, argc, argv);
		argc -= n_op, argv += n_op;	/* and skip them */
	}

	/* Check options compatibility */
	allow_at_most_one_option_out_of("dnp");	/* alternative output formats */
	allow_at_most_one_option_out_of("aS");	/* alternative ranges */
	allow_at_most_one_option_out_of("sS");	/* self is outside old files */

	if (is_set_option('t')) {
		/* threshold means percentages */
		if (!is_set_option('p'))
		    fatal("option -t requires -p");
	}
	if (is_set_option('P')) {
		if (!is_set_option('p'))
		    fatal("option -P requires -p");
	}

	/* Treat the simple options */
	if (is_set_option('v')) {
		fprintf(stdout, "%s\n", Version);
		return 0;
	}

	if (is_set_option('p')) {
		set_option('s');
	}

	/* Check the value options */
	if (Min_Run_Size <= 0)
		fatal("bad run size");
	if (Page_Width <= 0)
		fatal("bad page width");

	if (is_set_option('p')) {
		if ((Threshold_Percentage > 100) || (Threshold_Percentage <= 0))
			fatal("threshold must be between 1 and 100");
	}

	if (output_name) {
		Output_File = fopen(output_name, "w");
		if (Output_File == 0) {
			char *msg = (char *)Malloc(strlen(output_name) + 100);

			sprintf(msg, "cannot open output file `%s'",
				output_name);
			fatal(msg);
			/*NOTREACHED*/
		}
	}

	/* Treat the input-determining options */
	if (is_set_option('i')) {
		/* read input file names from standard input */
		if (argc != 0)
			fatal("-i option conflicts with file arguments");
		get_new_std_input_args(&argc, &argv);
	}
	if (is_set_option('R')) {
		get_new_recursive_args(&argc, &argv);
	}
	/* (argc, argv) now represents new_file* [ / old_file*] */

	/* Optionally show command line options */
	if (is_set_option('O')) {
		print_options(progname, optlist);
	}

	/* Here the real work starts */

	if (is_set_option('-')) {
		/* Just the lexical scan */
		while (argv[0]) {
			const char *arg = argv[0];
			if (!is_new_old_separator(arg)) {
				Print_Stream(arg);
			}
			argv++;
		}
	}
	else {	/* The works */
		Read_Input_Files(argc, argv);	/* turns files into texts */
		Compare_Files();		/* turns texts into runs */
		if (is_set_option('p')) {
			Print_Percentages();
		} else {
			Retrieve_Runs();
			Print_Runs();
		}
	}

	Free_Text();
	Free_Token_Array();
	if (is_set_option('M')) {
		ReportMemoryStatus(stderr);
	}

	return 0;
}
