/*	This file is part of the checked memory manager MALLOC.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: Malloc.c,v 1.26 2017-12-08 18:07:16 Gebruiker Exp $
*/

#include	<stdio.h>
#include	<stdlib.h>
#include	<unistd.h>
#include	<string.h>

#include	"any_int.h"
#include	"Malloc.h"
/* make malloc.h available */
#undef	malloc
#undef	calloc
#undef	realloc
#undef	free


/*Library module source prelude */
#undef	_MALLOC_CODE_
#ifndef	lint
#define	_MALLOC_CODE_
#endif
#ifdef	LIB
#define	_MALLOC_CODE_
#endif

#ifdef	_MALLOC_CODE_

/* Library module source code */

#undef	new
#define	new		use_my_new	/* don't call Malloc in Malloc.c */
#define	my_new(type)	((type *)malloc(sizeof (type)))

/* All output goes through designated files, so we block printf, etc. */
#undef	printf
#define	printf	use_fprintf
#undef	putchar
#define	putchar	use_fprintf

static size_t restricted_balance = 0;	/* to simulate out-of-memory */

							/* ADMINISTRATION */
static vlong_uint total = 0;
static vlong_uint balance = 0;
static vlong_uint max = 0;

struct alloc {	/* corresponds to an allocated block */
	struct alloc *next;
	const char *addr;
	size_t size;
	const char *fname;
	int l_nmb;
};

#define	HASH_SIZE	16381		/* largest prime under 2^16 */
static struct alloc *alloc_bucket[HASH_SIZE];
#define	alloc_bucket_for(x)	alloc_bucket[((unsigned int)(x)%HASH_SIZE)]

							/* MEMORY STATUS */

struct call {	/* summarizes all the allocations at a call in the program */
	struct call *next;
	const char *fname;
	int l_nmb;
	unsigned int n_blocks;
	int var_size;	/* all blocks have the same size or not */
	size_t size;	/* !var_size: the one size; var_size: sum of sizes */
};

static struct call *
compacted_calls(void) {
	struct call *list_of_calls = 0;
	int i;

	for (i = 0; i < HASH_SIZE; i++) {
		struct alloc *al = alloc_bucket[i];

		while (al) {
			struct call *cl = list_of_calls;

			/* try to find a call entry for this program location */
			while (cl) {
				if (	cl->fname == al->fname
				&&	cl->l_nmb == al->l_nmb
				)	break;
				cl = cl->next;
			}

			if (cl) {
				/* this is known call; update */
				if (cl->var_size) {
					cl->size += al->size;
				}
				else if (cl->size != al->size) {
					/* switch to var_size */
					cl->var_size = 1;
					cl->size =
					    cl->n_blocks*cl->size + al->size;
				}
				cl->n_blocks++;
			}
			else {	/* this is a new call */
				cl = my_new(struct call);
				cl->fname = al->fname;
				cl->l_nmb = al->l_nmb;
				cl->n_blocks = 1;
				cl->var_size = 0;
				cl->size = al->size;

				/* prepend to list_of_calls */
				cl->next = list_of_calls;
				list_of_calls = cl;
			}

			al = al->next;
		}
	}

	return list_of_calls;
}

static int
number_of_calls(const struct call *cl) {
	int res = 0;

	while (cl != 0) {
		res++;
		cl = cl->next;
	}

	return res;
}

static void
fprintloc(FILE *out, const char *fname, int l_nmb) {
	fprintf(out, "\"%s\", line %d: ", fname, l_nmb);
}

static void
report_actual_call(FILE *out, const struct call *cl) {
	fprintloc(out, cl->fname, cl->l_nmb);
	fprintf(out, "still allocated: %d block%s of size ",
		cl->n_blocks, (cl->n_blocks == 1 ? "" : "s")
	);
	if (cl->var_size) {
		/* cl->size is the sum of the sizes */
		size_t av = (cl->size+cl->n_blocks/2) / cl->n_blocks;
		fprintf(out, "%s on average", any_uint2string(av, 0));
		if (cl->n_blocks > 1) {
			fprintf(out, " = %s", any_uint2string(cl->size, 0));
		}
	}
	else {
		/* cl->size is the single size */
		fprintf(out, "%s", any_uint2string(cl->size, 0));
		if (cl->n_blocks > 1) {
			vlong_uint all = cl->size*cl->n_blocks;
			fprintf(out, " = %s", any_uint2string(all, 0));
		}
	}
	fprintf(out, "\n");
}

static void
report_actual_calls(FILE *out) {
	const struct call *cl = compacted_calls();	/* allocates cl */
	int n_calls = number_of_calls(cl);

	if (n_calls == 0) return;

	fprintf(out, "There %s %d call position%s with unreclaimed memory:\n",
		(n_calls == 1 ? "is" : "are"),
		n_calls,
		(n_calls == 1 ? "" : "s")
	);

	while (cl) {
		report_actual_call(out, cl);
		struct call *next_cl = cl->next;
		free((void *)cl);			/* frees cl */
		cl = next_cl;
	}
}

void
ReportMemoryStatus(FILE *out) {
	if (out == 0) out = stderr;
	report_actual_calls(out);

	fprintf(out, "Total memory allocated = %s", any_uint2string(total, 0));
	fprintf(out, ", max. allocated = %s", any_uint2string(max, 0));
	fprintf(out, ", still allocated = %s", any_uint2string(balance, 0));
	fprintf(out, "\n");
	fflush(out);
}

void	/* used in external macros */
_out_of_memory(const char *msg, const char *fname, int l_nmb, size_t size) {
	fprintloc(stderr, fname, l_nmb);
	fprintf(stderr, "OUT OF MEMORY");
	if (msg) {
		fprintf(stderr, ": %s", msg);
	}
	if (size != 0) {
		fprintf(stderr, ", requested size = %s bytes",
			any_uint2string(size, 0));
	}
	fprintf(stderr, "\n");
	fflush(stderr);
	ReportMemoryStatus(stderr);
	exit(1);
}

							/* MALLOC */

static void
register_alloc(char *addr, size_t size, const char *fname, int l_nmb) {
	/* registers the allocation of a block in the administration */
	struct alloc *new;
	struct alloc **al_hook = &alloc_bucket_for(addr);

	if (addr == 0) return;

	new = my_new(struct alloc);
	new->addr = addr;
	new->size = size;
	new->fname = fname;		/* no need to copy fname */
	new->l_nmb = l_nmb;
	new->next = *al_hook;
	*al_hook = new;

	total += size;
	balance += size;
	if (balance > max) {
		max = balance;
	}
}

void
MemClobber(void *p, size_t size) {
	unsigned char *s = (unsigned char *)p;
	size_t i;

	for (i = 0; i < size; i++) {
		s[i] = 0125;		/* 0101 0101 */
	}
}

void *
_mreg_malloc(int chk, size_t size, const char *fname, int l_nmb) {
	void *res;

	if (restricted_balance && balance + size > restricted_balance) {
		res = 0;
	} else {
		res = malloc(size);
	}

	if (res == 0) {
		if (chk) {
			_out_of_memory(0, fname, l_nmb, size);
			/*NOTREACHED*/
		}
		return res;
	}

	register_alloc(res, size, fname, l_nmb);

#ifdef	MEMCLOBBER
	MemClobber((char *)res, size);
#endif	/* MEMCLOBBER */

	return res;
}

char *
_new_string(int chk, const char *s, const char *fname, int l_nmb) {
	return strcpy((char *)(_mreg_malloc(chk, strlen(s)+1, fname, l_nmb)),
		      s);
}

							/* CALLOC */

void *
_mreg_calloc(int chk, size_t n, size_t size, const char *fname, int l_nmb) {
	void *res;

	if (restricted_balance && balance + n*size > restricted_balance) {
		res = 0;
	} else {
		res = calloc(n, size);
	}

	if (res == 0) {
		if (chk) {
			_out_of_memory(0, fname, l_nmb, n*size);
			/*NOTREACHED*/
		}
		return res;
	}

	register_alloc(res, n*size, fname, l_nmb);

	return res;
}

							/* REALLOC */

static struct alloc **
pointer_to_alloc_for(const char *addr) {
	struct alloc **al_hook = &alloc_bucket_for(addr);

	while (*al_hook) {
		if ((*al_hook)->addr == addr) break;
		al_hook = &(*al_hook)->next;
	}

	return al_hook;
}

static size_t
register_free(char *addr) {
	/* registers the freeing of a block */
	struct alloc **old_p = pointer_to_alloc_for(addr);
	struct alloc *old = *old_p;

	if (old == 0) return (size_t) -1;
	size_t old_size = old->size;

	*old_p = old->next;
	free((void *)old);

	balance -= old_size;
	return old_size;
}

void *
_mreg_realloc(int chk, void *addr, size_t size, const char *fname, int l_nmb) {
	void *res;
	size_t old_size = register_free(addr);

	/* we report first, because the realloc() below may cause a crash */
	if (	/* we are not reallocating address 0, which is allowed */
		addr != 0
	&&	/* the address was never handed out before */
		old_size == (size_t) -1
	) {
		fprintloc(stderr, fname, l_nmb);
		fprintf(stderr, ">>>> unallocated block reallocated <<<<\n");
		fflush(stderr);
	}

	if (restricted_balance && balance + size > restricted_balance) {
		res = 0;
	} else {
		res = realloc(addr, size);
	}

	if (res == 0) {
		if (chk) {
			_out_of_memory(0, fname, l_nmb, size);
			/*NOTREACHED*/
		}
		return res;
	}

	register_alloc(res, size, fname, l_nmb);

#ifdef	MEMCLOBBER
	if (old_size > 0 && size > old_size) {
		MemClobber(((char *)res)+old_size, size-old_size);
	}
#endif	/* MEMCLOBBER */

	return res;
}

							/* FREE */

/* ARGSUSED */
void
_mreg_free(void *addr, const char *fname, int l_nmb) {
	size_t old_size = register_free(addr);

	/* we report first, because the free() below may cause a crash */
	if (old_size == (size_t) -1) {
		fprintloc(stderr, fname, l_nmb);
		fprintf(stderr, ">>>> unallocated block freed ");
		fprintf(stderr, "or multiple free of allocated block <<<<\n");
		fflush(stderr);
	}
	else {
#ifdef	MEMCLOBBER
	MemClobber((char *)addr, old_size);
#endif	/* MEMCLOBBER */
	}
	free(addr);
}

/* End library module source code */
#endif	/* _MALLOC_CODE_ */

#ifdef	lint
static void
satisfy_lint(void *x) {
	void *v;

	v = _mreg_malloc(0, 0, 0, 0);
	v = _new_string(0, 0, 0, 0);
	v = _mreg_calloc(0, 0, 0, 0, 0);
	v = _mreg_realloc(0, 0, 0, 0, 0);
	_mreg_free(x, 0, 0);

	OutOfMemoryExit(0);
	ReportMemoryStatus(0);
	MemClobber(v, 0);

	satisfy_lint(v);
}
#endif	/* lint */
