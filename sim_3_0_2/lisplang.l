%{
/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: lisplang.l,v 2.23 2017-12-11 14:12:35 dick Exp $
*/

/*
	LISP language front end for the similarity tester.
	Author:	Gertjan Akkerman <akkerm@cs.vu.nl>
	Date:	Thu, 9 Apr 87 11:15:23 MDT
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
	{"append",	NORM('a')},
	{"append1",	NORM('b')},
	{"atom",	NORM('t')},
	{"car",		NORM('h')},
	{"cdr",		NORM('t')},
	{"cond",	NORM('c')},
	{"cons",	NORM('s')},
	{"defun",	NORM('u')},
	{"do",		NORM('d')},
	{"eq",		NORM('e')},
	{"equal",	NORM('e')},		/* See eq */
	{"for",		NORM('f')},
	{"if",		NORM('i')},
	{"list",	NORM('l')},
	{"nconc",	NORM('n')},
	{"rplaca",	NORM('A')},
	{"rplacd",	NORM('D')}
};

/* Token sets for properties module */
const Token Non_Finals[] = {
	NORM('('),
	NORM('['),
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
	No_Token
};
const Token Closers[] = {
	NORM(')'),
	NORM(']'),
	No_Token
};

/* Language-dependent code */

const char *Subject = "Lisp programs";

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

IdfChar		([-!#$%&*+,/0-9:;<=>?@A-Z\\^_`a-z{}~])

EscIdf		(({IdfChar}|\\.)+)
QuotIdf		("|"[^\|\n]*"|")
Idf		({EscIdf}|{QuotIdf})

%%

";".*$	{				/* comment */
	}

\"{StrChar}*\"	{			/* strings */
		return_ch(STR);
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
