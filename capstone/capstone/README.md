# Capstone - Make the Computer Draw a Box
Harshit | Roll no. 2501730196 | K = 96 | Nand to Tetris - I (ETCCNT301)

| Item | Value |
|---|---|
| K mod 3 = 0 | extra feature: `symbols.txt` |
| K mod 4 = 0 | width = 16 x 1 = 16 px (1 word) |
| Box | starts row 96, 20 rows tall, 16 px wide |
| Addresses | 19456 (SCREEN+3072) ... 20064, step 32 |

Run: `python assembler.py Box.asm` -> `Box.hack` + `symbols.txt`
Load `Box.hack` in the CPU Emulator, set animation to "No animation", then press/release a key.

Viva quick changes: move down -> change `@3072` (32 x row); taller -> change `@20`; wider -> add inner word loop.
