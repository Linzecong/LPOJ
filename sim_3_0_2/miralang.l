%{
/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: miralang.l,v 1.17 2017-12-11 14:12:35 dick Exp $
*/

/*
	Miranda language front end for the similarity tester.
	Author:	Emma Norling (ejn@cs.mu.oz.au)
	Date:	Nov 1998
*/

#include	"token.h"
#include	"properties.h"
#include	"lex.h"
#include	"lang.h"

/* General language front end data */
Token lex_token;
size_t lex_nl_cnt;
size_t lex_tk_cnt;
size_t lex_non_ASCII_cnt;

/* Language-dependent data */
#include	"idf.h"

static const struct idf reserved[] = {
	{"abstype",	NORM('a')},
	{"bool",	NORM('b')},
	{"char",	NORM('c')},
	{"const",	META('c')},
	{"div",		NORM('d')},
	{"False",	NORM('F')},
	{"if",		NORM('i')},
	{"mod",		NORM('m')},
	{"num",		NORM('n')},
	{"otherwise",	NORM('o')},
	{"readvals",	NORM('r')},
	{"show",	NORM('s')},
	{"sys_message",	META('s')},
	{"True",	NORM('T')},
	{"type",	NORM('t')},
	{"where",	NORM('w')},
	{"with",	META('w')}
};

/* Token sets for properties module */
const Token Non_Finals[] = {
	NORM('('),
	NORM('['),
	NORM('='),
	No_Token
};
const Token Non_Initials[] = {
	NORM(')'),
	NORM(']'),
	No_Token
};
const Token Openers[] = {
	NORM('('),
	NORM('['),
	NORM('='),
	No_Token
};
const Token Closers[] = {
	NORM(')'),
	NORM(']'),
	No_Token
};

/* Language-dependent code */

const char *Subject = "Miranda programs";

void
Init_Language(void) {
	Init_Language_Properties(Non_Finals, Non_Initials, Openers, Closers);
}

%}

%option	noyywrap

%Start	Comment

Layout		([ \t\r\f])
ASCII95		([\040-\176])

AnyQuoted	(\\.)
StrChar		([^\"\n\\]|{AnyQuoted})
ChrChar		([^\'\\]|{AnyQuoted})

Idf		([A-Za-z][A-Za-z0-9_\']*)

%%

"||".*$	{				/* comment */
	}

\"{StrChar}*\"	{			/* strings */
		return_ch(STR);
	}

\'{ChrChar}\'	{			/* characters */
		return_ch('\'');
	}

\%{Layout}*include.*	{		/* skip %include line */
	}

\%{Layout}*insert.*	{		/* skip %insert line */
	}

{Idf}	{				/* identifier */
		return_tk(idf_in_list(yytext, reserved, sizeof reserved, IDF));
	}

\n	{				/* count newlines */
		return_eol();
	}

{Layout}	{			/* ignore layout */
	}

{ASCII95}	{			/* copy other text */
		return_ch(yytext[0]);
	}

.	{				/* count non-ASCII chars */
		lex_non_ASCII_cnt++;
	}

%%

/* More language-dependent code */

void
yystart(void) {
	BEGIN INITIAL;
}
