%{
/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: javalang.l,v 1.22 2017-12-11 14:12:34 dick Exp $
*/

/*
	Java language front end for the similarity tester.
	Author:	Dick Grune <dick@cs.vu.nl>
	Date:	Nov. 1997
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

static const struct idf reserved[] = {
	{"abstract",	NORM('a')},
	{"boolean",	NORM('b')},
	{"break",	NORM('B')},
	{"byte",	CTRL('B')},
	{"case",	NORM('c')},
	{"catch",	NORM('C')},
	{"char",	CTRL('C')},
	{"class",	META('c')},
	{"continue",	META('C')},
	{"default",	NORM('d')},
	{"do",		NORM('D')},
	{"double",	CTRL('D')},
	{"else",	NORM('e')},
	{"extends",	NORM('E')},
	{"false",	NORM('g')},	/* Boolean literal */
	{"final",	NORM('f')},
	{"finally",	NORM('F')},
	{"float",	CTRL('F')},
	{"for",		META('f')},
	{"if",		NORM('i')},
	{"implements",	NORM('I')},
	{"import",	CTRL('I')},
	{"instanceof",	META('i')},
	{"int",		META('I')},
	{"interface",	MTCT('I')},
	{"long",	NORM('l')},
	{"native",	NORM('n')},
	{"new",		NORM('N')},
	{"null",	CTRL('N')},	/* null literal */
	{"package",	NORM('p')},
	{"private",	NORM('P')},
	{"protected",	CTRL('P')},
	{"public",	META('p')},
	{"return",	NORM('r')},
	{"short",	NORM('s')},
	{"static",	NORM('S')},
	{"super",	CTRL('S')},
	{"switch",	META('s')},
	{"synchronized",META('S')},
	{"this",	NORM('t')},
	{"throw",	NORM('T')},
	{"throws",	CTRL('T')},
	{"true",	META('t')},	/* Boolean literal */
	{"void",	NORM('v')},
	{"volatile",	NORM('V')},
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
const Token Non_Finals[] = {
	IDF,		/* identifier */
	NORM('{'),
	NORM('('),
	NORM('a'),	/* abstract */
	NORM('b'),	/* boolean */
	NORM('B'),	/* break */
	CTRL('B'),	/* byte */
	NORM('c'),	/* case */
	NORM('C'),	/* catch */
	CTRL('C'),	/* char */
	META('c'),	/* class */
	META('C'),	/* continue */
	NORM('d'),	/* default */
	NORM('D'),	/* do */
	CTRL('D'),	/* double */
	NORM('e'),	/* else */
	NORM('E'),	/* extends */
	NORM('f'),	/* final */
	NORM('F'),	/* finally */
	CTRL('F'),	/* float */
	META('f'),	/* for */
	NORM('i'),	/* if */
	NORM('I'),	/* implements */
	CTRL('I'),	/* import */
	META('i'),	/* instanceof */
	META('I'),	/* int */
	MTCT('I'),	/* interface */
	NORM('l'),	/* long */
	NORM('n'),	/* native */
	NORM('N'),	/* new */
	NORM('p'),	/* package */
	NORM('P'),	/* private */
	CTRL('P'),	/* protected */
	META('p'),	/* public */
	NORM('r'),	/* return */
	NORM('s'),	/* short */
	NORM('S'),	/* static */
	CTRL('S'),	/* super */
	META('s'),	/* switch */
	META('S'),	/* synchronized */
	NORM('T'),	/* throw */
	CTRL('T'),	/* throws */
	NORM('v'),	/* void */
	NORM('V'),	/* volatile */
	NORM('w'),	/* while */
	No_Token
};
const Token Non_Initials[] = {
	NORM(')'),
	NORM('}'),
	NORM(';'),
	No_Token
};
const Token Openers[] = {
	NORM('{'),
	NORM('('),
	NORM('['),
	No_Token
};
const Token Closers[] = {
	NORM('}'),
	NORM(')'),
	NORM(']'),
	No_Token
};

/* Language-dependent code */

const char *Subject = "Java programs";

void
Init_Language(void) {
	Init_Language_Properties(Non_Finals, Non_Initials, Openers, Closers);
}

%}

%option	noyywrap

%Start	Comment

Layout		([ \t\r\f])
ASCII95		([\040-\176])
PseudoUTF8	([\201-\377])

AnyQuoted	(\\.)
StrChar		([^\"\n\\]|{AnyQuoted})
ChrChar		([^\'\n\\]|{AnyQuoted})

StartComment	("/*")
EndComment	("*/")
SafeComChar	([^*\n])
UnsafeComChar	("*")

SingleLineCom	("//".*)

HexDigit	([0-9a-fA-F])
Idf		(([A-Za-z_][A-Za-z0-9_]*)|{PseudoUTF8})

%%

{StartComment}	{
		/*	We do not have one single pattern to match a comment
			(although one can be written), for two reasons.
			The matched string might overflow lex-internal buffers
			like yysbuf and yytext; and the pattern would be very
			complicated and overtax lex.
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

(0x)?{HexDigit}+("l"|"L")?	{      	/* numeral, passed as an identifier */
		return_tk(IDF);
	}

"import"{Layout}[^;]*;	{		/* import statement; ignore */
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
