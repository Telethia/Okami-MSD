

# Program to convert Okami's .MSD file format to readable .txt files.

import os

CTEBase = []
CTEBytes = []
CTEChars = []
File1 = input("Drag file here: ")
File3 = File1.lower().strip(".msd")
CTEFile = open("default.tbl", 'r', encoding="UTF-8")
UpperByte = 0x00
LowerByte = 0x00
MsdFile = open(File3 + ".MSD", 'rb')
File2 = os.path.basename(File1)
OutputFile = open(File3 + ".txt", 'w', encoding="UTF-8")
MsdFileSize = os.path.getsize(File1)
DialogCount = int.from_bytes(MsdFile.read(2), 'little') #Number of entries in file
Dialog2Count = int.from_bytes(MsdFile.read(2), 'little') #Number of second kind of entry in file. No clue what it is.
Offsets = []
MsdFile.seek(0, 0)
count = 0
#String = int.from_bytes(MsdFile.read(2), 'little') #First set of two bytes. Here we go.
#StringHex = str("0x" + format(String, 'x').zfill(4))

def test():
    Entries = 0
    #MsdFile.seek(0, 0) #Normalize from beginning of file
    while Entries < DialogCount:
        MsdFile.seek(4, 1)
        Value = int.from_bytes(MsdFile.read(4), 'little')
        #print(str("0x" + format(Value, 'x').zfill(4)))
        Offsets.append(Value) #Put entries into file
        Entries += 1
        continue
    
    with open("default.tbl", 'r', encoding="UTF-8") as fp:
        for count, line in enumerate(fp, 1):
            pass
    #print('Total Number of lines:', count if 'count' in locals() else 0)

    for line in CTEFile:
        CTEBase.append(line)
        
    for item in CTEBase:
        #print(item)
        try:
            item1, item2 = item.split("=")
            CTEBytes.append(item1)
            CTEChars.append(item2)
        except ValueError:
            print("Malformed value at" + item)
            pass
    print("Starting conversion...")
    i = 0
    index = 0
    MsdFile.seek(Offsets[0], 0)
    OutputFile.write("Dialogs: " + str(DialogCount) + "\n\n")
    Val = 1
    Text = "{BeginDialog: 0}\n"
    OutputFile.write(Text)
    while i < MsdFileSize:
        #Loop through whole file to print out the symbols
        #print("i is " + str(i))
        index = 0
        StrTemp = int.from_bytes(MsdFile.read(2), 'little')
        StrHexTemp = str("0x" + format(StrTemp, 'x').zfill(4))
        #print("StrHexTemp is " + StrHexTemp)
        
        
        for x in CTEBytes: #Start looping through the table and look for any matches
            #print(index)
            match StrHexTemp:
                case "0x0000":
                    #print("We zero")
                    i == MsdFileSize + 1
                    break
                case "0xa001":
                    Text = "\n"
                    #print(Text)
                    OutputFile.write(Text)
                    break
                case "0x8001":
                    Text = "\n{EndDialog}\n\n"
                    #print(Text)
                    OutputFile.write(Text)
                    if Val == DialogCount:
                        print("Complete!")
                        return
                    else:
                        #print("Value of Offsets is " + str(Val))
                        MsdFile.seek(Offsets[Val], 0)
                        Text = "\n{BeginDialog: " + str((Val)) + "}\n"
                        OutputFile.write(Text)
                        Val += 1
                    break
                case "0x8103":
                    StrHexTemp = MsdFile.read(4)
                    StrHexTemp = StrHexTemp.decode()
                    Text = "{Speaker1:" + StrHexTemp + "}"
                    #print(Text,end="")
                    OutputFile.write(Text)
                    break
                case "0x8203":
                    StrHexTemp = MsdFile.read(4)
                    StrHexTemp = StrHexTemp.decode()
                    Text = "{Speaker2:" + StrHexTemp + "}"
                    #print(Text,end="")
                    OutputFile.write(Text)
                    break
                case "0x8303":
                    Opcode1 = int.from_bytes(MsdFile.read(2), 'little')
                    Opcode1H = str("0x" + format(Opcode1, 'x').zfill(4))
                    Opcode2 = int.from_bytes(MsdFile.read(2), 'little')
                    Opcode2H = str("0x" + format(Opcode2, 'x').zfill(4))
                    Text = "{0x8303:" + str(Opcode1H) + ", " + str(Opcode2H) + "}"
                    OutputFile.write(Text)
                    #print("{0x8303:" + str(Opcode1H) + ", " + str(Opcode2H) + "}",end="")
                    break
                case "0x8903":
                    Opcode1 = int.from_bytes(MsdFile.read(2), 'little')
                    Opcode1H = str("0x" + format(Opcode1, 'x').zfill(4))
                    Opcode2 = int.from_bytes(MsdFile.read(2), 'little')
                    Opcode2H = str("0x" + format(Opcode2, 'x').zfill(4))
                    Text = "{OldPrompt:" + str(Opcode1H) + ", " + str(Opcode2H) + "}"
                    OutputFile.write(Text)
                    #print("{OldPrompt:" + str(Opcode1H) + ", " + str(Opcode2H) + "}",end="")
                    break
                case "0x8A01":
                    Text = "{0x8A01}"
                    OutputFile.write(Text)
                    break
                case "0x9302":
                    Opcode1 = int.from_bytes(MsdFile.read(2), 'little')
                    Opcode1H = str("0x" + format(Opcode1, 'x').zfill(4))
                    Text = "{Yen:" + str(Opcode1H) + "}"
                    OutputFile.write(Text)
                    break
                case "0x9502":
                    Opcode1 = int.from_bytes(MsdFile.read(2), 'little')
                    Opcode1H = str("0x" + format(Opcode1, 'x').zfill(4))
                    if Opcode1H == "0xffff":
                        Text = "{Item: contextual}"
                        OutputFile.write(Text)
                    else:
                        Text = "{Item:" + str(Opcode1H) + + "}"
                        OutputFile.write(Text)
                    break
                case "0xa101":
                    Text = "{Clear}\n"
                    OutputFile.write(Text)
                    break
                case "0xa301":
                    Text = "{Pause}"
                    OutputFile.write(Text)
                    break
                case "0xb301":
                    Text = "{black}"
                    OutputFile.write(Text)
                    break
                case "0xb602":
                    Opcode1 = int.from_bytes(MsdFile.read(2), 'little')
                    Opcode1H = str("0x" + format(Opcode1, 'x').zfill(4))
                    if Opcode1H == "0x0001":
                        Text = "{Color: Red}"
                        OutputFile.write(Text)
                        break
                    else:
                        Text = "{Color:" + str(Opcode1H) + "}"
                        OutputFile.write(Text)
                        break
                case "0xd201":
                    Text = "{Issun}"
                    OutputFile.write(Text)
                    break
                case "0xd404":
                    Opcode1 = int.from_bytes(MsdFile.read(2), 'little')
                    Opcode1H = str("0x" + format(Opcode1, 'x').zfill(4))
                    Opcode2 = int.from_bytes(MsdFile.read(2), 'little')
                    Opcode2H = str("0x" + format(Opcode2, 'x').zfill(4))
                    Opcode3 = int.from_bytes(MsdFile.read(2), 'little')
                    Opcode3H = str("0x" + format(Opcode3, 'x').zfill(4))
                    Text = "{PlaySound:" + str(Opcode1H) + ", " + str(Opcode2H) + ", " + str(Opcode3H) + "}"
                    OutputFile.write(Text)
                    break
                case _:
                    if x == StrHexTemp: #If we find it, print it out.
                        StrHexTemp = StrHexTemp.zfill(4)
                        #print("Index found at " + str(index))
                        Text = str((CTEChars[index].replace('\n','')))
                        OutputFile.write(Text)
                        #print(str((CTEChars[index].replace('\n',''))),end="")
                        break
                    else:
                        if index >= len(CTEChars) - 1: #Print it MAYBE
                            Text = "{" + str(StrHexTemp) + "}"
                            #print(Text)
                            OutputFile.write(Text)
                            break
                        else: #Iterate value
                            index+=1
            
        i+=1
    #print("File size is " + str(MsdFileSize))
    #print("Hello World")
    #print("File has {" + str(DialogCount) + ", " + str(Dialog2Count) + "} entries")
    #print("TrueOffset is " + str(OffsetTest))
    #print("First two bytes " + str(OffsetTest) + " bytes into the file is " + str(StringHex))
    #print(CTEBase[index])
    #print(CTEBytes[index])
    #print(CTEChars[index])
    print("Complete!")

test()