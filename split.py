import encodings
from encodings.utf_8 import encode
import json



with open('test.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

keys = [key for key in json_data]
i=0
k=0

data_list={}



for key in keys[:]:
    for data in json_data[key]:
        #print(data["title"])
        contents = data["title"]
        i=i+1
        #(영문명, icid)로 되어있는 데이터만 수집하였다. 
        if("kqc" in contents.lower() and contents.count('(')==1 and contents.count(',')):
            content = contents.split('(')[1].split(',')[0]
            if(("kqc" not in content.lower()) and 'a'<content.lower()[0]<'z'):
                data_list[content]={"id":k}
                k=k+1
        elif("icid" in contents.lower()):
            i
print(k)
file_path='./kqcData.json'
with open(file_path, 'w') as outfile:
    json.dump(data_list, outfile)
print(data_list)
print(i)

