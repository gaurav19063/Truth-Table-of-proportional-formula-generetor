


def replace_operator(operand1,operand2,operator): # changing the operator
    if  operator =='.':
        return ' ( '+operand1 +' and '+operand2+' ) '
    elif  operator =='+':
        return ' ( '+operand1 +' or '+operand2+' ) '
    elif  operator =='*':
        return ' ( '+' not '+operand1 +' or '+operand2+' ) '
    elif  operator =='==':
        return ' ( ( '+' not '+operand1 +' or '+operand2+' ) '+' and '+' ( '+' not '+operand2 +' or '+operand1+' ) ) '
def convert_dnf_natural(operand_Stack):  #to convert eval() known operators
    dnf_formula_chars=[]
    for ch in (operand_Stack[0].split()):
        # print(ch)
        if ch=='not':
            dnf_formula_chars.append(' ~ ')
        elif ch=='or':
            dnf_formula_chars.append(' + ')
        elif ch=='and':
            dnf_formula_chars.append(' . ')
        else:
            dnf_formula_chars.append(ch)
    str=""
    for x in dnf_formula_chars:
        str=str+x
    return str
def convert_dnf_valued(operand_Stack,list_operands,bits):  #converting to eval known form and replacing all operands to their bits values
    dnf_formula_chars=[]
    for ch in (operand_Stack[0].split()):
        # print(ch)
        if ch=='not':
            dnf_formula_chars.append(' not ')
        elif ch=='or':
            dnf_formula_chars.append(' or ')
        elif ch=='and':
            dnf_formula_chars.append(' and ')
        elif ch=='(':
            dnf_formula_chars.append(' ( ')
        elif ch==')':
            dnf_formula_chars.append(' ) ')
        else:
            ch_index=list_operands.index(ch)
            if(bits[ch_index]=='0'):
                dnf_formula_chars.append(" False ")
            else:
                dnf_formula_chars.append(" True ")

    str=""
    for x in dnf_formula_chars:
        str=str+x
    return str
def find_product(bits,list_operands):   #finding single product
    product=[]
    product.append( ' ( ')
    for i in range(len(bits)):
        if bits[i] == '0':
            product.append('~'+list_operands[i])
        else:
            product.append(list_operands[i])
        if(i<len(bits)-1):
            product.append(' . ')
    product.append(' ) ')
    return product
def convertToDnf(formula):
    formula_chars = [char for char in formula]                  #changing formula characters to a list
    l=len(formula_chars)
    if(formula_chars[0]!='('):
        formula_chars.append(')')
        formula_chars.insert(0,'(')

    k=0
    for i in range(l-1):
        if(formula_chars[i]=='~' and (formula_chars[i+1]!='(')):   #handling negetion
            formula_chars[i+1]='~'+formula_chars[i+1]
            del formula_chars[i]
            k=k+1
    operator_list=['~','.','+','*','==']
    operator_Stack = []   #defining stacks for operator and operands
    operand_Stack = []
    flag = 0
    temp_list=[]
    flag=0
    for i in range(len(formula_chars)):
        if formula_chars[i]=='=':
            flag=flag+1
            if flag==2:
                temp_list.append(formula_chars[i]+formula_chars[i])
                flag=0
            continue
        temp_list.append(formula_chars[i])
    formula_chars=temp_list
    for i in range(len(formula_chars)):
        c = formula_chars[i]
        if (formula_chars[i] == '('):      #pushing '(' simply
            operator_Stack.append('(')
            continue
        elif(formula_chars[i]==')'):                              #poping whwn ')' encounters
            if(operator_Stack[len(operator_Stack)-1]=='~'):
                operator_Stack.pop()
                operator_Stack.pop()
                val=operand_Stack.pop()
                operand_Stack.append('('+' not '+val+' ) ')
                continue
            operand2=operand_Stack.pop()
            operand1=operand_Stack.pop()
            operator=operator_Stack.pop()
            operator_Stack.pop()
            operand_Stack.append(replace_operator(operand1,operand2,operator))    #evaluating with operands with operator and push to the stack
            continue
        if c in operator_list:
            operator_Stack.append(c)
        else:
            operand_Stack.append(c)
    while(len(operator_Stack)!=0):
        opr=operator_Stack.pop()
        if(opr=='~'):
            operand_Stack.append('('+' not '+operand_Stack.pop())
            operator_Stack.pop()
        else:
            operand2=operand_Stack.pop()
            operand1=operand_Stack.pop()
            operator_Stack.pop()
            operand_Stack.append(replace_operator(operand1,operand2,opr))

    #############################################################################

    dnf_formula_chars=convert_dnf_natural(operand_Stack)    #converting to reduced formula
    reduced_formula=dnf_formula_chars
    list_operands=[]
    for ch in formula_chars:
        if ch not in operator_list+['(',')']:
            list_operands.append(ch)
    list_operands=list(set(list_operands))
    list_operands.sort()                                  #all operand list
    products=[]
    j=0
    for i in range (pow(2,len(list_operands))):       #running all bits combinations to evaluate dnf using eval function
        bits="{0:b}".format(i)
        bits = [char for char in bits]
        l = len(list_operands) - len(bits)
        temp = ['0'] * l
        bits = temp + bits
        dnf_formula_chars1 = convert_dnf_valued(operand_Stack,list_operands,bits)
        evaluation=str(eval(dnf_formula_chars1))
        if j==0:
            print("###########Truth Table##########")    #Generating Truth table with eval function
            print(list_operands,"   Formula value ")
            j=j+1
        print(bits,"   ",evaluation)
        if  evaluation=='True':
            products =products+ find_product(bits,list_operands)
            products=products+[' + ']
    temp_dnf=""
    for t in products:
        temp_dnf=temp_dnf+t
    temp_dnf=temp_dnf[0:-2]
    temp_dnf_2 = [char for char in temp_dnf]
    for i in range (len(temp_dnf_2)):
        if(temp_dnf_2[i]=='~' and temp_dnf_2[i+1]=='~'):
            temp_dnf_2[i]=""
            temp_dnf_2[i+1]=""
    final_dnf=""
    for ch in temp_dnf_2:
        final_dnf=final_dnf+ch
    print("DNF formula:   ", final_dnf)
    print("Reduced Formula:   ", reduced_formula)

print("Please Use optimal parentheses otherwise error may occur")
print ("Enter your formula:")
formula=input()

convertToDnf(formula)


