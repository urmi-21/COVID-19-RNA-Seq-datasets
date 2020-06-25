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
    #if none return header
    if not d:
        return '|'.join(['Date','Title','Description','Download','#Samples','#COVID','Type'])+'\n'+'|'.join(['---','---','---','---','---','---','---'])
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
    header=dictionary_to_md_row(None)
    rows=[]
    rows.append(header)
    for d in datalist:
        rows.append(dictionary_to_md_row(d))

    return('\n'.join(rows))
         
def resources_to_tab(rlist):
    rows=[]
    rows.append('|'.join(['Resource','Description']))
    rows.append('|'.join(['---','---']))
    for d in rlist:
        title=d['title']
        link=d['link']
        desc=d['description']
        rows.append('|'.join([mdlink(title,link),desc]))
    return('\n'.join(rows))
        

data_dict={}
resource_dict={}

yml_files=get_files('data','yaml')
for f in yml_files:
    #print (f)
    if not 'template.yaml' in f:
        parse_yml(f)

#after parsing and creating 'datasets' and 'resources' dict, make README file

#print(datasets)
#print(resources)


#convert to tab
data_table=datasets_to_tab(datasets)
resources_table=resources_to_tab(resources)
#write to file
with open('README.md','r') as f:
    content=f.read().splitlines()
content='\n'.join(content).split('######%%%#####')[0]
#print(content)
f=open('RM2.md','w')
f.write('\n\n'.join([content,'## COVID-19-RNA-Seq-datasets',data_table,'\n\n## COVID-19-RNA-Seq Resources',resources_table]))
print('Done!')
