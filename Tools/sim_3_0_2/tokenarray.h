/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: tokenarray.h,v 1.7 2016-04-30 18:53:33 dick Exp $
*/

/* Interface for the token storage */
extern void Init_Token_Array(void);
extern void Store_Token(Token tk);
extern void Free_Token_Array(void);
extern size_t Token_Array_Length(void);	/* also first free token position */

extern Token *Token_Array;

