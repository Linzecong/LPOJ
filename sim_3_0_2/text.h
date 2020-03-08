/*	This file is part of the software similarity tester SIM.
	Written by Dick Grune, Vrije Universiteit, Amsterdam.
	$Id: text.h,v 1.13 2017-12-09 17:18:03 dick Exp $
*/

/*	Implements the access to the lexical scanner.
	Additionally, the module tries to save newline information,
	anticipating a second scan which is interested in this
	information only.
*/

/* The input files are called "texts" */

struct text {
	const char *tx_fname;	/* the file name */
	size_t tx_start;	/* index of first token in Token_Array[]
				   belonging to the text */
	size_t tx_limit;	/* index of first position in Token_Array[]
				   not belonging to the text */
	int tx_EOL_terminated;	/* Boolean */
	struct position *tx_pos;/* list of positions in this file that are
				   part of a chunk; sorted and updated by
				   Pass 2
				*/
};

struct position {
	/* position of first and last token of a chunk */
	struct position *ps_next;
	int ps_type;		/* first = 0, last = 1, for debugging */
	size_t ps_tk_cnt;	/* in tokens; set by add_run()
				   in Read_Input_Files() */
	size_t ps_nl_cnt;	/* same, in line numbers;set by Retrieve_Runs(),
				   used by Print_Runs(), to report line numbers
				*/
};

extern struct text *Text;		/* Text[], one for each input file */
extern int Number_of_Texts;		/* number of text files;
					   this includes the new/old separator
					   if present
					*/
extern int Number_of_New_Texts;		/* number of *new* text files */

extern void Init_Text(int nfiles);
extern int Open_Text(struct text *txt);
extern int Next_Text_Token_Obtained(void);
extern void Close_Text(void);
extern void Free_Text(void);
