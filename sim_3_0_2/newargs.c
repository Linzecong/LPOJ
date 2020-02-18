/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: newargs.c,v 2.12 2017-12-13 20:20:47 dick Exp $
*/

#include	<stdio.h>

#include	"sim.h"
#include	"ForEachFile.h"
#include	"Malloc.h"
#include	"newargs.h"

#define	ARGS_INCR	1024
static char *args;
static size_t args_free;
static size_t args_size;

static void
init_args(void) {
	args = 0;
	args_free = 0;
	args_size = 0;
}

static void
add_char_to_args(char ch) {
	if (args_free == args_size) {
		/* allocated array is full; increase its size */
		size_t new_size = args_size + ARGS_INCR;
		char *new_args = (char *)Realloc(
			 (char *)args, sizeof (char *) * new_size
		);
		args = new_args, args_size = new_size;
	}

	/* now we are sure there is room enough */
	args[args_free++] = ch;
}

static void
add_string_to_args(const char *fn) {
	while (*fn) {
		add_char_to_args(*fn++);
	}
	add_char_to_args('\n');
}

static char *
std_input(void) {
	/* in the form (name \n)* \0 */

	/* get all of standard input */
	int ch;
	int last_char = '\n';

	while (ch = getchar(), ch != EOF) {
		/* omit duplicate layout (= empty name) */
		if (last_char == '\n' && ch == '\n') continue;

		add_char_to_args((char)ch);
		last_char = ch;
	}
	add_char_to_args('\0');

	/* make sure the result conforms to the form above  */
	if (args[args_free-2] != '\n')
		fatal("standard input not terminated with newline");

	return args;
}

static int
n_names(const char *s) {
	int cnt = 0;

	while (*s) {
		if (*s == '\n') {
			cnt++;
		}
		s++;
	}
	return cnt;
}

static const char **
new_argv(int argc, char *args) {
	/* converts the layout in args to \0, and constructs an argv list */
	const char **argv =
		(const char **)Malloc((size_t)(argc+1) * sizeof (char *));
	char *p = args;
	char last_char = '\n';

	argc = 0;
	while (*p) {
		if (last_char == '\n') {
			/* here a new name starts */
			argv[argc++] = p;
		}
		last_char = *p;
		if (*p == '\n') {
			*p = '\0';
		}
		p++;
	}
	argv[argc] = 0;

	return argv;
}

void
get_new_std_input_args(int *argcp, const char **argvp[]) {
	init_args();
	char *n_args = std_input();
	int argc = n_names(n_args);
	const char **argv = new_argv(argc, n_args);

	*argcp = argc, *argvp = argv;
}

static int
register_file(const Fchar *fn, const char *msg, const struct stat *fs) {
	if (msg) {
		fprintf(stderr, "could not handle file %s: %s\n", fn, msg);
		return 0;
	}

	if (	/* it is a non-empty regular file */
		S_ISREG(fs->st_mode) && fs->st_size > 0
	) {
		add_string_to_args(Fname2str(fn));
	}
	return 1;
}

static char *
recursive_args(int argc, const char *argv[]) {
	if (argc == 0) {
		ForEachFile(str2Fname("."), register_file);
	}
	else {
		int i;

		for (i = 0; i < argc; i++) {
			const char *arg = argv[i];
			if (is_new_old_separator(arg)) {
				add_string_to_args(arg);
			} else {
				ForEachFile(str2Fname(arg), register_file);
			}
		}
	}
	add_char_to_args('\0');

	return args;
}

void
get_new_recursive_args(int *argcp, const char **argvp[]) {
	init_args();
	char *n_args = recursive_args(*argcp, *argvp);
	int argc = n_names(n_args);
	const char **argv = new_argv(argc, n_args);

	*argcp = argc, *argvp = argv;
}
