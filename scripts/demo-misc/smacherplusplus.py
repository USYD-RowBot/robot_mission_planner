import base64
import zlib
import urllib.parse as uparse
import re


f=open('input.xml')
data=f.read()
data=re.search('\<diagram\>(.+)\<\/diagram\>',data).group(1)
# print(data)
data=base64.b64decode(data)
data=zlib.decompress(data,-15);
data=uparse.unquote(str(data))
data=data.replace('&amp;amp;','&')
states={};
for c,i in enumerate(re.finditer("\<mxCell id=\"([^\"]+)\" value=\"([^\"]*)\" style=\"[^\"]*\" vertex=\"[^\"]*\" parent=\"[^\"]*\">",data)):
    print("Match {0}:".format(c))
    
    states[i.group(0)]={
        'name':re.split('\[|\]',i.group(1))
    
    };
    for j in i.groups():
        print(j);
        
        