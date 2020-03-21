%{
/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: m2lang.l,v 2.26 2017-12-11 14:12:35 dick Exp $
*/

/*
	Modula-2 language front end for the similarity tester.
	Author:	Dick Grune <dick@cs.vu.nl>
	Date:	1986-12-02
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

/*	Most Modula-2 programs start with a number of IMPORTs that look
	very similar from program to program.  These are skipped by ignoring
	the reserved words IMPLEMENTATION, DEFINITION, MODULE, IMPORT
	and FROM, having a flag skip_imports, and start reacting only
	at the first non-ignored reserved word.

	Also, the nesting comments require a state variable.
*/

/* Additional state variables, set in yystart() */
static int skip_imports;
static int comment_level;

/* Data for module idf */

static const struct idf reserved[] = {
	{"AND",		NORM('&')},
	{"ARRAY",	NORM('A')},
	{"BEGIN",	NORM('{')},
	{"BY",		NORM('B')},
	{"CASE",	NORM('c')},
	{"CONST",	NORM('C')},
	{"DEFINITION",	No_Token},
	{"DIV",		NORM('/')},
	{"DO",		NORM('D')},
	{"ELSE",	NORM('e')},
	{"ELSIF",	NORM('e')},
	{"END",		NORM('}')},
	{"EXIT",	NORM('E')},
	{"EXPORT",	CTRL('E')},
	{"FOR",		NORM('F')},
	{"FROM",	No_Token},
	{"IF",		NORM('i')},
	{"IMPLEMENTATION",	No_Token},
	{"IMPORT",	No_Token},
	{"IN",		NORM('I')},
	{"LOOP",	NORM('l')},
	{"MOD",		NORM('%')},
	{"MODULE",	No_Token},
	{"NOT",		NORM('~')},
	{"OF",		No_Token},
	{"OR",		NORM('O')},
	{"POINTER",	NORM('p')},
	{"PROCEDURE",	NORM('P')},
	{"QUALIFIED",	NORM('q')},
	{"RECORD",	NORM('r')},
	{"REPEAT",	NORM('R')},
	{"RETURN",	CTRL('r')},
	{"SET",		NORM('s')},
	{"THEN",	No_Token},
	{"TO",		NORM('t')},
	{"TYPE",	NORM('T')},
	{"UNTIL",	NORM('u')},
	{"VAR",		NORM('v')},
	{"WHILE",	NORM('w')},
	{"WITH",	NORM('W')},
};

static const struct idf standard[] = {
	{"ABS",		META('a')},
	{"ADDRESS",	META('A')},
	{"ALLOCATE",	MTCT('A')},
	{"BITSET",	META('b')},
	{"BOOLEAN",	META('B')},
	{"CAP",		META('c')},
	{"CARDINAL",	META('C')},
	{"CHAR",	MTCT('C')},
	{"CHR",		META('x')},
	{"DEALLOCATE",	META('d')},
	{"DEC",		META('D')},
	{"EXCL",	META('e')},
	{"FALSE",	META('f')},
	{"FLOAT",	META('F')},
	{"HALT",	META('h')},
	{"HIGH",	META('H')},
	{"INC",		META('i')},
	{"INCL",	META('I')},
	{"INTEGER",	MTCT('I')},
	{"LONGCARD",	META('L')},
	{"LONGINT",	META('L')},
	{"LONGREAL",	META('L')},
	{"MAX",		META('m')},
	{"MIN",		META('M')},
	{"NEWPROCESS",	META('n')},
	{"NIL",		META('N')},
	{"ODD",		META('o')},
	{"ORD",		META('O')},
	{"PROC",	META('p')},
	{"REAL",	META('r')},
	{"SIZE",	META('s')},
	{"SYSTEM",	META('S')},
	{"TRANSFER",	META('t')},
	{"TRUE",	META('T')},
	{"TRUNC",	MTCT('T')},
	{"VAL",		META('v')},
	{"WORD",	META('w')}
};

/* Special treatment of identifiers */

static Token
idf2token(int hashing) {
	Token tk;

	/* the token can be on two lists, reserved and standard */
	tk = idf_in_list(yytext, reserved, sizeof reserved, IDF);

	/* is it one of the keywords to be ignored? */
	if (Token_EQ(tk, No_Token)) return tk;

	/*	The statement below is a significant comment
		on the value of state variables.
	*/
	if (!Token_EQ(tk, IDF)) {
		/* reserved word, stop the skipping */
		skip_imports = 0;
	}
	else {
		/* it is an identifier but not a reserved word */
		if (skip_imports) {
			/* skip it */
			tk = 0;
		}
		else {
			/* look further */
			tk = idf_in_list(yytext, standard, sizeof standard, IDF);
			if (Token_EQ(tk, IDF) && hashing) {
				/* return a one-Token hash code */
				tk = idf_hashed(yytext);
			}
		}
	}
	return tk;
}

/* Token sets for properties module */
const Token Non_Finals[] = {
	IDF,		/* identifier */
	NORM('{'),	/* also BEGIN */
	NORM('('),
	NORM('['),
	NORM('A'),	/* ARRAY */
	NORM('c'),	/* CASE */
	NORM('C'),	/* CONST */
	NORM('E'),	/* EXIT */
	NORM('F'),	/* FOR */
	NORM('i'),	/* IF */
	NORM('l'),	/* LOOP */
	NORM('p'),	/* POINTER */
	NORM('P'),	/* PROCEDURE */
	NORM('r'),	/* RECORD */
	NORM('R'),	/* REPEAT */
	CTRL('R'),	/* RETURN */
	NORM('s'),	/* SET */
	NORM('T'),	/* TYPE */
	NORM('v'),	/* VAR */
	NORM('w'),	/* WHILE */
	NORM('W'),	/* WITH */
	No_Token
};
const Token Non_Initials[] = {
	NORM('}'),
	NORM(')'),
	NORM(']'),
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

const char *Subject = "Modula-2 programs";

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
QuStrChar	([^\"\n\\]|{AnyQuoted})
ApoStrChar	([^\'\n\\]|{AnyQuoted})

StartComment	("(*")
EndComment	("*)")
SafeComChar	([^*\n])
UnsafeComChar	("*")

HexDigit	([0-9a-fA-F])
Idf		([A-Za-z][A-Za-z0-9_]*)

%%

{StartComment}	{			/* See clang.l */
		/*	Lex itself is incapable of handling Modula-2's
			nested comments. So let's help it a bit.
		*/
		if (comment_level == 0) {
			BEGIN Comment;
		}
		comment_level++;
	}

<Comment>{SafeComChar}+	{		/* safe comment chunk */
	}

<Comment>{UnsafeComChar}	{	/* unsafe char, read one by one */
	}

<Comment>"\n"		{		/* to break up long comments */
		return_eol();
	}

<Comment>{EndComment}	{		/* end-of-comment */
		comment_level--;
		if (comment_level == 0) {
			BEGIN INITIAL;
		}
	}

\"{QuStrChar}*\"	{		/* quoted strings */
		return_ch(STR);
	}

\'{ApoStrChar}*\'	{		/* apostrophed strings */
		return_ch(STR);
	}

{HexDigit}+("B"|"C"|"H")?	{	/* numeral, passed as an identifier */
		return_tk(IDF);
	}

"END"{Layout}*{Idf}	{		/* ignore identifier after END */
		Token tk =
		      idf_in_list("END", reserved, sizeof reserved, No_Token);
		if (!Token_EQ(tk, No_Token)) return_tk(tk);
	}

{Idf}/"("	{			/* identifier in front of ( */
		Token tk = idf2token(is_set_option('F')/* hashing option */);
		if (!Token_EQ(tk, No_Token)) return_tk(tk);
	}

{Idf}	{				/* identifier */
		Token tk = idf2token(0 /* no hashing */);
		if (!Token_EQ(tk, No_Token)) return_tk(tk);
	}

"<>"	{				/* <>, special equivalence */
		return_ch('#');
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
		if (!skip_imports) return_ch(yytext[0]);
	}

.	{				/* count non-ASCII chars */
		lex_non_ASCII_cnt++;
	}

%%

/* More language-dependent code */

void
yystart(void) {
	skip_imports = 1;
	comment_level = 0;
	BEGIN INITIAL;
}
