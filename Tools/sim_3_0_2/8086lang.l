%{
/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: 8086lang.l,v 2.2 2017-12-11 14:12:32 dick Exp $
*/

/*
	8086 assembler language front end for the similarity tester.
	Author:	Yaoyao Lei (雷瑶瑶 <lyyfight122@gmail.com>)
	Date:	2017-04-16
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
	{"AAA", NORM('A')},
	{"AAD", NORM('a')},
	{"AAM", META('A')},
	{"AAS", META('a')},
	{"ADC", CTRL('A')},
	{"ADD", MTCT('A')},
	{"AND", NORM('B')},
	{"ASSUME",NORM('b')},
	{"CALL", NORM('C')},
	{"CBW", NORM('c')},
	{"CLC", META('C')},
	{"CLD", META('c')},
	{"CLI", CTRL('C')},
	{"CMC", MTCT('C')},
	{"CMP", META('B')},
	{"CMPS",META('b')},
	{"COMMENT",CTRL('B')},
	{"CWD", MTCT('B')},
	{"DAA", NORM('D')},
	{"DAS", NORM('d')},
	{"DB", META('D')},
	{"DD", META('d')},
	{"DEC", CTRL('D')},
	{"DIV", MTCT('D')},
	{"DQ", NORM('F')},
	{"DT", NORM('f')},
	{"DW", META('F')},
	{"ELSE", NORM('E')},
	{"END", NORM('e')},
	{"ENDIF", META('E')},
	{"ENDP", META('e')},
	{"ENDS", CTRL('E')},
	{"EQU", MTCT('E')},
	{"ESC", META('f')},
	{"EVEN",CTRL('F')},
	{"EXITM",MTCT('F')},
	{"EXTRN",NORM('g')},
	{"GROUP",NORM('G')},
	{"HLT", NORM('H')},
	{"IDIV",NORM('I')},
	{"IF",NORM('i')},
	{"IF1", META('I')},
	{"IF2", META('i')},
	{"IFB", CTRL('I')},
	{"IFDEF",MTCT('I')},
	{"IFDIF",META('G')},
	{"IFE", META('g')},
	{"IFIND", CTRL('G')},
	{"IFNB",MTCT('G')},
	{"IFNDEF",NORM('h')},
	{"IMUL",META('H')},
	{"IN", META('h')},
	{"INC",CTRL('H')},
	{"INCLUDE", MTCT('H')},
	{"INT",NORM('K')},
	{"INTO",NORM('k')},
	{"IRET",META('K')},
	{"IRP",META('k')},
	{"IRPC",CTRL('K')},
	{"JA",NORM('J')},
	{"JB",NORM('j')},
	{"JBE",META('J')},
	{"JC",META('j')},
	{"JCXZ",CTRL('J')},
	{"JE", MTCT('J')},
	{"JG",MTCT('K')},
	{"JGE",CTRL('M')},
	{"JL",MTCT('M')},
	{"JLE",CTRL('N')},
	{"JMP",MTCT('N')},
	{"JNA",META('o')},
	{"JNAE",CTRL('O')},
	{"JNB",MTCT('O')},
	{"JNBE",NORM('Q')},
	{"JNC",NORM('q')},
	{"JNE",META('Q')},
	{"JNG",META('q')},
	{"JNGE",CTRL('Q')},
	{"JNL",MTCT('Q')},
	{"JNLE",META('T')},
	{"JNO",META('t')},
	{"JNP",CTRL('T')},
	{"JNS",MTCT('T')},
	{"JNZ",NORM('U')},
	{"JO",NORM('u')},
	{"JP",META('U')},
	{"JPE",META('u')},
	{"JPO",CTRL('U')},
	{"JS",MTCT('U')},
	{"JZ",NORM('V')},
	{"LAHF",NORM('L')},
	{"LDS", NORM('l')},
	{"LEA", META('L')},
	{"LES", META('l')},
	{"LOCAL",CTRL('L')},
	{"LOCK", MTCT('L')},
	{"LODS", NORM('v')},
	{"LOOP", META('V')},
	{"LOOPE",META('v')},
	{"LOOPNE",CTRL('V')},
	{"LOOPNZ",MTCT('V')},
	{"LOOPZ",NORM('w')},
	{"MACRO",NORM('M')},
	{"MOV", NORM('m')},
	{"MOVS",META('M')},
	{"MUL", META('m')},
	{"NAME",NORM('N')},
	{"NEG", NORM('n')},
	{"NOP", META('N')},
	{"NOT", META('n')},
	{"OR", NORM('O')},
	{"ORG", NORM('o')},
	{"OUT",META('O')},
	{"PAGE", NORM('P')},
	{"POP", NORM('p')},
	{"POPF",META('P')},
	{"PROC", META('p')},
	{"PUBLIC", CTRL('P')},
	{"PURGE", MTCT('P')},
	{"PUSH",META('W')},
	{"RCL", NORM('R')},
	{"RCR", NORM('r')},
	{"RECORD",META('R')},
	{"REP", META('r')},
	{"REPE", CTRL('R')},
	{"REPNE", MTCT('R')},
	{"REPNZ", META('w')},
	{"REPT", CTRL('W')},
	{"REPZ", MTCT('W')},
	{"RET", NORM('X')},
	{"ROL", NORM('x')},
	{"ROR", META('X')},
	{"SAHF", NORM('S')},
	{"SAL", NORM('s')},
	{"SAR", META('S')},
	{"SBB", META('s')},
	{"SCAS",CTRL('S')},
	{"SEGMENT",MTCT('S')},
	{"SHL", META('x')},
	{"SHR", CTRL('X')},
	{"STC", MTCT('X')},
	{"STD", NORM('Y')},
	{"STI", NORM('y')},
	{"STOS",META('Y')},
	{"STRUC",META('y')},
	{"SUB", CTRL('Y')},
	{"SUBTTL",MTCT('Y')},
	{"TEST", NORM('T')},
	{"TITLE", NORM('t')},
	{"WAIT", NORM('W')},
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

/* Language-dependent code */

const char *Subject = "8086 programs";

void
Init_Language(void) {
	if (is_set_option('f') || is_set_option('F'))
		fatal("options -f or -F not applicable in sim_8086");
}

%}

%option	noyywrap

%Start	Comment

Layout		([ \t\r\f])
ASCII95		([\040-\176])

AnyQuoted	(\\.)
StrChar		([^\"\n\\]|{AnyQuoted})
ChrChar		([^\'\n\\]|{AnyQuoted})

SafeComChar	([^*\n])
UnsafeComChar	("*")

Comment		(";".*)

HexDigit	([0-9a-fA-F])
Idf		([A-Za-z_$?@][A-Za-z0-9_$?@]*)

%%


{Comment}"\n"	{		/* comment */
		return_eol();
	}

\"{StrChar}*\"	{			/* strings */
		return_ch('"');
	}

\'{ChrChar}+\'	{			/* characters */
		return_ch('\'');
	}

(0x)?{HexDigit}+("l"|"L")?	{	/* numeral, passed as an identifier */
		return_tk(IDF);
	}

{Idf}	{				/* identifier,non_number beginning*/
		Token tk;

		tk = idf2token(0 /* no hashing */);/* this is for not recognizing different parameter's name*/
		if (!Token_EQ(tk, No_Token)) return_tk(tk);
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
