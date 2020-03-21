/*
	Module:	Sort Linked Lists
	Author:	dick@cs.vu.nl (Dick Grune @ Vrije Universiteit, Amsterdam)
	Version: 2015-01-18

Description:
	This is the specification part of a generic routine that sorts linked
	lists. The elements in the list are structs, each of which carries a
	pointer to the next element.

Specification:
	The module supplies:
	-	a routine void SORT_NAME(struct SORT_STRUCT **listhook)
		where 'listhook' is a pointer to the location that holds the
		pointer to the list to be sorted. Upon return, the list will
		be sorted, and the pointer updated.
		The routine will be defined static when instantiated inline.

Instantiation, inline:
	For each struct list type T, specify:
	-	a definition of SORT_STRUCT, the struct name of the linked
		structs;
	-	a definition of SORT_NAME, the name of the resulting sort
		routine;
	-	a definition of a routine
			int SORT_BEFORE(
				struct SORT_STRUCT *v, struct SORT_STRUCT *w
			)
		or a definition
			#define SORT_BEFORE((v,w)
		which yields non-zero if v is to be sorted before w;
	-	a definition of a field selector SORT_NEXT which names the
		field that points to the next struct SORT_STRUCT in the list.
	-	#include	"sortlist.bdy"

Instantiation, separate:
	For each struct list type T, create a file sort_T.h which contains at
	least:
	-	a definition of SORT_STRUCT, the struct name of the linked
		structs;
	-	a definition of SORT_NAME, the name of the resulting sort
		routine;
	-	#include	"sortlist.spc"

	This file sort_T.h is to be included in all files that use the routine
	SORT_NAME.

	For each struct list type T, create a file sort_T.c which contains at
	least:
	-	#include	"sort_T.h"
	-	a definition of a routine or definition SORT_BEFORE as
		described above;
	-	a definition of a field selector SORT_NEXT which names the
		field that points to the next struct SORT_STRUCT in the list;
	-	#include	"sortlist.bdy"

	This file sort_T.c compiles into the module object for SORT_STRUCT.

Implementation:
	Recursive split-sort-merge.
*/

extern void SORT_NAME(struct SORT_STRUCT **);
#define	_SORT_EXTERN_DEFINED
