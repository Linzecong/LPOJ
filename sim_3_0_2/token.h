/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: token.h,v 2.16 2017-12-11 14:12:38 dick Exp $
*/

/*
	Token interface.
	Since the definition of a token has been a continual source of
	problems, it is now defined as an abstract data type 'Token'.

	There are four classes of tokens:
	1. simple tokens; they derive directly from input characters;
	2. summary tokens; they summarise keywords, etc.;
	3. special tokens: No_Token, IDF, and End_Of_Line;
	4. hashed tokens, segments condensed by idf_hashed().
	The first three classes are called 'regular tokens'.
	There are also a few 'gap' tokens, tokens not produced by the above
	mechanisms, for example 0x100.

	In addition to the type Token and the special tokens, the module
	defines
	1. the constants
		N_REGULAR_TOKENS  number of regular tokens
		N_TOKENS	  total number of tokens, including No_Token
	2. macros for defining summary tokens (with ranges of their parameters):
		CTRL(ch)	ch in 'A'-'~'
		NORM(ch)	ch in '!'-'~'
		MTCT(ch)	ch in 'A'-'~'
		META(ch)	ch in '!'-'~'
	    These restrictions are not checked.
	3. the conversion routines
		Token2int(c)
		int2Token(i)
*/

#include	<stdio.h>
#include	<stdint.h>

#ifndef	_TOKEN_H
#define	_TOKEN_H

#ifdef	lint_test
/* For security we want to distinguish tokens from integers. Lint is not
   good at this, so for checking we use a pointer to a weird data type.
*/
struct for_lint_only {int i;};
typedef struct for_lint_only *Token;
extern int Token_EQ(const Token t1, const Token t2);
#else	/* if normal */
typedef uint16_t Token;
#define	Token_EQ(t1,t2)	(Token2int(t1) == Token2int(t2))
#endif	/* lint_test/normal */

#define	N_TOKENS		(1<<16)
#define	N_REGULAR_TOKENS	(1<<9)

/* Macros for the composition of tokens */		/* range (gaps unused)*/
#define	No_Token	int2Token(0)			/* 0x0000 */
/* 8-bit bytes */					/* 0x0001-0x00FF */
#define	CTRL(ch)	int2Token(0x100|((ch)&0x01F))	/* 0x0101-0x011E */
#define	NORM(ch)	int2Token(0x100|((ch)&0x07F))	/* 0x0121-0x017E */
#define	IDF		int2Token(0x17F)		/* 0x017F */
#define	STR		int2Token(0x180)		/* 0x0180 */
#define	MTCT(ch)	int2Token(0x180|((ch)&0x01F))	/* 0x0181-0x019E */
#define	META(ch)	int2Token(0x180|((ch)&0x07F))	/* 0x01A1-0x01FE */
/* tokens from idf_hashed() */				/* 0x0200-0xFFFE */
#define	End_Of_Line	int2Token(0xFFFF)		/* 0xFFFF */

/* Conversion routines */
#define	Token2int(c)	((int)(c))
#define	int2Token(i)	((Token)(i))

/* Auxiliaries */
#define	is_regular_token(tk)	(Token2int(tk) < N_REGULAR_TOKENS)
extern void fprint_token(FILE *ofile, const Token tk);

#endif	/* _TOKEN_H */
