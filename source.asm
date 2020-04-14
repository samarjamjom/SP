COPY     START  1000 
FIRST    STL    RETADR            SAVE RETURN ADDRESS       
CLOOP    JSUB   RDREC
         LDA    LENGTH            TEST FOR EOF
         COMP   ZERO
         JEQ    ENDFIL
         JSUB   WRREC
         J      CLOOP
         BASE
ENDFIL   LDA    =C'EOF'
         LDA    =X'F1'
         STA    BUFFER
         LDA    THREE8
         STA    LENGTH
         JSUB   WRREC
         LDL    RETADR
         RSUB
         LTORG
EOF      BYTE   C'EOF'
THREE    WORD   3
ZERO     WORD   0
RETADR   RESW   1
LENGTH   RESW   1
BUFFER   RESB   4096
.      SUBROUTINE TO READ RECORD INTO BUFFER
RDREC    LDX    ZERO
         LDA    ZERO
         LDA    =X'F2'
RLOOP    TD     INPUT
         JEQ    RLOOP
         RD     INPUT
         COMP   ZERO
         JEQ    EXIT
         STCH   BUFFER,X
         TIX    MAXLEN
         JLT    RLOOP
EXIT     STX    LENGTH
         RSUB       
         END    FIRST          