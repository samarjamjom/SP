""" The output of Pass 2:
1. The object file (.obj)
2. The listing file (.lst)
3. List of errors if happened (duplicate labels, invalid mnemonic,
inappropriate operand...). """


def send_tables(symbol_table,opt_table,literal_tab,directives,prog_name):

    #open source file to read it
    intermid_file = open("intermid.mdt", "r")

    #read  all input lines
    sic_assembly = intermid_file.readlines()

    #create a .lst files  
    list_file = open("list.lst","w+")

    error_flag = 0
    for ind, line in enumerate(sic_assembly):

        opject_code = ""

        opcode = line[15:21].strip()
        operand = line[22:41].strip()

        
        if opcode not in directives:

            #first segment of opject code
            if opcode in opt_table:
                opject_code += opt_table[opcode]

            #second segment of opject code
            if ",X" in operand:
                opject_code += "1"
            else:
                opject_code += "0"

            #third segment of opject code
            if operand in symbol_table:
                opject_code += symbol_table[operand]

        #elif opcode == "BYTE":

        #elif opcode == "WORD":




            print(opject_code)
            



    
    