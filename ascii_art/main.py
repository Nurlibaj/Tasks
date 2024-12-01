import sys
def load_ascii_art(filename):
    ascii_dict = {}
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        char_lines = []
        current_char = 32
        for line in lines:
            if len(line) ==0:
                if len(char_lines)!=0:
                    ascii_dict[current_char] = char_lines
                    char_lines = []
                    current_char = current_char+1
            else:
                char_lines.append(list(line))
    return ascii_dict
def display_text(some_text,dict):
    for i in range(8):
        for ch in some_text:
            for j in dict[ord(ch)][i]:
                print(j,end=" ")
        print()




#txt=input()
txt=""
if __name__=="__main__":
    if len(sys.argv)>1:
        txt=sys.argv[1]
        txt=txt.replace("\\n","")
ascii_art = load_ascii_art('standard.txt')
display_text(txt,ascii_art)
