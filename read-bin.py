#!/user/bin/env python

f=open("user_configuration.bin","rb")
num=list(f.read())
print (num)
f.close()