'''                         Created By : Ankit Chandok                       '''
#####################################################################################
if __name__ == '__main__':
    print()
    print('==================== Welcome to CPY Module v1.0 ====================')
    print('Type "help()", "classes()", "credits()" or "functions()" for more information.')
    print()
#####################################################################################
get,display,out,location=input,print,print,id
#####################################################################################
def help(func='Default'):
    Functions = {
        'percent':{'task':'Calculates the Percentage',
                   'syntax':'percent(sequence,max,pow_default_100=100)'},
        'num_filter':{'task':'Returns Filtered Sequence List/Tuple',
                      'syntax':'num_filter(sequence,function_default=None)'},
        'calculate':{'task':'Calculates the Given Expression',
                     'syntax':'calculate(expression)'},
        'root':{'task':'Returns the Root of Number',
                'syntax':'root(number,root_default_2=2)'},
        'pow':{'task':'Returns the Power of Number',
               'syntax':'pow(base,exp_default=2)'},
        'fab':{'task':'Gives the Fabbbonaci Series',
               'syntax':'fab(n,f1,f2)'},
        'factorial':{'task':'Gives the Factorial of the Number',
                     'syntax':'factorial(number)'},
        'ap':{'task':'Gives the AP',
              'syntax':'ap(a,d_default=1,n_default=10)'},
        'sn_ap':{'task':'Gives the Sum of the given AP',
                 'syntax':'sn_ap(ap,n_default=10)'},
        'sn':{'task':'Gives the sum of the AP',
              'syntax':'sn(a,d_default=1,n_default=10)'},
        'an_term':{'task':'Finds out the nth term of AP',
                   'syntax':'an_term(a,d,n)'},
        'sn_term':{'task':'Finds out the nth term of SN of AP',
                   'syntax':'sn_term(a,d,n)'}}
    try:
        if func == 'Default':
            return print('Write Function Name inside help() to know about that Function .')
        elif func == '*':
            return print(f'Functions = {Functions}')
        elif func in Functions:
            print(f'''
Function Name = {func}
task = {Functions[func]['task']}
syntax = {Functions[func]['syntax']}
''')
        else:
            print("Please check the Function name .")
    except:
        print('TryAgain')
#####################################################################################
def credits():
    print()
    print("                    Created By : Ankit Chandok                   ")
    print()
#####################################################################################
def classes():
    Classes = {
        "PyMath":"Math Methods"
        }
    return print(f"Classes = {Classes}")
class Credits:
#####################################################################################
    def creator():
        print("Creator of CPY Module : Ankit Chandok")
#####################################################################################
class PyMath:
#####################################################################################
    def percent(sequence,max,pow_default_100=100):
        '''Use percent() function to calculate the Percentage'''
        try:
            percent=(sum(sequence)/(len(sequence)*max))*pow_default_100
            return percent
        except:
            print("NotImplemented")
#####################################################################################
    def num_filter(sequence,function_default=None):
        '''Use num_filter() function to Filter the sequence by giving condition as Function'''
        try:
            if function_default==None:
                return print(sequence)
            elif function_default!=None and type(sequence)==type([1,2]):
                out_sequence=[]
                for _check_ in sequence:
                    _input_=_check_
                    output=function_default(_input_)
                    if output==True:
                        out_sequence.append(_check_)
                    elif output==False:
                        pass
                return print(out_sequence)
            elif function_default!=None and type(sequence)==type((1,2)):
                out_sequence=()
                for _check_ in sequence:
                    _input_=_check_
                    output=function_default(_input_)
                    if output==True:
                        out_sequence=out_sequence+(_check_,)
                    elif output==False:
                        pass
                return print(out_sequence)
        except:
            print('NotImplemented')
#####################################################################################
    def calculate(expression):
        '''Use calculate() function to calculate the given Expression'''
        try:
            ex_list=expression.split()
            add_list=[]
            sub_list=[]
            for ex in ex_list:
                if ex[0]=="+" and "*" not in ex and "/" not in ex:
                    add_list.append(int(ex[1:]))
                elif ex[0]=="-" and "*" not in ex and "/" not in ex:
                    sub_list.append(int(ex[1:]))
                elif ex[0]=="+" and "*" in ex or "/" in ex:
                    new,next_x='',''
                    count=-1
                    mul=False
                    for x in ex[1:]:
                        count=count+1
                        if mul:
                            if x!="/" and x!="*":
                                next_x=next_x+x
                                continue
                            elif x=='*' or x=='/':
                                mul=False
                                new=int(new) * int(next_x)
                                next_x=''
                        if x=="*":
                            mul=True
                        else:
                            new = new+x
                    add_list.append(int(new) * int(next_x) )
            add=sum(add_list)
            sub=sum(sub_list)
            solution=add-sub
            return print(solution)    
        except:
            print("NotImplemented")
#####################################################################################
    def root(number,root_default_2=2):
        '''Use root() function to find root'''
        try:
            rooted_num=number**(1/root_default_2)
            return print(rooted_num)
        except:
            return print("NotImplemented")
#####################################################################################
    def pow(base,exp_default=2):
        '''Use pow() function to take power of the Number'''
        try:
            power = base**exp_default
            return print(power)
        except:
            return print('NotImplemented')
#####################################################################################
    def fab(n,f1,f2):
        '''Use fab() function to find Fibonaaci Series'''
        try:
            def fabs(n,f1,f2):
                print(f1,f2,end=' ')
                f1 = f2+f1
                f2 = f1+f2
                n=n-1
                if n != 0:
                   fabs(n,f1,f2)
                else:
                   print(f1,f2,end=' ')
            n=int(n-1)
            return fabs(n,f1,f2)
        except:
            print("NotImplemented")
#####################################################################################
    def factorial(number):
        '''Use factorial() function to find Factorial of Number'''
        try:
            fact=1
            while number:
                fact=fact*number
                number-=1
            return print(fact)
        except:
            return print('NotImplemented')
#####################################################################################
    def ap(a,d_default=1,n_default=10):
        '''Use ap() function to find AP'''
        try:
            ap_out=''
            for i in range(n_default):
                ap_input=a+(i)*d_default
                ap_out=ap_out+str(int(ap_input))+', '
            ap_out=ap_out+'....'
            return print(ap_out)
        except:
            print('NotImplemented')
#####################################################################################
    def sn_ap(ap,n_default=10):
        '''Use sn_ap() function to find Sum of AP from given AP'''
        try:
            if (ap[1]-ap[0])==(ap[2]-ap[1]):
                d=ap[1]-ap[0]
                sn_output=''
                for i in range(n_default):
                    sn_input=int(((i+1)/2)*(2*ap[0]+(i)*d))
                    sn_output=sn_output+str(sn_input)+', '
                sn_output=sn_output+'....'
                return print(sn_output)
            else:
                print('NotImplemented')
        except:
            print('NotImplemented')
#####################################################################################
    def sn(a,d_default=1,n_default=10):
        '''Use sn() function to find Sum of AP'''
        try:
            sn_output=''
            for i in range(n_default):
                sn_input=int(((i+1)/2)*(2*a+(i)*d_default))
                sn_output=sn_output+str(sn_input)+', '
            sn_output=sn_output+'....'
            return print(sn_output)
        except:
            print('NotImplemented')
#####################################################################################
    def an_term(a,d,n):
        '''Use an_term() function to find nth term of AP'''
        try:
            an_term=(a+(n-1)*d)
            return print(an_term)
        except:
            print('NotImplemented')
#####################################################################################
    def sn_term(a,d,n):
        '''Use sn_term() function to find sn nth term of AP'''
        try:
            sn_term=int(((n/2)*(2*a+(n-1)*d)))
            return print(sn_term)
        except:
            print('NotImplemented')
#####################################################################################
    def arrange(sequence,arrange=None):
        '''Use arrange() function to arrange the sequence in Ascending or Descending Order'''
        try:
            if arrange==None and ( type(sequence)==type([1,2]) or type(sequence)==type((1,2))):
                return sequence
            elif arrange!=None and ( type(sequence)==type([1,2]) or type(sequence)==type((1,2))):
                if arrange.lower() in ['a','ascending']:
                    new=[]
                    sequence=list(sequence)
                    while len(sequence)!=0:
                        new.append(sequence.pop(sequence.index(min(sequence))))
                    return new
                elif arrange.lower() in ['d','descending']:
                    new=[]
                    sequence=list(sequence)
                    while len(sequence)!=0:
                        new.append(sequence.pop(sequence.index(max(sequence))))
                    return new
                else:
                    return sequence
            else:
                return print("NotImplemented")
        except:
            return print('NotImplemented')
#####################################################################################
    def rev(sequence):
        '''Use rev() function to reverse the sequence'''
        try:
            sequence=list(sequence)
            rev_list=[]
            for el in range(len(sequence)):
                rev_list.append(sequence.pop())
            return rev_list
        except:
            return print("NotImplemented")
#####################################################################################
    def pickout(sequence,x=None,index_or_value_or_max_or_min=None):
        '''Use pickout() function to pick out the item and store it in valriable also gets removed from sequence'''
        try:
            sequence=list(sequence)
            if index_or_value_or_max_or_min==None and x==None:
                return sequence.pop()
            elif str(x).lower() in ['min','max'] and index_or_value_or_max_or_min==None:
                if str(x).lower()=='min':
                    return sequence.pop(sequence.index(min(sequence)))
                elif str(x).lower()=='max':
                    return sequence.pop(sequence.index(max(sequence)))
            elif index_or_value_or_max_or_min==None and x not in ['min','max']:
                return print("NotImplemented")
            else :
                if index_or_value_or_max_or_min.lower() in ['min',None] and x in ['min']:
                    return sequence.pop(sequence.index(min(sequence)))
                elif index_or_value_or_max_or_min.lower() in ['max',None] and x in ['max']:
                    return sequence.pop(sequence.index(max(sequence)))
                elif index_or_value_or_max_or_min.lower() == 'index':
                    if len(sequence)>int(x):
                        return sequence.pop(int(x))
                    elif len(sequence)<=int(x):
                        return sequence.pop()
                elif index_or_value_or_max_or_min.lower() == 'value':
                    if x in sequence:
                        return sequence.pop(sequence.index(x))
                    else:
                        return print("NotImplemented")
        except:
            print('NotImplemented')
#####################################################################################
    def rm_duplicate(sequence):
        '''Use rm_duplicate() function to remove duplicate items from sequence'''
        try:
            if type(sequence)==type([1,2]):
                return list(set(sequence))
            elif type(sequence)==type((1,2)):
                return tuple(set(sequence))
            else:
                return print('NotImplemented')
        except:
            return print('NotImplemented')
#####################################################################################
    def update(sequence,from_sequence):
        '''Use update() function to update the sequence from another sequence'''
        pass
#####################################################################################
    def el_counter(sequence):
        '''Use el_counter() function to count no of each item/el/ch in sequence'''
        try:
            D_count={}
            sequence=list(sequence)
            for el in sequence:
                D_count[el]=sequence.count(el)
            return D_count
        except:
            return print('NotImplemented')
#####################################################################################
    def modulus(x):
        '''Use modulus() function to take modulus'''
        try:
            if type(x)==type(2) or type(x)==type(4.2):
                if str(x)[0]=='-':
                    if type(x)==type(2):
                        return int(str(x)[1:])
                    elif type(x)==type(4.2):
                        return float(str(x)[1:])
                else:
                    return x
            elif type(x)==type([1,2]) or type(x)==type((1,2)):
                if type(x)==type([1,2]):
                    new_x=[]
                    for i in x:
                        if str(i)[0]=='-':
                            if type(i)==type(2):
                                new_x.append(int(str(i)[1:]))
                            elif type(i)==type(4.2):
                                new_x.append(float(str(i)[1:]))
                        else:
                            new_x.append(i)
                    return new_x
                else:
                    new_x=[]
                    for i in x:
                        if str(i)[0]=='-':
                            if type(i)==type(2):
                                new_x.append(int(str(i)[1:]))
                            elif type(i)==type(4.2):
                                new_x.append(float(str(i)[1:]))
                        else:
                            new_x.append(i)
                    return tuple(new_x)
            else:
                return print('NotImplemented')
        except:
            return print('NotImplemented')
#####################################################################################
    def inverse(x):
        '''Use inverse() function to inverse the signs'''
        try:
            if type(x)==type(2) or type(x)==type(4.2):
                if str(x)[0]=='-':
                    if type(x)==type(2):
                        return int(str(x)[1:])
                    elif type(x)==type(4.2):
                        return float(str(x)[1:])
                else:
                    if type(x)==type(2):
                        return int('-'+str(x))
                    elif type(x)==type(4.2):
                        return float('-'+str(x))
            elif type(x)==type([1,2]) or type(x)==type((1,2)):
                if type(x)==type([1,2]):
                    new_x=[]
                    for i in x:
                        if str(i)[0]=='-':
                            if type(i)==type(2):
                                new_x.append(int(str(i)[1:]))
                            elif type(i)==type(4.2):
                                new_x.append(float(str(i)[1:]))
                        else:
                            if type(i)==type(2):
                                new_x.append(int('-'+str(i)))
                            elif type(i)==type(4.2):
                                new_x.append(float('-'+str(i)))
                    return new_x
                else:
                    new_x=[]
                    for i in x:
                        if str(i)[0]=='-':
                            if type(i)==type(2):
                                new_x.append(int(str(i)[1:]))
                            elif type(i)==type(4.2):
                                new_x.append(float(str(i)[1:]))
                        else:
                            if type(i)==type(2):
                                new_x.append(int('-'+str(i)))
                            elif type(i)==type(4.2):
                                new_x.append(float('-'+str(i)))
                    return tuple(new_x)
            else:
                return print('NotImplemented')
        except:
            return print("NotImplemented")
#####################################################################################
Function=[
    'percent',
    'num_filter',
    'calculate',
    'root',
    'pow',
    'fab',
    'factorial',
    'ap',
    'sn_ap',
    'sn',
    'an_term',
    'sn_term',
    'arrange',
    'rev',
    'pickout',
    'rm_duplicate',
    'update',
    'el_counter',
    'modulus',
    'inverse'
]    
def about():
    try:
        count=1
        for func in Function:
            print(f'{count}  {func}')
            count=count+1
    except:
        print()
##################################################################################### 
# More Functions will Come Soon 
#####################################################################################
