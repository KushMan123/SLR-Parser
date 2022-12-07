from flask import Flask 
from  typing import *
app = Flask(__name__)

Grammer = {}
Closures = {}
Start =  ""
Terminals = []
NonTerminasl = []
Symbols = []

#endpoints
@app.route("/find")
def Hello():
    driver()
    items()
    return Closures

def InNonTerminal(s:str)->bool:
    if s.isupper() and s not in NonTerminasl:
        return True
    else:
        return False
def InTerminal(s:str)->bool:
    if not s.isupper() and s not in Terminals:
        return True
    else:
        return False

def driver()->None:
    global Grammer,Closures,Start,Terminals,NonTerminasl,Symbols
  
    with open('grammar.txt') as file:

        grammer = file.readlines()
    head =''
    H=[]
    for prod in grammer:
        head = prod[:prod.index("->")].strip()
      
        H.append(head)
    

            
        productions=[i.strip().split(' ') for i in ''.join(prod[prod.index("->") + 2:]).split('|')]
        # print(production)
        if Start == "":
            Start = head  + "'"
            Grammer[Start] = [[head]]
        
        if head not in Grammer:
            Grammer[head] =[]#initiallizing empty list for head not in grammer so as to add when we get
        if head not in NonTerminasl:
            NonTerminasl.append(head)
        
        for p in productions:
            Grammer[head].append(p)

            for char in p:
                if InTerminal(char):
                    Terminals.append(char)
                elif InNonTerminal(char):
                    NonTerminasl.append(char)
                    # Grammer[char] =[]
    Symbols = Terminals + NonTerminasl

def find_closure(productions)->str:
    p = productions
    print(f"p -> {p}")
    while True:
        length = len(p)+sum(len(v) for v in iter(p.values()))
        print(f"length {length}")

        for heads in list(p.keys()):
      
            for prods in p[heads]:
                dot_pos = prods.index('.')
               
                if dot_pos + 1 < len(prods):
                    prod_after = prods[dot_pos+1]
                    if prod_after in NonTerminasl:
                        for prod in Grammer[prod_after]:
                            item =["."]+prod
                            if prod_after not in p.keys():
                                p[prod_after] = [item]
                            elif item not in p[prod_after]:
                                p[prod_after].append(item)
        if length == len(p)+sum(len(v) for v in iter(p.values())):
            return p

def Goto(production, sym):
    goto = {}
    for heads in list(production.keys()):
        for prods in production[heads]:
            for i in range(len(prods)-1):
                if "." == prods[i] and sym == prods[i+1]:
                    temp_prods = prods[:]
                    temp_prods[i],temp_prods[i+1] = temp_prods[i+1],temp_prods[i]
                    prod_closure  = find_closure({heads : [temp_prods]})
                    for keys in prod_closure:
                        if keys not in list(goto.keys()):
                            goto[keys] = prod_closure[keys]
                        elif prod_closure[keys] not in goto[keys]:
                            for prod in prod_closure[keys]:
                                goto[keys].append(prod)

    return goto


    






def items()->None:
    global Closures,Grammer
    Closures ={'I0':find_closure({Start:[['.']+Grammer[Start][0]]})}
    
    index =1
    while True:
        length = len(Closures)+sum(len(v) for v in iter(Closures.values()))
        for h in list(Closures.keys()):
            for s in Symbols:
                if Goto(Closures[h],s) and Goto(Closures[h],s) not in list(Closures.values()):
                    print(f"in I value {index}")
                    Closures['I'+str(index)] = Goto(Closures[h],s)
                    index+=1
                    print(Closures)

        
        if length == len(Closures)+sum(len(v) for v in iter(Closures.values())):
            return 
    
        
    



    



# print(Grammer)


if __name__=="__main__":
    app.run(debug=True)