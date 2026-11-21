// Box.asm  -  Capstone Part C
// Student: Harshit | Roll no: 2501730196 | K = 96
// Box: starts at row 96, 20 rows tall, 16 * ((96 mod 4) + 1) = 16 pixels wide (1 word).
// Key pressed -> black box.  Key released -> box disappears.
// Row r starts at SCREEN + 32*r, so row 96 starts at SCREEN + 3072 = 19456.

(LOOP)
    @KBD
    D=M
    @PRESSED
    D;JNE           // key pressed -> go set colour to black
    @color
    M=0             // no key -> white (0)
    @DRAW
    0;JMP
(PRESSED)
    @color
    M=-1            // key -> black (all 16 bits = 1)

(DRAW)
    @SCREEN
    D=A
    @3072           // 32 * 96
    D=D+A
    @addr
    M=D             // addr = first word of row 96
    @20
    D=A
    @count
    M=D             // count = 20 rows

(ROW)
    @color
    D=M
    @addr
    A=M
    M=D             // paint the one word (16 pixels) of this row
    @32
    D=A
    @addr
    M=D+M           // move down one row (+32 words)
    @count
    M=M-1
    D=M
    @ROW
    D;JGT           // repeat until 20 rows done
    @LOOP
    0;JMP
