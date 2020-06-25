'''
Execute this script from root
python scripts/parse.py
'''

import yaml
import glob
import os
import sys

datasets=[]
resources=[]
#add headers
datasets.append('|'.join(['Date','Title','Description','Download','#Samples','#COVID','Type'])+'\n'+'|'.join(['---','---','---','---','---','---','---']))
resources.append('|'.join(['Resource','Description']))
resources.append('|'.join(['---','---']))

#get a list of all yaml files in data
def get_files(directory,suffix):
    path=os.path.join(directory,'*.'+suffix)
    #print(path)
    result=glob.glob(path)
    return result

#def validate_keys(d,k):
#    '''
#    check d contains all k keys
#    '''
    


def parse_yml(filepath):
    all_dict=yaml.safe_load(open(filepath))

    for key, d in all_dict.items():
        #print (key,":", value)
        #decide if entry is rna-seq or resource
        if len(d) >3 :
            #this is RNA-Seq data
            #print('study:',key)
            #validate keys
            try:
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
                datasets.append(result)
                #return result
            except:
                print('1 Error parsing:'+filepath+' key:'+key)
                sys.exit(1)
            #datasets.append(value)
            
        else:
            #this is resource
            try:
                title=d['title']
                link=d['link']
                desc=d['description']
                result='|'.join([mdlink(title,link),desc])                
                resources.append(result)
            except:
                print('2 Error parsing:'+filepath+' key:'+key)
                sys.exit(1)

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

#print('\n'.join(datasets))
#print('\n'.join(resources))


#convert to tab
#data_table=datasets_to_tab(datasets)
#resources_table=resources_to_tab(resources)

#write to file
print('writing to file')
data_table='\n'.join(datasets)
resources_table='\n'.join(resources)
target='README.md'
sep='######%%%#####'
#get content before tables e.g. introduction section
with open(target,'r') as f:
    content=f.read().splitlines()
content='\n'.join(content).split('######%%%#####')[0]
print(content)

#write newly parsed tables along with  content
f=open(target,'w')
f.write('\n\n'.join([content+'\n'+sep,'## COVID-19-RNA-Seq-datasets',data_table,'\n\n## COVID-19-RNA-Seq Resources',resources_table]))
print('Done!')



