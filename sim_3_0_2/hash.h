/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: hash.h,v 1.6 2017-12-11 14:12:34 dick Exp $
*/

/*	Creating and consulting forward_reference[], used to speed up
	the Longest Substring Algorithm.
*/

extern void Make_Forward_References(void);
extern void Free_Forward_References(void);
/* with circularity check: */
extern size_t Forward_Reference(size_t i, size_t i0);
