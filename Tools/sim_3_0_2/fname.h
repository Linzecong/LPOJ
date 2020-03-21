/*	This file is part of the auxiliaries library.
	Written by Dick Grune, dick@dickgrune.com
	$Id: fname.h,v 1.14 2017-12-13 17:41:34 Gebruiker Exp $
*/

/*	Support for Unicode file names */

/*
   Under Windows file names are internally kept in UTF-16 and if they contain
   non-ASCII codes they have to be presented in UTF-16. Under *NIX systems
   file names are in UTF-8, just as all other strings.

   To accommodate non-ASCII file names on various platforms, this file defines
   the types

      Fchar             file name character
      Dir_t		struct for accessing a directory
      Dirent_t		struct for accessing a directory entry

   and the functions

      Dir_t* Opendir(const Fchar*);
      Dirent_t* Readdir(Dir_t*);
      int Closedir(Dir_t*);

      Fchar *Fnamecpy(Fchar *dest, Fchar *source);
      Fchar *Fnamecat(Fchar*, const Fchar*);
      int Fnamelen(const Fchar*);
      int Fnamecmp(const Fchar*, const Fchar*);

      int Stat(const Fchar *fn, struct stat *st);
      FILE *Fopen(const Fchar *fn, const char *rb);
         The stream is still char*!
      int Fclose(FILE*);

      const char *Fname2str(const Fchar *fn);
      const Fchar *str2Fname(const char *s);
         The result of these two routines is transient: is is good only until
	 the next call.

   The only way to obtain a UTF-16 file name is through readdir; the command
   line arguments are in ASCII. So a program can be adapted by replacing
       DIR by Dir_t, and
       struct dirent by Dirent_t.
   Compiling and correcting using the above replacements until there are no
   more errors or warnings will then yield an UTF-16 compatible program, as
   far as the input file names concerned. Output is done in UTF-8.

   For details about UTF-16 see fname.c.
*/

#ifndef	_FNAME_H_
#define _FNAME_H_

/* lint cannot handle the weird code Windows throws at it, so even under
   Windows we claim to have UTF-8
*/
#ifdef	MSDOS
#define	IS_UTF_16
#endif
#ifdef	lint
#undef	IS_UTF_16
#endif

#ifdef	IS_UTF_16			/* file names in UTF-16 */

#define	_UNICODE

#include	<tchar.h>

#include	<sys/stat.h>
#include	<dirent.h>

/* Private entries */
typedef _TCHAR Fchar;
typedef _WDIR Dir_t;
typedef struct _tdirent Dirent_t;

/* Public entries */
#define	Opendir		_topendir
#define	Closedir	_tclosedir
#define	Readdir		_treaddir

#define	Fnamecpy	wcscpy
#define	Fnamecat	wcscat
#define	Fnamelen	(int)wcslen
#define	Fnamecmp	wcscmp

extern const char *Fname2str(const Fchar *fn);		/* transient! */
extern const Fchar *str2Fname(const char *s);		/* transient! */

extern int Stat(const Fchar *fn, struct stat *st);
extern FILE *Fopen(const Fchar *fn, const char *rb);/* stream is still char* */
#define	Fclose		fclose

#else	/* not MSDOS */			/* file names are in UTF-8 */

#include	<sys/stat.h>
#include	<dirent.h>
#include	<string.h>

/* life is simple */
/* Public entries */
typedef char Fchar;

#define	Fnamecpy	strcpy
#define	Fnamecat	strcat
#define	Fnamelen	strlen
#define	Fnamecmp	strcmp

#define	Fname2str(fn)	(fn)
#define	str2Fname(s)	(s)

#define	Stat(fn,st)	stat(fn,st)

typedef DIR Dir_t;
typedef struct dirent Dirent_t;
#define	Opendir		opendir
#define	Closedir	closedir
#define	Readdir		readdir
#define	Fopen		fopen
#define	Fclose		fclose

#endif	/* MSDOS */

#endif	/* _FNAME_H_ */
