

def poziv_Parse_Macros(self):
    self._iter_lines(self.parse_Pow)
    self.fix_Lines()
    self._iter_lines(self.parse_Mult)
    self.fix_Lines()
    self._iter_lines(self.parse_Div)
    self.fix_Lines()
    
    self._iter_lines(self.parse_Macros)
    



def handle_Destination(self, line):
        #dst moze biti varijabla ili @10 ili @R100
        
        
        l=line.split("(")[1]
        l=l.split(",")
        dst=l[0]
        
        
        if dst[0]=='@':
            dio_iza_monkeya=dst.split("@")[1] #@10
            if dio_iza_monkeya.isnumeric():
                return dio_iza_monkeya
            
            elif dio_iza_monkeya[0]=='R':  #@R10
                dio_iza_R=dio_iza_monkeya.split("R")[1]
                if dio_iza_R.isnumeric():
                    return dio_iza_R
            return dio_iza_monkeya  #varijabla
        
        elif dst[0]=='R': #R10
            dio_iza_R=dst.split('R')[1]
            if(dio_iza_R.isnumeric()):
                return dio_iza_R
        
        
        self._flag = False
        self._errm = "Invalid destination in macro."
        return

def handle_Arg1(self,line):
    if ',' not in line or '('  not in line or ')' not in line:
        self._flag=False
        self._errm="Invalid macro syntax"
        return
    l= line.split(',')[1]
    dst=l.split(')')[0]
    
    if dst[0]=='@':
        dio_iza_monkeya=dst.split("@")[1] #@10
        if dio_iza_monkeya.isnumeric():
            return dio_iza_monkeya
            
        elif dio_iza_monkeya[0]=='R':  #@R10
            dio_iza_R=dio_iza_monkeya.split("R")[1]
            if dio_iza_R.isnumeric():
                return dio_iza_R
        return dio_iza_monkeya #varijabla
        
    elif dst[0]=='R': #R10
        dio_iza_R=dst.split('R')[1]
        if(dio_iza_R.isnumeric()):
            return dio_iza_R
        
    elif dst.isnumeric():
        return ""
    
    self._flag = False
    self._errm = "Invalid first argument in macro."
    return


def handle_Arg2(self,line):
    if ',' not in line or '('  not in line or ')' not in line:
        self._flag=False
        self._errm="Invalid macro syntax"
        return
    l= line.split(',')[2]
    dst=l.split(")")[0]
    
    if dst[0]=='@':
        dio_iza_monkeya=dst.split("@")[1] #@10
        if dio_iza_monkeya.isnumeric():
            return dio_iza_monkeya
            
        elif dio_iza_monkeya[0]=='R':  #@R10
            dio_iza_R=dio_iza_monkeya.split("R")[1]
            if dio_iza_R.isnumeric():
                return dio_iza_R
        return dio_iza_monkeya #varijabla
        
    elif dst[0]=='R': #R10
        dio_iza_R=dst.split('R')[1]
        if(dio_iza_R.isnumeric()):
            return dio_iza_R
        
    elif dst.isnumeric():

        return ""
    
    self._flag = False
    self._errm = "Invalid second argument in macro."
    return


def handle_cond(self,line):
    if '('  not in line or ')' not in line:
        self._flag=False
        self._errm="Invalid macro syntax"
        return
    l=line.split("(")[1]
    dst=l.split(")")[0]
    if dst[0]=='@':
            dio_iza_monkeya=dst.split("@")[1] #@10
            if dio_iza_monkeya.isnumeric():
                self.cond=dio_iza_monkeya
            
            elif dio_iza_monkeya[0]=='R':  #@R10
                dio_iza_R=dio_iza_monkeya.split("R")[1]
                if dio_iza_R.isnumeric():
                    self.cond=dio_iza_R
            self.cond=dio_iza_monkeya #varijbala
        
    elif dst[0]=='R': #R10
            dio_iza_R=dst.split('R')[1]
            if(dio_iza_R.isnumeric()):
                self.cond=dio_iza_R
        
        
 
    
    
    
      

def parse_Macros(self,line,m,n):
    line=line.replace(" ", "")
    
    if line[0] != "$" and line[0]!="{" and line[0]!="}":
        return line
    
                
    if line[0:3]=="$MV":
        dst=self.handle_Destination(line)
        arg1=self.handle_Arg1(line)
        if(arg1==""): #arg1 je konstanta
            l= line.split(',')[1]
            arg1=l.split(')')[0]
            return "@"+arg1+"\nD=A\n"+"@"+dst+"\nM=D" 
        return "@"+arg1+"\nD=M\n"+"@"+dst+"\nM=D" #arg1 nije konstanta
    
    
    elif line[0:4]=="$ADD":
        dst=self.handle_Destination(line)
        arg1=self.handle_Arg1(line)
        arg2=self.handle_Arg2(line)

        
        if arg1=="": 
            l= line.split(',')[1]
            const_arg1=l.split(')')[0]
        
        if arg2=="":
            l= line.split(',')[2]
            const_arg2=l.split(")")[0]
        
        if arg1=="" and arg2=="":    #arg1 i arg2 su konstante
            return "@"+const_arg1+"\nD=A\n"+"@"+dst+"\nM=D\n"+"@"+const_arg2+"\nD=A\n"+"@"+dst+"\nM=M+D"
        
        elif arg1 == "" and arg2 != "":   #samo arg1 je konstanta
            return "@"+const_arg1+"\nD=A\n"+"@"+dst+"\nM=D\n"+"@"+arg2+"\nD=M\n"+"@"+dst+"\nM=M+D"
            
        elif arg1 != "" and arg2 == "":   #samo arg2 je konstanta 
            return "@"+arg1+"\nD=M\n"+"@"+dst+"\nM=D\n"+"@"+const_arg2+"\nD=A\n"+"@"+dst+"\nM=M+D"
        return "@"+arg1+"\nD=M\n"+"@"+dst+"\nM=D\n"+"@"+arg2+"\nD=M\n"+"@"+dst+"\nM=M+D" #ni arg1 ni arg2 nisu konstante
              
    
    elif line[0:5]=="$SWAP":
        arg1=self.handle_Destination(line)
        arg2=self.handle_Arg1(line)
        if arg2=="":
            self._flag = False
            self._errm = "Invalid second argument in macro."
            return
        return "@"+arg2+"\nD=M\n"+"@"+arg1+"\nM=M+D\nD=M\n"+"@"+arg2+"\nM=D-M\nD=M\n"+"@"+arg1+"\nM=M-D"
    
    
    elif line[0:4]=="$SUB":
        dst=self.handle_Destination(line)
        arg1=self.handle_Arg1(line)
        arg2=self.handle_Arg2(line)
        
        if arg1=="": 
            l= line.split(',')[1]
            const_arg1=l.split(')')[0]
        
        if arg2=="":
            l= line.split(',')[2]
            const_arg2=l.split(")")[0]
            
        if arg1=="" and arg2=="":    #arg1 i arg2 su konstante
            return "@"+const_arg1+"\nD=A\n"+"@"+dst+"\nM=D\n"+"@"+const_arg2+"\nD=A\n"+"@"+dst+"\nM=M-D"
        
        elif arg1 == "" and arg2 != "":   #samo arg1 je konstanta
            return "@"+const_arg1+"\nD=A\n"+"@"+dst+"\nM=D\n"+"@"+arg2+"\nD=M\n"+"@"+dst+"\nM=M-D"
        
        elif arg1 != "" and arg2 == "":   #samo arg2 je konstanta 
            return "@"+arg1+"\nD=M\n"+"@"+dst+"\nM=D\n"+"@"+const_arg2+"\nD=A\n"+"@"+dst+"\nM=M-D"
        return "@"+arg1+"\nD=M\n"+"@"+dst+"\nM=D\n"+"@"+arg2+"\nD=M\n"+"@"+dst+"\nM=M-D" #ni arg1 ni arg2 nisu konstante
    
    
    elif line[0:4]=="$AND":
        dst=self.handle_Destination(line)
        arg1=self.handle_Arg1(line)
        arg2=self.handle_Arg2(line)
        
        if arg1=="": 
            l= line.split(',')[1]
            const_arg1=l.split(')')[0]
        
        if arg2=="":
            l= line.split(',')[2]
            const_arg2=l.split(")")[0]
    
        if arg1=="" and arg2=="":    #arg1 i arg2 su konstante
            return "@"+const_arg1+"\nD=A\n"+"@"+dst+"\nM=D\n"+"@"+const_arg2+"\nD=A\n"+"@"+dst+"\nM=D&M"
        elif arg1 == "" and arg2 != "":   #samo arg1 je konstanta
            return "@"+const_arg1+"\nD=A\n"+"@"+dst+"\nM=D\n"+"@"+arg2+"\nD=M\n"+"@"+dst+"\nM=D&M"
        
        elif arg1 != "" and arg2 == "":   #samo arg2 je konstanta 
            return "@"+arg1+"\nD=M\n"+"@"+dst+"\nM=D\n"+"@"+const_arg2+"\nD=A\n"+"@"+dst+"\nM=D&M"
        return "@"+arg1+"\nD=M\n"+"@"+dst+"\nM=D\n"+"@"+arg2+"\nD=M\n"+"@"+dst+"\nM=D&M" #ni arg1 ni arg2 nisu konstante
            
    elif line[0:3]=="$OR": 
        dst=self.handle_Destination(line)
        arg1=self.handle_Arg1(line)
        arg2=self.handle_Arg2(line)
        
        if arg1=="": 
            l= line.split(',')[1]
            const_arg1=l.split(')')[0]
        
        if arg2=="":
            l= line.split(',')[2]
            const_arg2=l.split(")")[0]
    
        if arg1=="" and arg2=="":    #arg1 i arg2 su konstante
            return "@"+const_arg1+"\nD=A\n"+"@"+dst+"\nM=D\n"+"@"+const_arg2+"\nD=A\n"+"@"+dst+"\nM=D|M"
        elif arg1 == "" and arg2 != "":   #samo arg1 je konstanta
            return "@"+const_arg1+"\nD=A\n"+"@"+dst+"\nM=D\n"+"@"+arg2+"\nD=M\n"+"@"+dst+"\nM=D|M"
        
        elif arg1 != "" and arg2 == "":   #samo arg2 je konstanta 
            return "@"+arg1+"\nD=M\n"+"@"+dst+"\nM=D\n"+"@"+const_arg2+"\nD=A\n"+"@"+dst+"\nM=D|M"
        return "@"+arg1+"\nD=M\n"+"@"+dst+"\nM=D\n"+"@"+arg2+"\nD=M\n"+"@"+dst+"\nM=D|M" #ni arg1 ni arg2 nisu konstante
    
    
    elif line[0:4]=="$NOT": #reverse bits
        dst=self.handle_Destination(line)
        arg1=self.handle_Arg1(line)

        if arg1=="": #argument je konstanta
            l= line.split(',')[1]
            const_arg1=l.split(')')[0]
        if arg1=="":
            return "@"+const_arg1+"\nD=A\n"+"@"+dst+"\nM=D\nM=!M"
        return "@"+arg1+"\nD=M\n"+"@"+dst+"\nM=D\nM=!M"
        
            
            
    elif line[0:4]=="$XOR":
        dst=self.handle_Destination(line)
        arg1=self.handle_Arg1(line)
        arg2=self.handle_Arg2(line)
        
        if arg1=="": 
            l= line.split(',')[1]
            const_arg1=l.split(')')[0]
        
        if arg2=="":
            l= line.split(',')[2]
            const_arg2=l.split(")")[0]
        
        if arg1=="" and arg2=="":    #arg1 i arg2 su konstante
            return "@temp5\nM=0\n"+"@"+const_arg1+"\nD=A\n"+"@temp5"+"\nM=D\n"+"@"+const_arg2+"\nD=A\n"+"@temp5"+"\nM=D|M\n"+"@"+const_arg1+"\nD=A\n"+"@"+dst+"\nM=D\nM=!M\n"+"@"+const_arg2+"\nD=A\nD=!D\n"+"@"+dst+"\nM=M|D\n"+"@temp5\nD=M\n"+"@"+dst+"\nM=M&D"
        
        elif arg1 == "" and arg2 != "":   #samo arg1 je konstanta
            return "@temp5\nM=0\n"+"@"+const_arg1+"\nD=A\n"+"@temp5"+"\nM=D\n"+"@"+arg2+"\nD=M\n"+"@temp5"+"\nM=D|M\n"+"@"+const_arg1+"\nD=A\n"+"@"+dst+"\nM=D\nM=!M\n"+"@"+arg2+"\nD=M\nD=!D\n"+"@"+dst+"\nM=M|D\n"+"@temp5\nD=M\n"+"@"+dst+"\nM=M&D"
            
        elif arg1 != "" and arg2 == "":   #samo arg2 je konstanta    
            return "@temp5\nM=0\n"+"@"+arg1+"\nD=M\n"+"@temp5"+"\nM=D\n"+"@"+const_arg2+"\nD=A\n"+"@temp5"+"\nM=D|M\n"+"@"+arg1+"\nD=M\n"+"@"+dst+"\nM=D\nM=!M\n"+"@"+const_arg2+"\nD=A\nD=!D\n"+"@"+dst+"\nM=M|D\n"+"@temp5\nD=M\n"+"@"+dst+"\nM=M&D"
                    
        return "@temp5\nM=0\n"+"@"+arg1+"\nD=M\n"+"@temp5"+"\nM=D\n"+"@"+arg2+"\nD=M\n"+"@temp5"+"\nM=D|M\n"+"@"+arg1+"\nD=M\n"+"@"+dst+"\nM=D\nM=!M\n"+"@"+arg2+"\nD=M\nD=!D\n"+"@"+dst+"\nM=M|D\n"+"@temp5\nD=M\n"+"@"+dst+"\nM=M&D"    
          
    
      
    elif line[0:3]=="$IF":
          if line[-1]=="{" and line.split("{")[1]=="":
              self.broj_otvorenih_petlji+=1
              self.petlje.append("IF")
              self.handle_cond(line)
              self.unique_key+=1
              self.stack.append("("+"END"+self.petlje[-1]+str(self.unique_key)+")")
              return "@"+self.cond+"\nD=M\n"+"@END"+self.petlje[-1]+str(self.unique_key)+"\n"+"D;JNE"
          self.petlje.append("IF")
          self.handle_cond(line)
          return ""
     
    elif line[0:10]=="$JLT_WHILE":
        self.petlje.append("JLT_WHILE")
        self.handle_cond(line)
        return ""
     
    elif line[0:6]=="$WHILE":
        if line[-1]=="{" and line.split("{")[1]=="":
              self.broj_otvorenih_petlji+=1
              self.petlje.append("WHILE")
              self.handle_cond(line)
              self.unique_key+=1
              self.stack.append("("+"END"+self.petlje[-1]+str(self.unique_key)+")")
              return "(START"+self.petlje[-1]+str(self.unique_key)+")\n"+ "@"+self.cond+"\nD=M\n"+"@END"+self.petlje[-1]+str(self.unique_key)+"\n"+"D;JEQ"
        self.petlje.append("WHILE")
        self.handle_cond(line)
        
        return ""   
    
    elif line[0]=="{" and line.split("{")[1]=="":
        self.broj_otvorenih_petlji+=1
        self.unique_key+=1
    
        if self.broj_otvorenih_petlji!=len(self.petlje):
            self._flag=False
            self._errm="Invalid loop syntax"
            return ""
        
        if self.petlje[-1]=="IF":
            self.stack.append ("(END"+self.petlje[-1]+str(self.unique_key)+")")
            return "@"+self.cond+"\nD=M\n"+"@END"+self.petlje[-1]+str(self.unique_key)+"\n"+"D;JNE"
        
        elif self.petlje[-1]=="WHILE":
            self.stack.append("("+"END"+self.petlje[-1]+str(self.unique_key)+")")
            return "(START"+self.petlje[-1]+str(self.unique_key)+")\n"+ "@"+self.cond+"\nD=M\n"+"@END"+self.petlje[-1]+str(self.unique_key)+"\n"+"D;JEQ"
        
        elif self.petlje[-1]=="JLT_WHILE":
            self.stack.append("("+"END"+self.petlje[-1]+str(self.unique_key)+")")
            return "(START"+self.petlje[-1]+str(self.unique_key)+")\n"+ "@"+self.cond+"\nD=M\n"+"@END"+self.petlje[-1]+str(self.unique_key)+"\n"+"D;JLT"
        
        
    elif line[0]=="}":
        if self.petlje[-1]=="IF":
            to_return=self.stack[-1]
            self.stack=self.stack[:-1]
            self.broj_otvorenih_petlji-=1
            self.petlje=self.petlje[:-1]
            return to_return
        
        elif self.petlje[-1]=="WHILE" or self.petlje[-1]=="JLT_WHILE":
            to_return="@START"+self.stack[-1][4:-1]+"\n0;JMP\n"+self.stack[-1]
            self.stack=self.stack[:-1]
            self.broj_otvorenih_petlji-=1
            self.petlje=self.petlje[:-1]
            return to_return
        
        
    return line        
            
            
def parse_Mult(self,line,m,n):
    line=line.replace(" ", "")
    if line[0:5]!="$MULT":
        return line
    
    dst=self.handle_Destination(line)
    arg1=self.handle_Arg1(line)
    arg2=self.handle_Arg2(line)

        
    if arg1=="": 
        l= line.split(',')[1]
        const_arg1=l.split(')')[0]
        
    if arg2=="":
        l= line.split(',')[2]
        const_arg2=l.split(")")[0]
    
    if arg1=="" and arg2=="": #arg1 i arg2 su konstante
        return "@"+dst+"\nM=0\n" +"$MV(@temp,"+const_arg2+")"+"\n$WHILE(@temp)\n{\n"+"$ADD("+"@"+dst+","+"@"+dst+","+const_arg1+")\n"+"$SUB(@temp,@temp,1)\n" +"}"
    elif arg1 == "" and arg2 != "":   #samo arg1 je konstanta
        return "@"+dst+"\nM=0\n" +"$MV(@temp,"+"@"+arg2+")"+"\n$WHILE(@temp)\n{\n"+"$ADD("+"@"+dst+","+"@"+dst+","+const_arg1+")\n"+"$SUB(@temp,@temp,1)\n" +"}"
    elif arg1 != "" and arg2 == "":   #samo arg2 je konstanta 
        return "@temp2"+"\nM=0\n" +"$MV(@temp,"+const_arg2+")"+"\n$WHILE(@temp)\n{\n"+"$ADD("+"@temp2"+","+"@temp2"+","+"@"+arg1+")\n"+"$SUB(@temp,@temp,1)\n" +"}\n$MV(@"+dst+",@temp2)"
    elif arg1!="" and arg2!="": 
        return "@temp2"+"\nM=0\n" +"$MV(@temp,"+"@"+arg2+")"+"\n$WHILE(@temp)\n{\n"+"$ADD("+"@temp2"+","+"@temp2"+","+"@"+arg1+")\n"+"$SUB(@temp,@temp,1)\n" +"}\n$MV(@"+dst+",@temp2)"
    return line


def parse_Pow(self,line,m,n):
    line=line.replace(" ", "")
    if line[0:4]!="$POW":
        return line
    
    dst=self.handle_Destination(line)
    arg1=self.handle_Arg1(line)
    arg2=self.handle_Arg2(line)

        
    if arg1=="": 
        l= line.split(',')[1]
        const_arg1=l.split(')')[0]
        
    if arg2=="":
        l= line.split(',')[2]
        const_arg2=l.split(")")[0]

    if arg1=="" and arg2=="":  #arg1 i arg2 su konstante
        return "@"+dst+"\nM=1\n" +"$MV(@temp1,"+const_arg2+")"+"\n$WHILE(@temp1)\n{\n"+"$MULT("+"@"+dst+","+"@"+dst+","+const_arg1+")\n"+"$SUB(@temp1,@temp1,1)\n" +"}"
    
    elif arg1 == "" and arg2 != "":   #samo arg1 je konstanta
        return "@"+dst+"\nM=1\n" +"$MV(@temp1,@"+arg2+")"+"\n$WHILE(@temp1)\n{\n"+"$MULT("+"@"+dst+","+"@"+dst+","+const_arg1+")\n"+"$SUB(@temp1,@temp1,1)\n" +"}"
    
    elif arg1 != "" and arg2 == "":   #samo arg2 je konstanta 
        return "@"+dst+"\nM=1\n" +"$MV(@temp1,"+const_arg2+")"+"\n$WHILE(@temp1)\n{\n"+"$MULT("+"@"+dst+","+"@"+dst+",@"+arg1+")\n"+"$SUB(@temp1,@temp1,1)\n" +"}"
    
    elif arg1!="" and arg2!="":
        return "@"+dst+"\nM=1\n" +"$MV(@temp1,@"+arg2+")"+"\n$WHILE(@temp1)\n{\n"+"$MULT("+"@"+dst+","+"@"+dst+",@"+arg1+")\n"+"$SUB(@temp1,@temp1,1)\n" +"}"
        
    return line

    
def parse_Div(self,line,m,n):
    line=line.replace(" ", "")
    if line[0:4]!="$DIV":
        return line
    
    dst=self.handle_Destination(line)
    arg1=self.handle_Arg1(line)
    arg2=self.handle_Arg2(line)
    
    if arg1=="": 
        l= line.split(',')[1]
        const_arg1=l.split(')')[0]
        
    if arg2=="":
        l= line.split(',')[2]
        const_arg2=l.split(")")[0]
    
    if arg1=="" and arg2=="":  #arg1 i arg2 su konstante
        return "@"+const_arg1+"\nD=A\n@"+const_arg2+"\nD=D-A\n@pomoc_kraj\nD;JLT\n" + "$MV(@temp4," + const_arg1 + ")\n"  + "@"+dst+"\nM=0\n"+"$MV(@temp3," + const_arg1 + ")\n"+ "$JLT_WHILE(@temp4)\n{\n"+ "$SUB(@temp3,@temp3,"+const_arg2+")\n@"+dst+"\nM=M+1\n" + "$SUB(@temp4,@temp3,"+const_arg2+")\n" +"}\n"+"(pomoc_kraj)" 
    
    elif arg1 == "" and arg2 != "":   #samo arg1 je konstanta
        return "@"+const_arg1+"\nD=A\n@"+arg2+"\nD=D-M\n@pomoc_kraj\nD;JLT\n" + "$MV(@temp4," + const_arg1 + ")\n"  + "@"+dst+"\nM=0\n"+"$MV(@temp3," + const_arg1 + ")\n"+ "$JLT_WHILE(@temp4)\n{\n"+ "$SUB(@temp3,@temp3,@"+arg2+")\n@"+dst+"\nM=M+1\n" + "$SUB(@temp4,@temp3,@"+arg2+")\n" +"}\n"+"(pomoc_kraj)"
    
    elif arg1 != "" and arg2 == "":   #samo arg2 je konstanta
        return "@"+arg1+"\nD=M\n@"+const_arg2+"\nD=D-A\n@pomoc_kraj\nD;JLT\n" + "$MV(@temp4,@" + arg1 + ")\n"  + "@"+dst+"\nM=0\n"+"$MV(@temp3,@" + arg1 + ")\n"+ "$JLT_WHILE(@temp4)\n{\n"+ "$SUB(@temp3,@temp3,"+const_arg2+")\n@"+dst+"\nM=M+1\n" + "$SUB(@temp4,@temp3,"+const_arg2+")\n" +"}\n"+"(pomoc_kraj)"
   
    elif arg1!="" and arg2!="":
        return "@"+arg1+"\nD=M\n@"+arg2+"\nD=D-M\n@pomoc_kraj\nD;JLT\n" + "$MV(@temp4,@" + arg1 + ")\n"  + "@"+dst+"\nM=0\n"+"$MV(@temp3,@" + arg1 + ")\n"+ "$JLT_WHILE(@temp4)\n{\n"+ "$SUB(@temp3,@temp3,@"+arg2+")\n@"+dst+"\nM=M+1\n" + "$SUB(@temp4,@temp3,@"+arg2+")\n" +"}\n"+"(pomoc_kraj)"
    
    
    
    
    
    
    
    