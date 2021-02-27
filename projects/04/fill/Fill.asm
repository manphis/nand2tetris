// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

	@KBD
	D=A
	@keyaddr
	M=D

(LOOP)
	@SCREEN
	D=A
	@screenaddr
	M=D

	@keyaddr
	A=M
	D=M
	@i
	M=0			// i = 0

	@ZERO
	D;JEQ

	@value
	M=-1		// value = -1
	@FILLLOOP
	0;JMP

(ZERO)
	@value
	M=0			// value = 0

(FILLLOOP)
	@screenaddr
	D=M

	@keyaddr
	D=M-D
	@FILLLOOPEND
	D;JEQ

	@value
	D=M
	@screenaddr
	A=M
	M=D

	@screenaddr
	M=M+1		// screenaddr = screenaddr + 1

	@FILLLOOP
	0;JMP


(FILLLOOPEND)
	@LOOP
	0;JMP








