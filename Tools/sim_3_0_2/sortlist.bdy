/*
	Module:	Sort Linked Lists
	Author:	dick@dickgrune.com (Dick Grune, Amstelveen)
	Version: 2015-01-18

Description:
	This is the implementation part of a generic routine that sorts
	linked lists.

Instantiation:
	See sortlist.spc
*/

#ifndef	_SORT_EXTERN_DEFINED
static
#endif
void
SORT_NAME(struct SORT_STRUCT **l_hook) {
	/* by split-sort-merge */
	struct SORT_STRUCT *lst = *l_hook;
	if (lst == 0) return;			/* the empty list is sorted */
	if (lst->SORT_NEXT == 0) return;	/* a 1-element list is sorted */

	/* There are at least two elements; split them into two sublists. */
	struct SORT_STRUCT *q0 = 0, *q1 = 0;	/* starts of the sublists */
	struct SORT_STRUCT **q_hook[2];		/* append hooks for the lists */
	q_hook[0] = &q0, q_hook[1] = &q1;
	int q_cnt = 0;				/* pertinemt sublist pointer */

	while (lst) {
		/* Detach the head element */
		struct SORT_STRUCT *l = lst;
		lst = lst->SORT_NEXT;
		l->SORT_NEXT = 0;

		/* and append it to the pertinent sublist. */
		*q_hook[q_cnt] = l;
		q_hook[q_cnt] = &l->SORT_NEXT;
		q_cnt = 1 - q_cnt;		/* switch pertinent sublist */
	}

	/* Sort recursively. */
	SORT_NAME(&q0);
	SORT_NAME(&q1);

	/* Merge. */
	*l_hook = 0;
	while (q0 || q1) {
		/* determine the list with the smallest head element */
		struct SORT_STRUCT **h_hook = (
			  q0 == 0 ? &q1 :
			  q1 == 0 ? &q0 :
			  SORT_BEFORE((q0), (q1)) ? &q0 : &q1
		);
		/* detach head element */
		struct SORT_STRUCT *l = *h_hook;
		*h_hook = (*h_hook)->SORT_NEXT;
		l->SORT_NEXT = 0;

		/* append l to l_hook */
		*l_hook = l;
		l_hook = &l->SORT_NEXT;
	}
}
