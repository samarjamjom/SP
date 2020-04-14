""" The output of Pass 1 is:
1. Symbol Table SYBTAB: should be displayed on the screen.
2. LOCCTR, PRGLTH, PRGNAME, ...
3. Intermediate file (.mdt): Stored on the secondary storage. 
4.Your assembler can stop execution if there are errors in Pass 1"""


#TEAM MEMBERS
#samar jamjom
#latifa masri


import guiForm
from tkinter import messagebox
import tkinter as tk

source_code,intermid_file = guiForm.gui_fun()

if source_code == "":
    messagebox.showerror("ERROR ","Please only Browse to get full path of .asm file!\n" \
                                "\n\nError MSG: {0}")
#open source file to read it
sic_source_file = open(source_code, "r")

#open OPTAP file to read it
opcode_table_file = open("OPTAB.txt", "r")

#read  all input lines
sic_assembly = sic_source_file.readlines()

#read opcode table 
opcode_table = opcode_table_file.readlines()

symbol_table = {}
opt_table = {}
literal_table = {}
literal_tab = {}
prog_name = ""
prog_leng = 0
start_add = 0
error_flag = 0


#initialize instruction component
label = ""
opcode = ""
operand = 0
comment = ""

#create a .text files  
intermid_file = open(intermid_file+".mdt","w+")

#initialize a list of directives
directives = ["START", "END", "BYTE", "WORD", "RESB", "RESW", "BASE", "LTORG"]

#store opcode table in 2D list
for ind, line in enumerate(opcode_table):
    #read file from third line 
    if ind>1:
        opt_table[line[0:11].split(' ')[0]] = line[12:15].strip()

#read first input line
first_line = sic_assembly[0]
if first_line[9:15].strip() == "START":
    prog_name =  first_line[0:8].strip()
    start_add = int(first_line[16:35].strip(),16)
    loc_ctr = start_add

    #to save a fixed format in intermediate file 
    blanks = 6-len(str((loc_ctr)))

    #write line to intemediate file
    intermid_file.write(hex(loc_ctr)[2:]+" "*blanks+first_line)
    
else:
    loc_ctr = 0

for ind, line in enumerate(sic_assembly):
    #read opcode
    opcode = line[9:15].strip()
    if opcode == "END":
        break
    elif opcode != "START":
        #if this is not a comment line
        if line[0] != '.':
            if line[34:] != "":
                line = line[:34]+"\n"
                
            #write line to intemediate file
            #check if that line is LTORG
            if(opcode == "LTORG" or opcode == "BASE"):
                intermid_file.write(" "*6+line)
            else :
                #to save a fixed format in intermediate file
                blanks = 6-len(str(hex(loc_ctr)[2:]))
                intermid_file.write(hex(loc_ctr)[2:]+" "*blanks+line)
            
            #read label field
            label = line[0:8].strip()
            #if there is asymbol in label field
            if label != "":
                #serch SYMTAB for LABEL
                #if found
                if label in symbol_table:
                    #set error flag
                    error_flag = 1
                    print("ERROR, Duplicate symbol!")
                    # message box display
                    messagebox.showerror("ERROR ","Duplicate symbol!\n" \
                                "\n\nError MSG: {0}")
                    break
                #else insert [label, LOCCTR] into SYMTAB
                else:
                    symbol_table[label] = hex(loc_ctr)[2:]

            #read opcode field
            #search OPTAB for OPCODE
            #if found
            if opcode in opt_table:
                #add 3 {instruction length} to LOCCTR
                loc_ctr += 3
            #if not found
            elif opcode in directives:
                if opcode == "WORD":
                    #add 3 {instruction length}
                    loc_ctr += 3
                elif opcode == "RESW":
                    operand = line[16:35].strip()
                    loc_ctr += 3 * int(operand)
                elif opcode == "RESB":
                    operand = line[16:35].strip()
                    loc_ctr += int(operand)
                elif opcode == "BYTE":
                    operand = line[16:35].strip()
                    #find the length of constant in bytes and add it to loc_ctr
                    if operand[0] == 'X':
                        loc_ctr += int((len(operand) - 3)/2)
                    elif operand[0] == 'C':
                        loc_ctr += (len(operand) - 3)
                #place literals into a pool at some location in object program
                elif opcode == "LTORG":
                    for key in literal_table:
                        literal_table[key][2] = hex(loc_ctr)[2:]
                        blanks = 6-len(str(hex(loc_ctr)[2:]))
                        intermid_file.write(hex(loc_ctr)[2:]+" "*blanks+"*"+" "*7+"="+key+"\n")
                        loc_ctr += int(literal_table[key][1])
                    literal_table = {}
            else:
                #set error flag
                error_flag = 1
                print("ERROR, Invalid operation code")
                # message box display
                messagebox.showerror("invalid operation code","Please enter valid operation code\n" \
                                "\n\nError MSG: {0}")
                break
                    
            #check if line contain literal
            if line[16:17] == '=':
                literalList = []
                isExist = 1
                literal = line[17:35].strip()
                if literal[0]=='C':
                    hexCode = literal[2:-1].encode("utf-8").hex()
                elif literal[0]== 'X':
                    hexCode = literal[2:-1]
                else:
                    #set error flag
                    error_flag = 1
                    print("invalid literals")
                    # message box display
                    messagebox.showerror("invalid literals","Please enter valid literal\n" \
                                "E.g.: =C'' or =X''"
                                "\n\nError MSG: {0}")
                #find literal in table literal

                if literal in literal_tab:
                    isExist = 0
                
                #if literal not exist in literal tabel 
                if isExist:
                    literalList=[hexCode,len(hexCode)/2, 0]
                    literal_table[literal]= literalList
                    literal_tab[literal]= literalList
if line[34:] != "":
    line = line[:34]+"\n"
if(opcode == "END"):
    intermid_file.write(" "*6+line)

#place literals into apool at the end of prog
#if not LTORG has came after them 
if literal_table:
    for key in literal_table:
        literal_table[key][2] = hex(loc_ctr)[2:]
        blanks = 6-len(str(hex(loc_ctr)[2:]))
        intermid_file.write(hex(loc_ctr)[2:]+" "*blanks+"*"+" "*7+"="+key+"\n")
        loc_ctr += int(literal_table[key][1])

#save (loc_ctr - starting add ) as program length
prog_leng = int(loc_ctr) - int(start_add)

#close file
sic_source_file.close()
opcode_table_file.close()
intermid_file.close()

""" 
if error_flag != 1:
    pl = hex(int(prog_leng))[2:].format(int(prog_leng))
    lc = hex(int(loc_ctr))[2:].format(int(loc_ctr))
    print("name of the program: ",prog_name)
    print("length of the program: ",pl)
    print("LOCCTR: ",lc)
    print("symbol table : ",symbol_table)
    print("literal table : ",literal_tab)

    SymbolTable = "\nSymbol"+" "*4+"address\n"
    for Symbol in symbol_table:
        blanks = 8-len(Symbol)
        SymbolTable += (Symbol+" "*blanks+"  "+ symbol_table[Symbol] + '\n')

    literalTable = "\nliteral"+" "*3+"value"+" "*9+"length"+" "*3+"address\n"
    for literal in literal_tab:
        blanks = 10-len(str(literal))
        b = blanks*2
        literalTable += (literal+" "*blanks+ str(literal_tab[literal][0])+" "*b+str(literal_tab[literal][1])+" "*9+str(literal_tab[literal][2]) + '\n')

    root = tk.Tk()
    root.title("output of pass1")
    programName = tk.Text(root, height=60, width=80)
    programName.pack()
    quote = "program name: "+prog_name+"\n\nLocation counter: "+lc+"\n\nthe length of the program: "+pl+"\n\nSYMTAB: "+SymbolTable+"\n\nLITTAB: "+literalTable
    programName.insert(tk.END, quote)

    root.mainloop()
 """


import pass2
pass2.send_tables(symbol_table,opt_table,literal_tab,directives,prog_name)
