/*	This file is part of the module ANY_INT.
	Written by Dick Grune, dick@dickgrune.com
	$Id: any_int.h,v 1.4 2017-01-22 14:50:00 Gebruiker Exp $
*/

#ifndef	_ANY_INT_H_
#define _ANY_INT_H_

/*	Printing size_t and very long ints.

   Printing integers using *printf requires specifying the format, which
   requires knowing the exact nature of the integer. But this is not always
   the case, f.e with size_t or extra-long integers for the accumulation of
   size_t values. Some systems use %z as a dedicated format to print size_t,
   but this is not portable since not all compilers know it.

   These problems are solved by introducing the type vlong_[u]int (see below),
   defined as the largest [unsigned] machine int type on the system,
   and routines to convert these to string.
   The resulting string is transient, but up to N_INDEPENDENT_CALLS calls
   can be used simultaneously.

   Since the value is passed to the conversion routines as a typed parameter
   the C compiler does the conversion (actually widening) for you.
*/

/* Public entries */
typedef long long int vlong_int;		/* largest int in the system */
typedef unsigned long long int vlong_uint;	/* largest uint in the system */

/* transient * N_INDEPENDENT_CALLS */
extern const char *any_int2string(vlong_int val, int size);
extern const char *any_uint2string(vlong_uint val, int size);

#endif	/* _ANY_INT_H_ */
