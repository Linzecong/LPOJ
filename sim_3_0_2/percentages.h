/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: percentages.h,v 1.7 2017-12-03 09:55:24 dick Exp $
*/

extern void add_to_percentages(
    const struct text *txt0, const struct text *txt1, size_t size);
extern void Print_Percentages(void);
