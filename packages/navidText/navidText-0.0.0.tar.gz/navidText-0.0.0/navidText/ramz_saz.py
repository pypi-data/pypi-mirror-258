def RamzSaz(text):
    num = ""
    for i in text:
        #============= English ==============#
        if i == "a":
            num += "~^="
        elif i == "b":
            num += "~&^"
        elif i == "c":
            num += "~&&"
        elif i == "d":
            num += "~&*"
        elif i == "e":
            num += "~&("
        elif i == "f":
            num += "~&)"
        elif i == 'g':
            num += "~&_"
        elif i == 'h':
            num += "~&-"
        elif i == 'i':
            num += "~&+"
        elif i == 'j':
            num += "~&="
        elif i == 'k':
            num += "~*^"
        elif i == 'l':
            num += "~*&"
        elif i == 'm':
            num += "~*("
        elif i == 'n':
            num += "~*)"
        elif i == 'o':
            num += "~*_"
        elif i == 'p':
            num += "~*-"
        elif i == 'q':
            num += "~*="
        elif i == 'r':
            num += "~*+"
        elif i == 's':
            num += "~(^"
        elif i == 't':
            num += "~(&"
        elif i == 'u':
            num += '~(*'
        elif i == 'v':
            num += "~(("
        elif i == 'w':
            num += "~()"
        elif i == 'x':
            num += "~(_"
        elif i == 'y':
            num += "~(-"
        elif i == 'z':
            num += "~(="
        #============= prsian ============#
        elif i == "ض":
            num += "~^!"
        elif i == "ص":
            num += "~^@"
        elif i == "ث":
            num += "~^#"
        elif i == "ق":
            num += "~^$"
        elif i == "ف":
            num += "~!!"
        elif i == 'غ':
            num += "~!#"
        elif i == 'ع':
            num += "~!$"
        elif i == 'ه':
            num += "~!%"
        elif i == 'خ':
            num += "~!^"
        elif i == 'ح':
            num += "~@!"
        elif i == 'ج':
            num += "~@@"
        elif i == 'چ':
            num += "~@#"
        elif i == 'ش':
            num += "~@$"
        elif i == 'س':
            num += "~@%"
        elif i == 'ی':
            num += "~@^"
        elif i == 'ب':
            num += "~#!"
        elif i == 'ل':
            num += "~#@"
        elif i == 'ا' or i=="آ":
            num += "~##"
        elif i == 'ت':
            num += "~#$"
        elif i == 'ن':
            num += '~#%'
        elif i == 'م':
            num += "~#^"
        elif i == 'ک':
            num += "~$!"
        elif i == 'گ':
            num += "~$@"
        elif i == 'پ':
            num += "~$#"
        elif i == 'ظ':
            num += "~$$"
        elif i == 'ط':
            num += "~$%"
        elif i == 'ز':
            num += "~$^"
        elif i == 'ژ':
            num += "~%!"
        elif i == 'ر':
            num += "~%@"
        elif i == 'ذ':
            num += "~%#"
        elif i == 'د':
            num += "~%$"
        elif i == 'ئ':
            num += "~%%"
        elif i == 'و':
            num += "~%^"
        #============= add ===============#
        elif i == '1' or i=="۱":
            num += "~=&"
        elif i == '2' or i=="۲":
            num += "~^%"
        elif i == '3' or i=="۳":
            num += "~^^"
        elif i == '4' or i=="۴":
            num += "~^&"
        elif i == '5' or i=="۵":
            num += "~^*"
        elif i == '6' or i=="۶":
            num += "~^("
        elif i == '7' or i=="۷":
            num += "~^)"
        elif i == '8' or i=="۸":
            num += "~^_"
        elif i == '9' or i=="۹":
            num += "~^-"
        elif i == '0' or i=="۰":
            num += "~^+"
        # ============= stiker ==============#
        elif i == '🤣':
            num += "~=*"
        elif i == '😊':
            num += "~=("
        elif i == '😂':
            num += "~=)"
        elif i == '😕':
            num += "~=-"
        elif i == '😐':
            num += "~=_"
        elif i == '😑':
            num += "~=="
        elif i == '😎':
            num += "~=+"
        elif i == '🤦🏻':
            num += "~!&"
        elif i == '😳':
            num += "~!*"
        elif i == '😍':
            num += "~!("
        elif i == '🤝':
            num += "~!)"
        elif i == '🙏':
            num += "~!-"
        elif i == '😉':
            num += "~!_"
        elif i == '🙄':
            num += "~!="
        elif i == '❤':
            num += "~!+"
        elif i == '🤷🏻':
            num += "~@&"
        elif i == '🌹':
            num += "~@("
        elif i == '😭':
            num += "~@)"
        # ============= Oder ==============#
        elif i == '!':
            num += "~(+"
        elif i == '@':
            num += "~)^"
        elif i == '#':
            num += "~)&"
        elif i == '$':
            num += "~)*"
        elif i == '%':
            num += "~)("
        elif i == '^':
            num += "~))"
        elif i == '&':
            num += "~)_"
        elif i == '*':
            num += "~)-"
        elif i == '(':
            num += "~)+"
        elif i == ')':
            num += "~)="
        elif i == '_':
            num += "~_^"
        elif i == '-':
            num += "~_&"
        elif i == '=':
            num += "~_*"
        elif i == '+':
            num += "~_("
        elif i == '[':
            num += "~_)"
        elif i == ']':
            num += "~__"
        elif i == '{':
            num += "~_-"
        elif i == '}':
            num += "~_="
        elif i == ':':
            num += "~_+"
        elif i == ';':
            num += "~-^"
        elif i == '"':
            num += "~-&"
        elif i == "'":
            num += "~-*"
        elif i == '\\':
            num += "~-("
        elif i == '|':
            num += "~-)"
        elif i == '<':
            num += "~--"
        elif i == '>':
            num += "~-_"
        elif i == '.':
            num += "~-="
        elif i == '/':
            num += "~-+"
        elif i == '?':
            num += "~=^"
        elif i== " ":
            num+="~*%"
        else:
            num+="~"+i
    return "`"+num+"`"
def ramznghar(text):
    num=""
    sp=text.split("~")
    for i in sp:
        # ============= English ==============#
        if i == "^=":
            num += "a"
        elif i == "&^":
            num += "b"
        elif i == "&&":
            num += "c"
        elif i == "&*":
            num += "d"
        elif i == "&(":
            num += "e"
        elif i == "&)":
            num += "f"
        elif i == '&_':
            num += "g"
        elif i == '&-':
            num += "h"
        elif i == '&+':
            num += "i"
        elif i == '&=':
            num += "j"
        elif i == '*^':
            num += "k"
        elif i == '*&':
            num += "l"
        elif i == '*(':
            num += "m"
        elif i == '*)':
            num += "n"
        elif i == '*_':
            num += "o"
        elif i == '*-':
            num += "p"
        elif i == '*=':
            num += "q"
        elif i == '*+':
            num += "r"
        elif i == '(^':
            num += "s"
        elif i == '(&':
            num += "t"
        elif i == '(*':
            num += 'u'
        elif i == '((':
            num += "v"
        elif i == '()':
            num += "w"
        elif i == '(_':
            num += "x"
        elif i == '(-':
            num += "y"
        elif i == '(=':
            num += "z"
        # ============= prsian ============#
        elif i == "^!":
            num += "ض"
        elif i == "^@":
            num += "ص"
        elif i == "^#":
            num += "ث"
        elif i == "^$":
            num += "ق"
        elif i == "!!":
            num += "ف"
        elif i == '!#':
            num += "غ"
        elif i == '!$':
            num += "ع"
        elif i == '!%':
            num += "ه"
        elif i == '!^':
            num += "خ"
        elif i == '@!':
            num += "ح"
        elif i == '@@':
            num += "ج"
        elif i == '@#':
            num += "چ"
        elif i == '@$':
            num += "ش"
        elif i == '@%':
            num += "س"
        elif i == '@^':
            num += "ی"
        elif i == '#!':
            num += "ب"
        elif i == '#@':
            num += "ل"
        elif i == '##':
            num += "ا"
        elif i == '#$':
            num += "ت"
        elif i == '#%':
            num += 'ن'
        elif i == '#^':
            num += "م"
        elif i == '$!':
            num += "ک"
        elif i == '$@':
            num += "گ"
        elif i == '$#':
            num += "پ"
        elif i == '$$':
            num += "ظ"
        elif i == '$%':
            num += "ط"
        elif i == '$^':
            num += "ز"
        elif i == '%!':
            num += "ژ"
        elif i == '%@':
            num += "ر"
        elif i == '%#':
            num += "ذ"
        elif i == '%$':
            num += "د"
        elif i == '%%':
            num += "ئ"
        elif i == '%^':
            num += "و"
        # ============= add ===============#
        elif i == '=&':
            num += "1"
        elif i == '^%':
            num += "2"
        elif i == '^^':
            num += "3"
        elif i == '^&':
            num += "4"
        elif i == '^*':
            num += "5"
        elif i == '^(':
            num += "6"
        elif i == '^)':
            num += "7"
        elif i == '^_':
            num += "8"
        elif i == '^-':
            num += "9"
        elif i == '^+':
            num += "0"
        # ============= stiker ==============#
        elif i == '=*':
            num += "🤣"
        elif i == '=(':
            num += "😊"
        elif i == '=)':
            num += "😂"
        elif i == '=-':
            num += "😕"
        elif i == '=_':
            num += "😐"
        elif i == '==':
            num += "😑"
        elif i == '=+':
            num += "😎"
        elif i == '!&':
            num += "🤦🏻"
        elif i == '!*':
            num += "😳"
        elif i == '!(':
            num += "😍"
        elif i == '!)':
            num += "🤝"
        elif i == '!-':
            num += "🙏"
        elif i == '!_':
            num += "😉"
        elif i == '!=':
            num += "🙄"
        elif i == '!+':
            num += "❤"
        elif i == '@&':
            num += "🤷🏻"
        elif i == '@(':
            num += "🌹"
        elif i == '@)':
            num += "😭"
        # ============= Oder ==============#
        elif i == '(+':
            num += "!"
        elif i == ')^':
            num += "@"
        elif i == ')&':
            num += "#"
        elif i == ')*':
            num += "$"
        elif i == ')(':
            num += "%"
        elif i == '))':
            num += "^"
        elif i == ')_':
            num += "&"
        elif i == ')-':
            num += "*"
        elif i == ')+':
            num += "("
        elif i == ')=':
            num += ")"
        elif i == '_^':
            num += "_"
        elif i == '_&':
            num += "-"
        elif i == '_*':
            num += "="
        elif i == '_(':
            num += "+"
        elif i == '_)':
            num += "["
        elif i == '__':
            num += "]"
        elif i == '_-':
            num += "{"
        elif i == '_=':
            num += "}"
        elif i == '_+':
            num += ":"
        elif i == '-^':
            num += ";"
        elif i == '-&':
            num += '"'
        elif i == "-*":
            num += "'"
        elif i == '-(':
            num += "\\"
        elif i == '-)':
            num += "|"
        elif i == '--':
            num += "<"
        elif i == '-_':
            num += ">"
        elif i == '-=':
            num += "."
        elif i == '-+':
            num += "/"
        elif i == '=^':
            num += "?"
        elif i == "*%":
            num += " "
        else:
            num+=i
    return "`"+num+"`"