// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

	@R0
	D=M
	@STOP
	D;JEQ

	@n
	M=D		// n = R0

	@R1
	D=M
	@STOP
	D;JEQ

	@m
	M=D		// m = R1
	@i
	M=1		// i = 1
	@sum
	M=0		// sum = 0

(LOOP)
	@i
	D=M
	@m
	D=D-M	// i - m
	@STOP
	D;JGT

	@sum
	D=M
	@n
	D=D+M 	// sum = sum + n
	@sum
	M=D
	@i
	M=M+1	// i = i + 1
	@LOOP
	0;JMP

(STOP)
	@sum
	D=M
	@R2
	M=D
	@END
	0;JMP

(END)
	@END
	0;JMP







