#!/usr/local/bin/python3
"""
VarInt Converter – GUI
"""
import argparse

def integer_to_varint(value, out):
    try:       
        integer = int(value)      
        integerinput = bytes.fromhex('%04X' % (integer))             
        result = []  
        length = len(integerinput)
        count = length
        loc = 1
        this = ((integerinput[length - loc] << loc) & 0xFF00) >> 8
        last = ((integerinput[length - loc] << loc) & 0xFF) >> 1
        result.append('%02X' % last)
        last = this
        count -=1
        loc += 1
        while count > 0:
            this = (((integerinput[length - loc] << loc) & 0xFF00) >> 8)
            last = ((((integerinput[length - loc] << loc) & 0XFF) >> 1) + last) + 128
            result.insert(0, '%02X' % last)
            last = this
            loc += 1
            count -= 1
        result.insert(0, '%02X' % (last + 128))
        while '80' in result:
            result.remove('80')
        final = ''.join(result)
        out = final
    except ValueError:
        print("Error: Invalid Integer Value")
    return(out)

def varint_to_int(value, out):
    out=''
    try:
        hexinput = value
        hexinput = bytes.fromhex(hexinput)
        numofvalues = len(hexinput)
        this = 0
        last = (hexinput[numofvalues - 1] << 1)
        count = 2
        leftshift = 8
        while (numofvalues - count) >= 0:
            this = ((((hexinput[numofvalues - count] << 1) & 0xFF) >> 1) << leftshift)
            last = (this | last)
            count += 1
            leftshift += 7
        out = out + str((last >> 1))               
    except ValueError:
        print("Error: Invalid Hex Value")
    return(out)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('Art', help='varint or int')
    parser.add_argument('Wert', help='Wert eingeben')
    args = parser.parse_args()
    out = ''

    if args.Art == 'varint':
        print('Umrechnung varInt nach Int!')
        erg = varint_to_int(args.Wert,out)
        print('Eingabe varInt: ',args.Wert)
        print ('Ausgabe Int: ',erg)
    elif args.Art == 'int':
        print('Umrechnung Int nach varInt')
        erg = integer_to_varint(args.Wert,out)
        print('Eingabe Int: ',args.Wert)
        print ('Ausgabe varInt: ',erg)
    else:
        print('Bitte varint oder int auswählen!')

if __name__ == "__main__":
    main()