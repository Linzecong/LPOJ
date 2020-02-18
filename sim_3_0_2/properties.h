/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: properties.h,v 2.2 2017-12-11 14:12:37 dick Exp $
*/

/*	The module properties.[ch] administers language properties.
	It supplies the following routines:
	    void Init_Language_Properties()
	        accepts language properties and stores them; see below;
	    int May_Be_Start_Of_Run() and
	    size_t Best_Run_Size()
	        allow proposed runs the be judged and/or modified.

	Two sets of properties are maintained:
	1.  sets of Tokens that cannot be the beginning or end of a run;
	    these are applied to all runs;
	2.  sets of matching openers and closers (parentheses); these are
	    applied only when the -f flag is given.

	The *lang.l designer is required to define four token sets,
	represented as Token set[] and terminated by No_Token:
	    Token Non_Finals[]
	        tokens that may not end a run;
	    Token Non_Initials[]
	        tokens that may not start a run;
	    Token Openers[]
	        openers of parentheses that must balance in functions;
	    Token Closers[]
	        the corresponding closers, in the same order.
	These must be passed to Init_Language_Properties(), in the above order.
	A non-applicable item may be passed as 0.
*/

extern void Init_Language_Properties(
    const Token Non_Finals[], const Token Non_Initials[],
    const Token Openers[], const Token Closers[]
); /* note the order of the arguments: Non_Finals ~ Openers, etc. */
extern int May_Be_Start_Of_Run(Token tk);
extern size_t Best_Run_Size(const Token *str, size_t size);
