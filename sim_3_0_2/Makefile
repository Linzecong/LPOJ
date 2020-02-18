#	This file is part of the software similarity tester SIM.
#	Written by Dick Grune, Vrije Universiteit, Amsterdam.
#	$Id: Makefile,v 2.115 2017-12-15 17:23:23 dick Exp $
#

#VERSION="-DVERSION=\"3.0.2 of 2017-12-16\""	# uncomment for public version

#	E N T R Y   P O I N T S

help:
	@echo  'Entry points:'
	@echo  'test:           compile sim_c and run a simple test'
	@echo  ''
	@echo  'binaries:       create all binaries'
	@echo  'exes:           create executables in MSDOS'
	@echo  'install:        install all binaries'
	@echo  ''
	@echo  'view_man:       view sim.pdf'
	@echo  'lint:           lint sim sources'
	@echo  'simsim:         run sim_c on the sim sources'
	@echo  'view_SPC:       view the percentage computation document'
	@echo  'chklat:         do a LaTeX check on the .tex documents'
	@echo  ''
	@echo  'fresh:          remove created files'

#
# When you modify any of the following macros, do 'make clean'
#

# System dependencies
#	=============== including ../lib/sysidf.mk here
#	This file is part of the auxiliary libraries.
#	Written by Dick Grune, dick@dickgrune.com
#	$Id: sysidf.mk,v 1.19 2017-12-08 18:07:17 dick Exp $
#

################################################################
# For UNIX-like systems

SYSTEM =	UNIX
SUBSYSTEM =	SOLARIS

# Locations
DIR =		/home/zs
BINDIR = /usr/bin
MAN1DIR =	/usr/share/man/man1

# Commands
COPY =		cp -p
EXE =		#
LEX =		flex
LN =		ln
ZIP =		zip -o

# File names
NULLFILE =	/dev/null

################################################################
# # For MSDOS + MinGW

# SYSTEM =	MSDOS
# SUBSYSTEM =	MinGW

# # Locations
# DIR =		C:/BIN
# BINDIR =	C:/BIN
# MAN1DIR =	C:/BIN

# # File names
# NULLFILE =	nul

# Commands (cp required, since xcopy cannot handle forward slashes)
COPY =		cp -p
EXE =		.exe
LEX =		flex
LN =		ln
ZIP =		zip -o

################################################################
# General, C compilation:
CC =		gcc -D$(SYSTEM) -D$(SUBSYSTEM)
LINT =		lint -ansi -D$(SYSTEM) -D$(SUBSYSTEM)
LINTFLAGS =	-xh

# General, text:
LATEX =		pdflatex
SHOW_PDF =	pdfview
GROFF =		groff -man
GROFF =		man2pdf

.SUFFIXES:	.1 .3 .pdf

.1.pdf:
		$(GROFF) $<

.3.pdf:
		$(GROFF) $<
#	=============== end of ../lib/sysidf.mk

# Compiling
MEMORY =	-DMEMCHECK -DMEMCLOBBER
CFLAGS =	$(VERSION) $(MEMORY) -O4 # -Dlint -DLIB # for all db active
LIBFLAGS =	#
LINTFLAGS =	-Dlint_test $(MEMORY) -h# -X
LOADFLAGS =	-s#			# strip symbol table
LOADER =	$(CC) $(LOADFLAGS)

# Debugging
CFLAGS +=	-DDEBUG

#	T E S T   P A R A M E T E R S

# Rumen Stevanov test
TEST_LANG =	text
TEST_OPT =	-pPae -r4 -O -t4
TEST_INP =	Contributors/Rumen_Stefanov/new/*.txt

# slash test
TEST_LANG =	text
TEST_OPT =	-r24 -M clang.l pasclang.l "|" textlang.l
TEST_INP =

# -i option test
TEST_LANG =	c
TEST_OPT =	-f -r 20 -R -i <option-i.inp
TEST_INP =	#

# overlap  test, foo^100 vs. foo^150
TEST_LANG =	text
TEST_OPT =	-r50 -p
TEST_OPT =	-r50
TEST_INP =	Test_percentages/foo_100
TEST_INP =	Test_percentages/foo_100 Test_percentages/foo_150

# single file test
TEST_LANG =	c
TEST_OPT =	-r24 -M
TEST_INP =	pass3.c pass3.c	# compares 1st to 2nd, then 2nd to 2nd

# tight match test, foo_100 has exactly 100 tokens
TEST_LANG =	text
TEST_OPT =	-r50
TEST_INP =	Test_percentages/foo_100

# percentage test
TEST_LANG =	c
TEST_OPT =	-puae
TEST_INP =	*.l

# spaced word test
TEST_LANG =	text
TEST_OPT =	-r 5
TEST_INP =	Testfiles/test_seplet

# larger test
TEST_LANG =	text
TEST_OPT =	-r24 -M -puae
TEST_INP = clang.c textlang.c
TEST_INP = textlang.c clang.c javalang.c

# test UTF-8 file names
TEST_LANG =	text
TEST_OPT =	Kor_test/한국어 Kor_test/한국어# 'make' cannot see these files
TEST_INP =	#

# test UTF-8 recursive file name test
TEST_LANG =	text
TEST_OPT =	-R Kor_test
TEST_INP =	#

# test bad UTF-8 text
TEST_LANG =	text
TEST_OPT =	-r12 -MO -w80
TEST_INP =	Testfiles/Korean1_bad.txt Testfiles/Korean1_bad2.txt

# test UTF-8 text
TEST_LANG =	text
TEST_OPT =	-r12 -MO -w80
TEST_INP =	Testfiles/Korean1.txt Testfiles/Korean2.txt

# test
TEST_LANG =	c
TEST_OPT =	-r10 -MO -
TEST_INP =	pass2.c pass1.c

#	M A I N   M O D U L E S

#	Each module (set of programs that together perform some function)
#	has the following sets of files defined for it:
#		_SRC	the C-files from which the object files derive
#		_OBJ	object files
#		_HDR	header files and other include files
#		_GRB	garbage files produced by the module
#
#	(This is a feeble attempt at software-engineering a Makefile.)
#

test:		sim.res stream.res percentages.res version.res
		./sim_$(TEST_LANG)$(EXE) -v


#	B I N A R I E S

BINARIES =	sim_c$(EXE) sim_c++$(EXE) sim_java$(EXE) sim_pasc$(EXE) \
		sim_m2$(EXE) sim_lisp$(EXE) sim_mira$(EXE) sim_text$(EXE) \
		sim_8086$(EXE)

binaries:	$(BINARIES)#		# for *N?X
exes:		binaries#		# for MSDOS
test_exes:	binaries#		# for packCVS

#	A U X I L I A R Y   M O D U L E S

# Common modules:
COM_SRC =	token.c lex.c stream.c text.c tokenarray.c debug.c \
		utf8.c ForEachFile.c fname.c Malloc.c any_int.c
COM_OBJ =	token.o lex.o stream.o text.o tokenarray.o debug.o \
		utf8.o ForEachFile.o fname.o Malloc.o any_int.o
COM_HDR =	token.h lex.h stream.h text.h tokenarray.h debug.h \
		utf8.h ForEachFile.h fname.h Malloc.h any_int.h \
		lang.h \
		sortlist.spc sortlist.bdy system.par

# C files for the abstract modules:
ABS_SRC =	lang.c

# The idf module:
IDF_SRC =	idf.c
IDF_OBJ =	idf.o
IDF_HDR =	idf.h

# The runs package:
RUNS_SRC =	runs.c percentages.c
RUNS_OBJ =	runs.o percentages.o
RUNS_HDR =	runs.h percentages.h

# The main program:
MAIN_SRC =	sim.c options.c newargs.c hash.c compare.c add_run.c \
		pass1.c pass2.c pass3.c
MAIN_OBJ =	sim.o options.o newargs.o hash.o compare.o add_run.o \
		pass1.o pass2.o pass3.o
MAIN_HDR =	sim.h options.h newargs.h hash.h compare.h add_run.h \
		pass1.h pass2.h pass3.h \
		debug.par settings.par

sim.o:	 	Makefile	# because of $(VERSION)

# The similarity tester without the language part:
SIM_SRC =	$(COM_SRC) $(IDF_SRC) $(RUNS_SRC) $(MAIN_SRC)
SIM_OBJ =	$(COM_OBJ) $(IDF_OBJ) $(RUNS_OBJ) $(MAIN_OBJ)
SIM_HDR =	$(COM_HDR) $(IDF_HDR) $(RUNS_HDR) $(MAIN_HDR)


#	L A N G U A G E S

# The properties module:
PROP_SRC =	properties.c
PROP_OBJ =	properties.o
PROP_HDR =	properties.h

# The Generic Language module
#	variable:	GEN_LANG
#	entry point:	sim_gen$(EXE)
#	makes:		sim_$(GEN_LANG)$(EXE)

sim_gen.c:	$(GEN_LANG)lang.l
		$(LEX) -t $(GEN_LANG)lang.l >sim_gen.c

SIM_GEN_SRC =	$(SIM_SRC) $(PROP_SRC) sim_gen.c
SIM_GEN_OBJ =	$(SIM_OBJ) $(PROP_OBJ) sim_gen.o

sim_gen$(EXE):	$(SIM_GEN_OBJ)
		$(LOADER) $(SIM_GEN_OBJ) -o $@
		mv sim_gen$(EXE) sim_$(GEN_LANG)$(EXE)
		rm -f sim_gen.[co]

# The executables:				# using recursive make

LEX_HDR:	options.h token.h properties.h idf.h lex.h lang.h

sim_c$(EXE):	$(SIM_SRC) $(PROP_SRC) clang.l $(LEX_HDR)
		make GEN_LANG=c sim_gen$(EXE)

sim_text$(EXE):	$(SIM_SRC) $(PROP_SRC) textlang.l $(LEX_HDR)
		make GEN_LANG=text sim_gen$(EXE)

sim_c++$(EXE):	$(SIM_SRC) $(PROP_SRC) c++lang.l $(LEX_HDR)
		make GEN_LANG=c++ sim_gen$(EXE)

sim_java$(EXE):	$(SIM_SRC) $(PROP_SRC) javalang.l $(LEX_HDR)
		make GEN_LANG=java sim_gen$(EXE)

sim_pasc$(EXE):	$(SIM_SRC) $(PROP_SRC) pasclang.l $(LEX_HDR)
		make GEN_LANG=pasc sim_gen$(EXE)

sim_m2$(EXE):	$(SIM_SRC) $(PROP_SRC) m2lang.l $(LEX_HDR)
		make GEN_LANG=m2 sim_gen$(EXE)

sim_lisp$(EXE):	$(SIM_SRC) $(PROP_SRC) lisplang.l $(LEX_HDR)
		make GEN_LANG=lisp sim_gen$(EXE)

sim_mira$(EXE):	$(SIM_SRC) $(PROP_SRC) miralang.l $(LEX_HDR)
		make GEN_LANG=mira sim_gen$(EXE)

sim_8086$(EXE):	$(SIM_SRC) $(PROP_SRC) 8086lang.l $(LEX_HDR)
		make GEN_LANG=8086 sim_gen$(EXE)














#	T E S T S

# Some simple tests:
.PHONY:		sim.res percentages.res

sim.res:	sim_$(TEST_LANG)$(EXE) $(TEST_INP)
		./sim_$(TEST_LANG)$(EXE) $(TEST_OPT) $(TEST_INP)

stream.res:	sim_$(TEST_LANG)$(EXE)
		./sim_$(TEST_LANG)$(EXE) -- $(TEST_OPT) $(TEST_INP) >$@
		wc $@ $(TEST_INP)
GARBAGE =	stream.res

PERC_TEST_EXE	=	sim_text$(EXE)
PERC_TEST_FILES =	Test_percentages/foo_100 Test_percentages/foo_150
PERC_TEST_EXE	=	sim_c$(EXE)
PERC_TEST_FILES =	pasclang.l clang.l javalang.l
percentages.res:$(PERC_TEST_EXE) $(PERC_TEST_FILES)
		@echo ''
		./$(PERC_TEST_EXE) -T -p $(PERC_TEST_FILES)
		@echo ''
		./$(PERC_TEST_EXE) -T -pa $(PERC_TEST_FILES)
		@echo ''
		./$(PERC_TEST_EXE) -T -pae $(PERC_TEST_FILES)

version.res:	sim_$(TEST_LANG)$(EXE)
		./sim_$(TEST_LANG)$(EXE) -v


# More simple tests, using the C version only:
simsim:		sim_c$(EXE) $(SIM_SRC) $(PROP_SRC)
		./sim_c$(EXE) -fr 20 $(SIM_SRC) $(PROP_SRC)

# Lint
lint:		$(SIM_SRC) $(PROP_SRC) $(ABS_SRC) \
		$(SIM_HDR) $(PROP_HDR) $(ABS_HDR)
		$(LINT) $(LINTFLAGS) $(SIM_SRC) $(PROP_SRC) $(ABS_SRC)


#	O T H E R   E N T R I E S

# Documentation

view_man:	sim.pdf
		$(SHOW_PDF) sim.pdf

%.pdf:		%.tex
		$(LATEX) $< || log2errmsg <$*.log
		$(LATEX) $<
		$(LATEX) $<

SPC =		Similarity_Percentage_Computation
view_SPC:	$(SPC).pdf
		$(SHOW_PDF) $(SPC).pdf
DOCS +=		$(SPC).pdf

# LaTeX checker
chklat:
		chklat *.tex

# Installation
install_all:	install			# just a synonym
install:	$(MAN1DIR)/sim.1 \
		$(BINDIR)/sim_c$(EXE) \
		$(BINDIR)/sim_text$(EXE) \
		$(BINDIR)/sim_c++$(EXE) \
		$(BINDIR)/sim_java$(EXE) \
		$(BINDIR)/sim_pasc$(EXE) \
		$(BINDIR)/sim_m2$(EXE) \
		$(BINDIR)/sim_lisp$(EXE) \
		$(BINDIR)/sim_mira$(EXE) \
		$(BINDIR)/sim_8086$(EXE)

$(MAN1D)/sim.1:	sim.1
		$(COPY) sim.1 $@

$(BINDIR)/sim_c$(EXE):	sim_c$(EXE)
		$(COPY) sim_c$(EXE) $@

$(BINDIR)/sim_text$(EXE):	sim_text$(EXE)
		$(COPY) sim_text$(EXE) $@

$(BINDIR)/sim_c++$(EXE):	sim_c++$(EXE)
		$(COPY) sim_c++$(EXE) $@

$(BINDIR)/sim_java$(EXE):	sim_java$(EXE)
		$(COPY) sim_java$(EXE) $@

$(BINDIR)/sim_pasc$(EXE):	sim_pasc$(EXE)
		$(COPY) sim_pasc$(EXE) $@

$(BINDIR)/sim_m2$(EXE):	sim_m2$(EXE)
		$(COPY) sim_m2$(EXE) $@

$(BINDIR)/sim_lisp$(EXE):	sim_lisp$(EXE)
		$(COPY) sim_lisp$(EXE) $@

$(BINDIR)/sim_mira$(EXE):	sim_mira$(EXE)
		$(COPY) sim_mira$(EXE) $@

$(BINDIR)/sim_8086$(EXE):	sim_8086$(EXE)
		$(COPY) sim_8086$(EXE) $@

# Clean-up

.PHONY:		clean fresh
clean:
		-rm -f *.o
		-rm -f $(GARBAGE)
		-rm -f *.aux *.log *.out
		-rm -f a.out a.exe sim.txt core mon.out

fresh:		clean
		-rm -f *.exe

#	D E P E N D E N C I E S

# DO NOT DELETE THIS LINE -- make depend depends on it.
ForEachFile.o: ForEachFile.c ForEachFile.h fname.h
Malloc.o: Malloc.c any_int.h Malloc.h
add_run.o: add_run.c sim.h text.h runs.h percentages.h options.h \
 add_run.h
any_int.o: any_int.c any_int.h
compare.o: compare.c sim.h text.h token.h tokenarray.h hash.h \
 properties.h options.h add_run.h compare.h debug.par
count_sim_dup.o: count_sim_dup.c
debug.o: debug.c debug.h
fname.o: fname.c fname.h
hash.o: hash.c system.par debug.par sim.h text.h Malloc.h any_int.h \
 token.h properties.h tokenarray.h options.h hash.h
idf.o: idf.c system.par token.h idf.h
lang.o: lang.c token.h properties.h idf.h lex.h lang.h
lex.o: lex.c lex.h
newargs.o: newargs.c sim.h ForEachFile.h fname.h Malloc.h newargs.h
options.o: options.c sim.h token.h lang.h options.h
pass1.o: pass1.c debug.par sim.h text.h token.h tokenarray.h lang.h \
 options.h pass1.h
pass2.o: pass2.c debug.par sim.h token.h text.h lang.h pass2.h \
 sortlist.bdy
pass3.o: pass3.c system.par debug.par sim.h options.h fname.h text.h \
 token.h runs.h percentages.h pass3.h
percentages.o: percentages.c debug.par sim.h text.h options.h Malloc.h \
 percentages.h sortlist.bdy
properties.o: properties.c sim.h options.h token.h properties.h
runs.o: runs.c sim.h text.h runs.h Malloc.h debug.par sortlist.bdy
sim.o: sim.c system.par settings.par sim.h options.h newargs.h token.h \
 tokenarray.h text.h runs.h hash.h compare.h pass1.h pass2.h pass3.h \
 percentages.h stream.h lang.h Malloc.h any_int.h
stream.o: stream.c system.par sim.h token.h lang.h fname.h stream.h
t.o: t.c
text.o: text.c stream.h Malloc.h text.h
token.o: token.c token.h
tokenarray.o: tokenarray.c sim.h Malloc.h token.h lang.h tokenarray.h
