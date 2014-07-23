#import plasTeX.TeX

#tex = plasTeX.TeX.TeX()
tex_2_wiki_dic = \
  { "\\Procedure{" : ("{{algorithm-begin|name=", "}{", "}}\n Input: ", "}"), \
    "\\ForAll{" : ("'''For each''' ", "}:", ", '''do'''"), \
    "\\For{" : ("'''For'''", "}:", ", '''do'''"), \
    "\\EndFor\n" : ("",), \
    "\\State" : ("", "\n"), \
    "\\Call{" : ("'''Call''' '''", "}{", "'''(", "}", ")"), \
    "\\Comment" : ("#","\n",""), \
    "\\If {": ("'''If'''", "}", "''', then'''"), \
    "\\Else": ("'''Else'''"), \
    "\\EndIf\n" : ("",), \
    "\\Return": ("'''Return'''", "\n"), \
    "$": ("''", "$", "''", "\n"), \
    "\\EndProcedure": ("",), \
    "\\begin{algorithm}[H]\n": ("",), \
    "\\caption{":("====","}", "===="), \
    "\\begin{algorithmic}[1]\n": ("",), \
    "\\end{algorithmic}\n":("",), \
    "\\end{algorithm}\n": ("",), \
    "\\label{": ("<!--","}","-->")
  }

def convertor(cur_token):
    import pdb
    #pdb.set_trace()
    new_token_list = []
    begin_offset = 0
    for offset in range(0,len(cur_token)):
        #print offset
        for state_selector in tex_2_wiki_dic:
            if (state_selector == '\\State' and cur_token == "  \State Global $myId := 1$\n"):
                pass#pdb.set_trace()
            if (cur_token[offset:offset + len(state_selector)] == state_selector):
                #pdb.set_trace()
                new_token_list.append(cur_token[begin_offset:offset] + tex_2_wiki_dic[state_selector][0])
                in_state_offset = offset+ len(state_selector)
                for i in range(1, len(tex_2_wiki_dic[state_selector]),2):
                    if in_state_offset >= len(cur_token):
                        break
                    new_token_offset = cur_token[in_state_offset:].find(tex_2_wiki_dic[state_selector][i])
                    if (new_token_offset < 0):
                        new_token_offset = len(cur_token[in_state_offset:])

                    new_token_list.append(convertor(cur_token[in_state_offset:in_state_offset + new_token_offset]))

                    if i+1 < len(tex_2_wiki_dic[state_selector]):
                        new_token_list.append(tex_2_wiki_dic[state_selector][i+1])

                        in_state_offset += new_token_offset + len(tex_2_wiki_dic[state_selector][i])

                return ''.join(new_token_list)

    #pdb.set_trace()
    return cur_token

tex_file = open('mpCat_spec_ver_0.2.1_algo.tex','r')
for cur_line in tex_file:
    if cur_line == "END\n":
        break

    conv_line =  convertor(cur_line)
    if conv_line.strip(' ') != "":
        print conv_line
    else:
        pass#print "EMPTY"
