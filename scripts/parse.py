'''
Execute this script from root
python scripts/parse.py
'''

import yaml
import glob
import os

datasets=[]
resources=[]


#get a list of all yaml files in data
def get_files(directory,suffix):
    path=os.path.join(directory,'*.'+suffix)
    #print(path)
    result=glob.glob(path)
    return result

def parse_yml(filepath):
    all_dict=yaml.safe_load(open(filepath))

    for key, value in all_dict.items():
        #print (key,":", value)
        #decide if entry is rna-seq or resource
        if len(value) >3 :
            #this is RNA-Seq data
            print('study:',key)
            datasets.append(value)
            
        else:
            #this is resource
            print('res:',key)
            resources.append(value)

def mdlink(text,link):
    if text==None:
        text=""
    if link==None:
        link=""
    return '['+str(text)+']'+'('+str(link)+')'

def dictionary_to_md_row(d):
    #print (d)
    #print("XXXXXXXXX")
    #parse
    title=d['title']
    link=d['link']
    desc=d['description']
    date=d['date']
    typeseq=d['type']
    geoacc=d['geo']['accession']
    geolink=d['geo']['link']
    sraacc=d['sra']['accession']
    sralink=d['sra']['link']
    otheracc=d['other']['accession']
    otherlink=d['other']['link']
    total=d['samples']['total']
    covid=d['samples']['covid']

    title=mdlink(title,link)
    download='/'.join([mdlink(geoacc,geolink),mdlink(sraacc,sralink),mdlink(otheracc,otherlink)])
    
    result='|'.join([str(date),title,desc,download,str(total),str(covid),typeseq])    
    return result



def datasets_to_tab(datalist):
    for d in datalist:
        #print (d)
        #print("XXXXXXXXX")
        #parse
        print(dictionary_to_md_row(d)) 


         
#def resources_to_tab(d):

data_dict={}
resource_dict={}

yml_files=get_files('data','yaml')
for f in yml_files:
    #print (f)
    if not 'template.yaml' in f:
        parse_yml(f)

#after parsing and creating 'datasets' and 'resources' dict, make README file

print(datasets)
print("SDSASD")
print(resources)


#convert to tab
datasets_to_tab(datasets)


