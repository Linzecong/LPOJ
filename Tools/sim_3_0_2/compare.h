/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: compare.h,v 1.4 2016-04-10 11:19:47 dick Exp $
*/

/*	Compares each new text to the appropriate texts.
	Stores the runs found by passing them to add_run().
	Runs contain references to positions in the input files.
*/

extern void Compare_Files(void);
