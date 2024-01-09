LOOKUP HRFORTH  ( HGR page 1 reserved )
LOOKUP HR2FORTH ( HGR page 1 and 2 reserved )
OR NOT ABORT" Must run with HRFORTH."

SRC" PLASMA.4TH"
SRC" CONIO.4TH"
SRC" HGRLIB.4TH"

 5 VARIABLE BALLCLR
10 VARIABLE BALLX
20 VARIABLE BALLY
10 VARIABLE OLDX
20 VARIABLE OLDY
 1 VARIABLE INCX
 1 VARIABLE INCY

: BEEP 30 10 TONE ;

: BOOP 10 30 TONE ;

: MOVEBALL
  BALLX @ 0=    IF INCX @ NEGATE INCX ! BEEP THEN
  BALLX @ 279 = IF INCX @ NEGATE INCX ! BEEP THEN
  BALLY @ 0=    IF INCY @ NEGATE INCY ! BOOP THEN
  BALLY @ 191 = IF INCY @ NEGATE INCY ! BOOP THEN
  INCX @ BALLX +!
  INCY @ BALLY +!
  BALLCLR @ HGRCOLOR
  BALLX @ BALLY @ HGRPLOT
  0 HGRCOLOR
  OLDX @ OLDY @ HGRPLOT
  BALLX @ OLDX !
  BALLY @ OLDY !
;

: BOUNCE
  1 HGRMODE    DROP
  0 HGRDRAWBUF DROP
  0 HGRSHOW    DROP
  BEGIN
    MOVEBALL
    ?TERMINAL
  UNTIL
  KEY DROP
  0 HGRMODE DROP
;

BOUNCE