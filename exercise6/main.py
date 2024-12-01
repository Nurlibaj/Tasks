def exercise1(a,b):
    return "exercise1:"+str(a+b)
def exercise2(s):
    return "exercise2: "+s[::-1]
def exercise3(s):
    return "exercise3: "+str(len(s))
def exercise4(s1,s2):
    return "exercise4: "+s1+s2
def exercise5(c):
    c=c.lower()
    if c=="a" or c=="e" or c=="y" or c=="i" or c=="o" or c=="u":
        return "exercise5: True"
    else:
        return "exercise5: False"
def exercise6(s):
    new_string=s[-1]+s[1:-1]+s[0]
    return "exercise6:"+new_string
def exercise7(s):
    return "exercise7:"+s.upper()
def exercise8(length,width):
    return "exercise8: area="+str(length*width)
def exercise9(number):
    if number%2==0:
        return "exercise9:"+str(number)+"is even"
    else:
        return "exercise9:"+str(number)+"is not even"
def exercise10(s):
    return "exercise10:"+s[:3]
def exercise11(name,age):
    return "exercise11:" f'My name is {name} and  i am {age} years old.'
def exercise12(s):
    return "exercise12: "+ s[2:6]
def exercise13(num):
    new_num=int(num)
    return "exercise13: "+ str(new_num)
def exercise14(s):
    s=s*3
    return "exercise14: " + s
def exercise15(a,b):
    return "exercise15: "+ str(a//b)+","+str(a%b)
def exercise16(a,b):
    return "exercise16: " + str(a/b)
def exercise17(string,character):
    return "exercise17:"+str(string.count(character))
def exercise18():
    s="exercise18:Hello, \" world!\""
    return s
def exercise19():
    s="""exercise19:Hello, world!
    nFactorial
    Batch106"""
    return s
def exercise20(base,exponent):
    return "exercise20: "+str(base**exponent)
def exercise21(s):
    reverse=s[::-1]
    if s==reverse:
        return "exercise21: string "+s+" is palindrom"
    else:
        return "exercise21: string "+s+" is not palindrom"
def exercise22(s1,s2):
    s1=s1.lower()
    s2=s2.lower()
    if s1==s2:
        return "exercise22: they are anagram"
    else:
        return "exercise22: they aren't not anagram"   
if __name__ == "__main__":
    print(exercise1(2,3))
    print(exercise2("Python"))
    print(exercise3("Astana"))
    print(exercise4("Hello","World!"))
    print(exercise5("a"))
    print(exercise6("Python"))
    print(exercise7("nFactorial"))
    print(exercise8(5,4))
    print(exercise9(23))
    print(exercise10("Python"))
    print(exercise11("Naruto",40))
    print(exercise12("Madara"))
    print(exercise13("13"))
    print(exercise14("Python"))
    print(exercise15(5,2))
    print(exercise16(5,2))
    print(exercise17("Hello,World!","o"))
    print(exercise18())
    print(exercise19())
    print(exercise20(2,3))
    print(exercise21("Kazak"))
    print(exercise22("nis","SiN"))
    
    
