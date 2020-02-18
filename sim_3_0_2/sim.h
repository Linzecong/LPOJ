/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: sim.h,v 2.22 2016-05-29 15:23:16 dick Exp $
*/

#include	<stdio.h>

extern const char *Version;

extern int Min_Run_Size;
extern int Page_Width;
extern FILE *Output_File;
extern FILE *Debug_File;

extern const char *Token_Name;		/* possibly modified in *lang.l */
extern int Threshold_Percentage;

/* Service routines */
extern int is_new_old_separator(const char *s);
extern const char *size_t2string(size_t s);
extern void fatal(const char *msg);

/* All output goes through designated files, so we block printf, etc. */
#undef	printf
#define	printf	use_fprintf
#undef	putchar
#define	putchar	use_fprintf
