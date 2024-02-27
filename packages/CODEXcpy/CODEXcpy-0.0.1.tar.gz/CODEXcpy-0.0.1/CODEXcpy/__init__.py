'''                         Created By : Ankit Chandok                       '''
#####################################################################################
if __name__ == '__main__':
    print()
    print('==================== Welcome to CPY Module v1.0 ====================')
    print('Type "help()", "classes()", "credits()" or "functions()" for more information.')
    print()
#####################################################################################

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
               'syntax':'pow(base,exp_default=2)'}}
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
        try:
            percent=(sequence/len(sequence)*max)*pow_default_100
            return percent
        except:
            print("NotImplemented")
#####################################################################################
    def num_filter(sequence,function_default=None):
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
        try:
            rooted_num=number**(1/root_default_2)
            return print(rooted_num)
        except:
            return print("NotImplemented")
#####################################################################################
    def pow(base,exp_default=2):
        try:
            power = base**exp_default
            return print(power)
        except:
            return print('NotImplemented')
#####################################################################################
    def fab(n,f1,f2):
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
        try:
            an_term=(a+(n-1)*d)
            return print(an_term)
        except:
            print('NotImplemented')
#####################################################################################
    def sn_term(a,d,n):
        try:
            sn_term=int(((n/2)*(2*a+(n-1)*d)))
            return print(sn_term)
        except:
            print('NotImplemented')
#####################################################################################
def out(ex='',sep='',end='',return_var=None):
    try:
        print(ex+sep+end)
    except:
        print()
def include(name,_from=None):
    try:
        if _from!=None:
            line_1='import '+_from
            line_2='from '+_from+' import '+name
            #print(line_1)
            #print(line_2)
            exec(line_1)
            exec(line_2)
        else:
            exec(f'import math')
    except:
        print("NotFound")
def inc(x):
    print(x)
    
