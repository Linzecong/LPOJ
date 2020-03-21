%{
/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: c++lang.l,v 2.8 2017-12-11 14:12:33 dick Exp $
*/

/*
	C++ language front end for the similarity tester.
	Based on C language front end written by Dick Grune <dick@cs.vu.nl>
	Author:	Dick Grune <dick@cs.vu.nl>
	Modified by: Evin Murphy, UCD Dublin, Ireland
	Date:	2017-03-15
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
	{"define",		META('d')},
	{"elif",		META('e')},
	{"else",		META('E')},
	{"endif",		META('n')},
	{"error",		META('r')},
	{"if",			META('i')},
	{"ifdef",		META('I')},
	{"ifndef",		META('x')},
	{"include",		MTCT('I')},
	{"line",		META('l')},
	{"pragma",		META('p')},
	{"undef",		META('u')}
};

static const struct idf reserved[] = {
	{"and",			NORM('a')},
	{"and_eq",		NORM('A')},
	{"asm",			CTRL('A')},
	{"auto",		META('a')},
	{"bitand",		NORM('b')},
	{"bitor",		NORM('B')},
	{"bool",		CTRL('B')},
	{"break",		META('b')},
	{"case",		NORM('c')},
	{"char",		NORM('C')},
	{"class",		CTRL('C')},
	{"const",		META('c')},
	{"const_cast",		META('C')},
	{"continue",		MTCT('C')},
	{"default",		NORM('d')},
	{"delete",		NORM('D')},
	{"do",			CTRL('D')},
	{"double",		META('D')},
	{"dynamic_cast",	MTCT('D')},
	{"else",		NORM('e')},
	{"enum",		NORM('E')},
	{"explicit",CTRL('E')},
	{"extern",		MTCT('E')},
	{"false",		NORM('f')},
	{"float",		NORM('F')},
	{"for",			CTRL('F')},
	{"friend",		META('f')},
	{"goto",		NORM('g')},
	{"if",			NORM('i')},
	{"inline",		NORM('I')},
	{"int",			CTRL('I')},
	{"long",		NORM('l')},
	{"mutable",		NORM('m')},
	{"namespace",		NORM('n')},
	{"new",			NORM('N')},
	{"not",			CTRL('N')},
	{"not_eq",		META('N')},
	{"operator",		NORM('o')},
	{"or",			NORM('O')},
	{"or_eq",		CTRL('O')},
	{"private",		NORM('p')},
	{"protected",		NORM('P')},
	{"public",		CTRL('P')},
	{"register",		No_Token},
	{"reinterpret_cast",	NORM('r')},
	{"return",		NORM('R')},
	{"short",		NORM('s')},
	{"signed",		NORM('S')},
	{"sizeof",		CTRL('S')},
	{"static",		META('s')},
	{"static_cast",		META('S')},
	{"struct",		MTCT('S')},
	{"switch",		META('w')},
	{"template",		NORM('t')},
	{"this",		NORM('T')},
	{"throw",		CTRL('T')},
	{"true",		META('t')},
	{"try",			META('T')},
	{"typedef",		MTCT('T')},
	{"typeid",		NORM('y')},
	{"typename",		NORM('z')},
	{"union",		NORM('u')},
	{"unsigned",		NORM('U')},
	{"using",		CTRL('U')},
	{"virtual",		NORM('v')},
	{"void",		NORM('V')},
	{"while",		NORM('w')},
	{"xor",			NORM('x')},
	{"xor_eq",		NORM('X')}
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
	IDF,			/* identifier */
	NORM('{'),
	NORM('('),
	NORM('a'),		/* and */
	NORM('A'),		/* and_eq */
	CTRL('A'),		/* asm */
	META('a'),		/* auto */
	NORM('b'),		/* bitand */
	NORM('B'),		/* bitor */
	CTRL('B'),		/* bool */
	META('b'),		/* break */
	NORM('c'),		/* case */
	NORM('C'),		/* char */
	CTRL('C'),		/* class */
	META('c'),		/* const */
	META('C'),		/* const_cast */
	MTCT('C'),		/* continue */
	NORM('d'),		/* default */
	NORM('D'),		/* delete */
	CTRL('D'),		/* do */
	META('D'),		/* double */
	MTCT('D'),		/* dynamic_cast */
	NORM('e'),		/* else */
	NORM('E'),		/* enum */
	CTRL('E'),		/* explicit */
	MTCT('E'),		/* extern */
	NORM('F'),		/* float */
	CTRL('F'),		/* for */
	META('f'),		/* friend */
	NORM('g'),		/* goto */
	NORM('i'),		/* if */
	NORM('I'),		/* inline */
	CTRL('I'),		/* int */
	NORM('l'),		/* long */
	NORM('m'),		/* mutable */
	NORM('n'),		/* namespace */
	NORM('N'),		/* new */
	CTRL('N'),		/* not */
	META('N'),		/* not_eq */
	NORM('o'),		/* operator */
	NORM('O'),		/* or */
	CTRL('O'),		/* or_eq */
	NORM('p'),		/* private */
	NORM('P'),		/* protected */
	CTRL('P'),		/* public */
	NORM('r'),		/* reinterpret_cast */
	NORM('R'),		/* return */
	NORM('s'),		/* short */
	NORM('S'),		/* signed */
	CTRL('S'),		/* sizeof */
	META('s'),		/* static */
	META('S'),		/* static_cast */
	MTCT('S'),		/* struct */
	META('w'),		/* switch */
	NORM('t'),		/* template */
	CTRL('T'),		/* throw */
	META('T'),		/* try */
	MTCT('T'),		/* typedef */
	NORM('y'),		/* typeid */
	NORM('z'),		/* typename */
	NORM('u'),		/* union */
	NORM('U'),		/* unsigned */
	CTRL('U'),		/* using */
	NORM('v'),		/* virtual */
	NORM('V'),		/* volatile */
	CTRL('V'),		/* void */
	NORM('w'),		/* while */
	NORM('x'),		/* xor */
	NORM('X'),		/* xor_eq */
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

const char *Subject = "C++ programs";

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
ChrChar		([^\'\n\\]|{AnyQuoted})

StartComment	("/*")
EndComment	("*/")
SafeComChar	([^*\n])
UnsafeComChar	("*")

SingleLineCom	("//".*)

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

{SingleLineCom}"\n"	{		/* single-line comment */
		return_eol();
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

(0x)?{HexDigit}+("l"|"L")?	{      	/* numeral, passed as an identifier */
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
