/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: lang.c,v 2.12 2017-12-11 14:12:34 dick Exp $
*/

/*
	This is a dummy implementation of the  module 'lang'.
	Its actual implementation derives from the pertinent *lang.l file.
*/

#include	"token.h"

#include	"properties.h"
#include	"idf.h"
#include	"lex.h"
#include	"lang.h"


FILE *yyin;

int
yylex(void) {
#ifdef	lint
	(void)May_Be_Start_Of_Run(0);
	(void)Best_Run_Size(0, 0);
	(void)idf_in_list(0, 0, 0, 0);
	(void)idf_hashed(0);
	(void)lower_case(0);
#endif
	return 0;
}

void
yystart(void) {
#ifdef	lint
	Init_Language_Properties(0, 0, 0, 0);
#endif
}

Token lex_token;
size_t lex_nl_cnt;
size_t lex_tk_cnt;
size_t lex_non_ASCII_cnt;

const char *Subject;

void
Init_Language(void) {
}
