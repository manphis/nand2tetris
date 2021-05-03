import argparse

pushToStack = '@SP\nA=M\nM=D\n@SP\nM=M+1'
getMemValue = 'A=D+M\nD=M'
addCmd = '@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D+M'
subCmd = '@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=M-D'
cmpToD = '@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D'
negOp = '@SP\nA=M-1\nD=-M\nM=D'
notOp = '@SP\nA=M-1\nD=!M\nM=D'
andOp = '@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D&M'
orOp = '@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D|M'

register_table = {
	'local':'@LCL', 'argument':'@ARG', 'this':'@THIS', 'that':'@THAT'
}
gpRegister = ['R13', 'R14', 'R15']
result = ''
g_filename = ''
g_tag_count = 0

def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', '-i', type=str, required=True, help='input file for translator')
    
    return parser.parse_args()

def popToAddrInMem(reg):
	str = '@SP\nAM=M-1\nD=M\n@' + reg + '\nA=M\nM=D'
	return str

def popToMem(reg):
	str = '@SP\nAM=M-1\nD=M\n@' + reg + '\nM=D'
	return str

def pushBooleanToStack(flag):
	v = -1 if flag else 0
	return '@SP\nA=M\nM=' + str(v) + '\n@SP\nM=M+1'

def tag(str):
	return '(' + str + ')'

def append(str):
	global result
	result += str + '\n'

def parsePush(cmd, addr):
	if cmd == 'pointer':
		if addr == 0:
			append(register_table['this'])
		elif addr == 1:
			append(register_table['that'])
		append('D=M')
	elif cmd == 'static':
		append('@' + g_filename + '.' + str(addr))
		append('D=M')
	else:
		append('@' + str(addr))
		append('D=A')

		if cmd in register_table:
			append(register_table[cmd])
			append(getMemValue)
		elif cmd == 'temp':
			append('@5')
			append('A=D+A\nD=M')

	append(pushToStack)

def parsePop(cmd, addr):
	if cmd == 'pointer':
		if addr == 0:
			append(popToMem('THIS'))
		elif addr == 1:
			append(popToMem('THAT'))
	elif cmd == 'static':
		append(popToMem(g_filename + '.' + str(addr)))
	else:
		if cmd in register_table:
			reg = register_table[cmd] + '\nD=D+M'
		elif cmd == 'temp':
			reg = '@5\nD=D+A'

		append('@' + str(addr))
		append('D=A')
		append(reg)
		append('@'+gpRegister[0])
		append('M=D')
		append(popToAddrInMem(gpRegister[0]))

def parseSingleCmd(cmd):
	if cmd == 'add':
		append(addCmd)
	elif cmd == 'sub':
		append(subCmd)
	elif cmd == 'neg':
		append(negOp)
	elif cmd == 'not':
		append(notOp)
	elif cmd == 'and':
		append(andOp)
	elif cmd == 'or':
		append(orOp)
	else:
		append(cmpToD)
		global g_tag_count
		append('@compTrue' + str(g_tag_count))
		if cmd == 'eq':
			append('D;JEQ')
		elif cmd == 'lt':
			append('D;JLT')
		elif cmd == 'gt':
			append('D;JGT')

		append(pushBooleanToStack(False))
		append('@end' + str(g_tag_count))
		append('0;JMP')
		append(tag('compTrue' + str(g_tag_count)))
		append(pushBooleanToStack(True))
		append(tag('end' + str(g_tag_count)))

		g_tag_count += 1

def parse(file_name):
	global result
	global g_filename
	file = open(file_name, 'r')
	output_file = file_name.replace('.vm', '.asm')
	write_fp = open(output_file, "w")

	g_filename = file_name.split('/')[-1].split('.')[0]

	while True:
	    line = file.readline()
	    if not line:
	        break

	    line = line.strip()
	    if not line:
	    	continue
	    if line.startswith('//'):
	    	continue

	    append('//'+line)
	    items = line.split()
	    if len(items) == 3:
	    	if items[0] == 'push':
	    		parsePush(items[1], int(items[2]))
	    	elif items[0] == 'pop':
	    		parsePop(items[1], int(items[2]))
	    elif len(items) == 1:
	    	parseSingleCmd(items[0])

	write_fp.write(result)

	file.close()
	write_fp.close()


if __name__ == '__main__':
	args = process_command()
	parse(args.input_file)