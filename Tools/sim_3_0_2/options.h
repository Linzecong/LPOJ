/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: options.h,v 1.12 2016-06-12 13:00:04 dick Exp $
*/

/*	Setting and consulting command line options
*/

enum Value_Type {None, Number, String};
struct option {
	char op_char;		/* char as in call */
	char *op_text;		/* explanatory text */
	enum Value_Type op_type;
	void *op_value;
};

extern void set_option(char ch);
extern int is_set_option(int ch);
extern int do_options(
	const char *progname, const struct option *optlist,
	int argc, const char *argv[]
);
extern void allow_at_most_one_option_out_of(const char *opts);
extern void print_options(const char *progname, const struct option *optlist);
