import argparse

symbol_table = {
	'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7, 'R8':8, 'R9':9, 'R10':10,
	'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15, 'SCREEN':16384, 'KBD':24576,
	'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4
}

dest_table = {
	'M':'001', 'D':'010', 'MD':'011', 'A':'100', 'AM':'101', 'AD':'110', 'AMD':'111'
}

jump_table = {
	'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'
}

comp_table = {
	'0':'0101010', '1':'0111111', '-1':'0111010', 'D':'0001100', 'A':'0110000', '!D':'0001101', '!A':'0110001',
	'-D':'0001111', '-A':'0110011', 'D+1':'0011111', 'A+1':'0110111', 'D-1':'0001110', 'A-1':'0110010',
	'D+A':'0000010', 'D-A':'0010011', 'A-D':'0000111', 'D&A':'0000000', 'D|A':'0010101',
	'M':'1110000', '!M':'1110001', '-M':'1110011', 'M+1':'1110111', 'M-1':'1110010', 'D+M':'1000010',
	'D-M':'1010011', 'M-D':'1000111', 'D&M':'1000000', 'D|M':'1010101'
}

get_bin = lambda x, n: format(x, 'b').zfill(n)

def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', '-i', type=str, required=True, help='input file for assembler')
    
    return parser.parse_args()

def parse(file_name):
	file = open(file_name, 'r')
	output_file = file_name + '.hack'
	write_fp = open(output_file, "w")
	count = 0
	result = ''

	# phase 1: add symbol
	while True:
	    line = file.readline()
	    if not line:
	        break

	    line = line.strip()
	    if not line:
	    	continue
	    if line.startswith('//'):
	    	continue

	    if line.startswith('('):
	    	idx = line.find(')')
	    	symbol = line[1:idx]
	    	if symbol not in symbol_table:
	    		symbol_table[symbol] = count
	    	continue

	    count += 1
	
	file.seek(0)
	count = 0
	available_addr = 16
	# phase 2: parse
	while True:
	    line = file.readline()
	    if not line:
	        break

	    line = line.strip()
	    if not line:
	    	continue
	    if line.startswith('//'):
	    	continue

	    if '//' in line:
	    	line = line.split('//')[0].strip()


	    if line.startswith('('):
	    	continue
	    
	    elif line.startswith('@'):
	    	addr = line.split('@')[1]
	    	if addr.isdigit():
	    		result = '0' + get_bin(int(addr), 15)
	    	else:
	    		if addr in symbol_table:
	    			sym_addr = symbol_table[addr]
	    		else:
	    			sym_addr = available_addr
	    			symbol_table[addr] = sym_addr
	    			available_addr += 1
	    		result = '0' + get_bin(sym_addr, 15)
	    
	    else:
	    	statement = line
	    	jump = None
	    	bin_dest = '000'
	    	bin_comp = ''
	    	bin_jump = '000'
	    	result = '111'

	    	if ';' in line:
	    		jump = line.split(';')[1].strip()
	    		statement = line.split(';')[0].strip()

	    	if '=' in statement:
	    		dest = statement.split('=')[0].strip()
	    		comp = statement.split('=')[1].strip()
	    	else:
	    		dest = None
	    		comp = statement

	    	result += comp_table[comp]

	    	if dest != None:
	    		bin_dest = dest_table[dest]
	    	result += bin_dest

	    	if jump != None:
	    		bin_jump = jump_table[jump]
	    	result += bin_jump

	    write_fp.write(result + '\n')

	    count += 1
	    
	    # print("Line{}: {}".format(count, line))
	    # print("result = {}".format(result))
	 
	# print(f'total {count} lines')
	file.close()
	write_fp.close()

	print(symbol_table)


if __name__ == '__main__':
	args = process_command()
	parse(args.input_file)