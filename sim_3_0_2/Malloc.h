/*	This file is part of the checked memory manager MALLOC.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: Malloc.h,v 1.16 2017-12-13 17:41:34 Gebruiker Exp $
*/

#ifndef	_MALLOC_H_
#define _MALLOC_H_

/*****
The files Malloc.[ch] provide several functionalities:

- checking for "out of memory":			to simplify programming
- allocating memory using a routine new(type):	"     "        " "
- clobbering freshly allocated memory:		to obtain safer programs
- checking for freeing of unallocated blocks:	"     "     "      "
- reporting on memory usage:			to obtain cleaner programs
- detecting memory leaks:			"    "       "       "

The module defines several sets of routines:

1.  void *Malloc(size_t s)
    void *Calloc(size_t n, size_t s)
    void *Realloc(void *p, size_t s)
    void Free(void *p)

    These routines act like checking versions of their Unix counterparts,
    except that they never return NULL; upon out-of-memory an error message
    is given on standard error, showing the file name and the line number
    of the call.
    Since in almost all cases there is nothing more intelligent to do, this
    is almost always adequate, and makes for simpler and safer programming.

2.  void *TryMalloc(size_t s)
    void *TryCalloc(size_t n, size_t s)
    void *TryRealloc(void *p, size_t s)
    void OutOfMemoryExit(const char *msg)

    In those rare cases that the program *can* continue when out of memory, the
    Try... routines can be used; they act exactly like those in group 1,
    except that they return NULL when out of memory.
    A call of OutOfMemoryExit(msg) gives an out-of-memory error message,
    displaying the message msg and some memory usage information, and
    terminating the program.

3.  T *new(T)
    T *try_new(T)
    char *new_string(const char *s)

    A call of new(T), with T any type, yields a pointer of type T* to a block
    of type T, allocated using Malloc(). A call of try_new(T) does the same
    but returns NULL when out of memory.
    A call of new_string(s), with s a string, yields a pointer to a copy of s,
    allocated using Malloc(); it is equivalent to strdup() except that it uses
    Malloc(). A call of try_new_string(s) does the same but returns NULL when
    out of memory.

4.  void ReportMemoryStatus(FILE *f)

    Produces a compacted list of allocated but not yet freed blocks on the
    stream f, with information about where they were allocated.
    This is useful to get insight into memory use and abuse.

5.  void MemClobber(void *p, size_t size)

    When Malloc.c is compiled with -DMEMCLOBBER, it clobbers all newly allocated
    memory from Malloc() and Realloc() just after allocation, and all freed
    memory just before freeing it.  An area is clobbered by overwriting it with
    a wacky bit pattern. This is done in the hope that improper use of memory
    will cause some evident error somewhere.

    The routine that performs the clobbering, MemClobber(void *p, size_t size),
    is available regardless of the -DMEMCLOBBER compilation option. It can be
    used to create comparison patterns.

Notes:
*    Compiled with any of the -DMEM... flags, Malloc will also produce run-time
     error messages for multiple Free()s of the same block, and Realloc()s on
     not-allocated blocks. It then allows the program to continue.

*    The system consumes hardly any time and is fast enough to be kept active
     at all times.
*****/

#include	<stdio.h>		/* for FILE */
#include	<stdlib.h>		/* for size_t */

/* Blocking malloc.h */
#define	malloc(s)	you_are_using_the_Malloc_package_so_use_Malloc
#define	calloc(n,s)	you_are_using_the_Malloc_package_so_use_Calloc
#define	realloc(p,s)	you_are_using_the_Malloc_package_so_use_Realloc
#define	free(p)		you_are_using_the_Malloc_package_so_use_Free


/* Private entries */
extern void *_mreg_malloc(int chk, size_t size, const char *fname, int l_nmb);
extern void *_mreg_calloc(int chk, size_t n, size_t size, const char *fname, int l_nmb);
extern void *_mreg_realloc(int chk, void *addr, size_t size, const char *fname, int l_nmb);
extern void _mreg_free(void *addr, const char *fname, int l_nmb);
extern void _out_of_memory(
		const char *msg, const char *fname, int l_nmb, size_t size);

extern char *_new_string(int chk, const char *s, const char *fname, int l_nmb);

/* Public entries */
#define	Malloc(s)	(_mreg_malloc(1, (s), __FILE__, __LINE__))
#define	Calloc(n,s)	(_mreg_calloc(1, (n), (s), __FILE__, __LINE__))
#define	Realloc(p,s)	(_mreg_realloc(1, (void *)(p), (s), __FILE__, __LINE__))
#define	Free(p)		(_mreg_free((void *)(p), __FILE__, __LINE__))

#define	TryMalloc(s)	(_mreg_malloc(0, (s), __FILE__, __LINE__))
#define	TryCalloc(n,s)	(_mreg_calloc(0, (n), (s), __FILE__, __LINE__))
#define	TryRealloc(p,s)	(_mreg_realloc(0, (void *)(p), (s), __FILE__, __LINE__))
#define	OutOfMemoryExit(s) _out_of_memory((s), __FILE__, __LINE__, 0)

#define	new(type)	((type *)Malloc(sizeof (type)))
#define	try_new(type)	((type *)TryMalloc(sizeof (type)))
#define	new_string(s)	(_new_string(1, (s), __FILE__, __LINE__))
#define	try_new_string(s)(_new_string(0, (s), __FILE__, __LINE__))

extern void ReportMemoryStatus(FILE *f);
extern void MemClobber(void *p, size_t size);

#endif	/* _MALLOC_H_ */
