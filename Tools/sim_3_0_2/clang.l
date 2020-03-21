%{
/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: clang.l,v 2.28 2017-12-11 14:12:33 dick Exp $
*/

/*
	C language front end for the similarity tester.
	Author:	Dick Grune <dick@cs.vu.nl>
	Date:	1986-05-18
*/

#include	"options.h"
#include	"token.h"
#include	"properties.h"
#include	"idf.h"
#include	"lex.h"
#include	"lang.h"

/* General language front end data */
Token lex_token;
size_t lex_nl_cnt;
size_t lex_tk_cnt;
size_t lex_non_ASCII_cnt;

/* Language-dependent data */

/* Data for module idf */

static const struct idf ppcmd[] = {
	{"define",	META('d')},
	{"else",	META('e')},
	{"endif",	META('E')},
	{"if",		META('i')},
	{"ifdef",	META('I')},
	{"ifndef",	META('x')},
	{"include",	MTCT('I')},
	{"line",	META('l')},
	{"undef",	META('u')}
};

static const struct idf reserved[] = {
	{"auto",	NORM('a')},
	{"break",	NORM('b')},
	{"case",	NORM('c')},
	{"char",	NORM('C')},
	{"continue",	CTRL('C')},
	{"default",	NORM('d')},
	{"do",		NORM('D')},
	{"double",	CTRL('D')},
	{"else",	NORM('e')},
	{"enum",	NORM('E')},
	{"extern",	CTRL('E')},
	{"float",	NORM('f')},
	{"for",		NORM('F')},
	{"goto",	NORM('g')},
	{"if",		NORM('i')},
	{"int",		NORM('I')},
	{"long",	NORM('l')},
	{"register",	No_Token},
	{"return",	NORM('r')},
	{"short",	NORM('s')},
	{"sizeof",	NORM('S')},
	{"static",	CTRL('S')},
	{"struct",	META('s')},
	{"switch",	META('S')},
	{"typedef",	NORM('t')},
	{"union",	NORM('u')},
	{"unsigned",	NORM('U')},
	{"void",	No_Token},
	{"while",	NORM('w')}
};

/* Special treatment of identifiers */

static Token
idf2token(int hashing) {
	Token tk;

	tk = idf_in_list(yytext, reserved, sizeof reserved, IDF);
	if (Token_EQ(tk, IDF) && hashing) {
		/* return a one-Token hash code */
		tk = idf_hashed(yytext);
	}
	return tk;
}

/* Token sets for properties module */
static const Token Non_Finals[] = {
	IDF,		/* identifier */
	NORM('{'),
	NORM('('),
	NORM('a'),	/* auto */
	NORM('b'),	/* break */
	NORM('c'),	/* case */
	NORM('C'),	/* char */
	CTRL('C'),	/* continue */
	NORM('d'),	/* default */
	NORM('D'),	/* do */
	CTRL('D'),	/* double */
	NORM('E'),	/* enum */
	CTRL('E'),	/* extern */
	NORM('f'),	/* float */
	NORM('F'),	/* for */
	NORM('g'),	/* goto */
	NORM('i'),	/* if */
	NORM('I'),	/* int */
	NORM('l'),	/* long */
	NORM('r'),	/* return */
	NORM('s'),	/* short */
	CTRL('S'),	/* static */
	META('s'),	/* struct */
	META('S'),	/* switch */
	NORM('t'),	/* typedef */
	NORM('u'),	/* union */
	NORM('U'),	/* unsigned */
	NORM('w'),	/* while */
	No_Token
};

static const Token Non_Initials[] = {
	NORM(')'),
	NORM('}'),
	NORM(';'),
	No_Token
};

static const Token Openers[] = {
	NORM('{'),
	NORM('('),
	NORM('['),
	No_Token
};

static const Token Closers[] = {
	NORM('}'),
	NORM(')'),
	NORM(']'),
	No_Token
};

/* Language-dependent code */

const char *Subject = "C programs";

void
Init_Language(void) {
	Init_Language_Properties(Non_Finals, Non_Initials, Openers, Closers);
}

/* UTF-8 bytes in strings and comment are absorbed in patterns starting
   with [^...]. Non-ASCII chars outside strings or comments are counted in
   lex_non_ASCII_cnt.
*/

%}

%option	noyywrap

%Start	Comment

Layout		([ \t\r\f])
ASCII95		([\040-\176])

AnyQuoted	(\\.)
StrChar		([^\"\n\\]|{AnyQuoted})
ChrChar		([^\'\n\\]|{AnyQuoted})

StartComment	("/*")
EndComment	("*/")
SafeComChar	([^*\n])
UnsafeComChar	("*")

MSComment	("//"{MSCommentChar}*)
MSCommentChar	([^\n])

HexDigit	([0-9a-fA-F])
Idf		([A-Za-z_][A-Za-z0-9_]*)

%%

{StartComment}	{
		/*	We do not have one single pattern to match a comment
			(although one can be written), for two reasons.
			The matched string might overflow lex-internal buffers
			like yysbuf and yytext; and the pattern would be very
			complicated and impair maintainability.
			So we break up the string into safe chunks and keep
			track of where we are in a start condition <Comment>.
		*/
		BEGIN Comment;
	}

<Comment>{SafeComChar}+	{		/* safe comment chunk */
	}

<Comment>{UnsafeComChar}	{	/* unsafe char, read one by one */
	}

<Comment>"\n"		{		/* to break up long comments */
		return_eol();
	}

<Comment>{EndComment}	{		/* end-of-comment */
		BEGIN INITIAL;
	}

{MSComment}	{			/* ignore */
	}

\"{StrChar}*\"	{			/* strings */
		return_ch(STR);
	}

\'{ChrChar}+\'	{			/* characters */
		return_ch('\'');
	}

^#{Layout}*include.*	{		/* ignore #include lines */
	}

^#{Layout}*{Idf}	{		/* a preprocessor line */
		char *idf = yytext+1;

		/* skip layout in front of preprocessor identifier */
		while (*idf == ' ' || *idf == '\t') {
			idf++;
		}
		return_tk(idf_in_list(idf, ppcmd, sizeof ppcmd, NORM('#')));
	}

(0x)?{HexDigit}+("l"|"L")?	{	/* numeral, passed as an identifier */
		return_tk(IDF);
	}

{Idf}/"("	{			/* identifier in front of ( */
		Token tk;

		tk = idf2token(is_set_option('F'));
		if (!Token_EQ(tk, No_Token)) return_tk(tk);
	}

{Idf}	{				/* identifier */
		Token tk;

		tk = idf2token(0 /* no hashing */);
		if (!Token_EQ(tk, No_Token)) return_tk(tk);
	}

\;	{				/* semicolon, conditionally ignored */
		if (is_set_option('f')) return_ch(yytext[0]);
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
