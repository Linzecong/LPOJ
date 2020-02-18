/*	This file is part of the auxiliaries library.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: ForEachFile.h,v 1.14 2017-01-22 14:49:59 Gebruiker Exp $
*/

#ifndef	_FOREACHFILE_H_
#define _FOREACHFILE_H_

#include	"fname.h"
#include	<sys/types.h>
#include	<sys/stat.h>

/****
* ForEachFile(const Fchar *Fn, int (*proc)(...):
  Each file or directory reachable from Fn is passed to the procedure proc(),
  which is declared as:

    int proc(const Fchar *Fn, const char *msg, const struct stat *fs):
	the file or directory Fn has been reached;
	if msg != NULL, an error prevails the text of which is *msg;
	otherwise fs points to the stat buffer for Fn.

	If Fn is a file or the argument of ForEachFile(), the return value of
	proc() is ignored; if it is a directory but not the argument of
	ForEachFile() and the return value is 0, the directory is not visited
	further, and files and directories in it are not reported.

	Basically if proc() always returns 1, all reachable files are reported;
	if it always returns 0, only the local files and directories are
	reported. But finer control is possible.

* proc() is not called with the directory names "." or ".." unless it is the
  first argument to ForEachFile().

* MAX_FILE_NAME_LENGTH is the maximum length of the file name Fn, including
  directories.
****/

/* Public entries */
#define	MAX_FILE_NAME_LENGTH	1024		/* maximum file name length */

extern void ForEachFile(
	const Fchar *Fname,
	int (*proc)(const Fchar *, const char *, const struct stat *)
);

/* avoid awkward dir test */
extern int is_dirstat(const struct stat *fs);
extern int is_Dirname(const Fchar *Fn);
extern int is_Admin_Dirname(const Fchar *Fn);	/* !=0 for "." and ".." */

#endif	/* _FOREACHFILE_H_ */
