SRC" plasma.4th"
SRC" conio.4th"
SRC" machid.4th"
LOOKUP CMDSYS 19 + @ PLASMA EXECSYS

: STRINPUT ( STR -- )
  DUP 1+ 255 ACCEPT -TRAILING SWAP C!
;
: STRING CREATE 256 ALLOT DOES> ; ( JUST ALLOCATE THE BIGGEST STRING POSSIBLE )

STRING DEST
STRING FILELIST

0 0 40 24 VIEWPORT
HOME
12 SPACES INVERSETEXT
." PLASMA HD INSTALL"
NORMALTEXT CR CR
0 1 40 23 VIEWPORT
." Enter destination " DEST STRINPUT
DEST C@ 0= ?ABORT" Destination required"
." Copying install files to " DEST (.") CR
FILELIST " -R PL* CMD* SYS AUTORUN " STRCPY DEST STRCAT
" COPY" SWAP LOADMOD
FILELIST " HDINSTALL2.4TH " STRCPY DEST STRCAT " /HDINSTALL.4TH" STRCAT
" COPY" SWAP LOADMOD

." Stage 2..." CR
0 0 40 24 VIEWPORT

DEST SETPFX DROP
" PLASMA.SYSTEM" EXECSYS
