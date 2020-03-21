/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: lex.h,v 2.14 2017-12-06 16:43:49 dick Exp $
*/

/* Macros for use in the *lang.l files */
/* All returns in *lang.l files go through these macros which set
   lex_token, lex_tk_cnt, and lex_nl_cnt.
*/
#define	return_tk(tk)	{lex_tk_cnt++; lex_token = (tk); return 1;}
#define	return_ch(ch)	{lex_tk_cnt++; lex_token = int2Token((int)(ch)); return 1;}
#define	return_eol()	{lex_nl_cnt++; lex_token = End_Of_Line; return 1;}
