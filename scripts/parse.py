'''
Parse yml files to markdown
Execute this script from root
python scripts/parse.py

Urmi
'''

import yaml
import glob
import os
import sys
from operator import itemgetter


datasets=[] #is a list of lists, each inner-list is a row
resources=[] #is a list of lists
#headers
datasets_h1=['S.No.','Date','Title','Description','Download','#Samples','#COVID','Type']
datasets_h2=['---','---    ','---','---','---','---','---','---']
resources_h1=['S.No.','Resource','Description']
resources_h2=['---','---','---']


#keep track of added data
added_dataset=[]
added_resources=[]

#get a list of all yaml files in data
def get_files(directory,suffix):
    path=os.path.join(directory,'*.'+suffix)
    #print(path)
    result=glob.glob(path)
    return result

def check_duplicate_keys(yaml):
    '''
    check for duplicate keys in yaml
    return true if there are duplicate keys
    '''
    with open(yaml) as f:
        data=f.read().splitlines()
        #print(data)
    keys=[]
    duplicate=False
    for l in data:
        if not (l.startswith('#') or l.startswith(' ') or l.startswith('-') or l.startswith('\n')):
            if (l):
                #print ('keyfound:'+l)
                if l in keys:
                    duplicate=True
                    print('File: {} found duplicate key {}'.format(yaml,l))
                keys.append(l) 
    return duplicate

def parse_yml(filepath):
    all_dict=yaml.safe_load(open(filepath))

    for key, d in all_dict.items():
        #print (key,":")
        #decide if entry is rna-seq or resource
        if len(d) >3 :
            #this is RNA-Seq data
            #print('study:',key)
            #validate keys
            try:
                title=d['title']
                if title in added_dataset:
                    print("SKIPPING: {} already exists".format(title))
                    continue   
                added_dataset.append(title)
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
                download=[]
                if geoacc:
                    download.append(mdlink(geoacc,geolink))
                if sraacc:
                    download.append(mdlink(sraacc,sralink))
                if otheracc:
                    download.append(mdlink(otheracc,otherlink))
                #download=';'.join([mdlink(geoacc,geolink),mdlink(sraacc,sralink),mdlink(otheracc,otherlink)])
                #S.No. will be assigned later after sorting
                result=['0',str(date),title,desc,'<br>'.join(download),str(total),str(covid),typeseq]    
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
                if title in added_resources:
                    print("SKIPPING: {} already exists".format(title))
                    continue   
                link=d['link']
                desc=d['description']
                result=['0',mdlink(title,link),desc]
                added_resources.append(title)
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

        


yml_files=get_files('data','yaml')
for f in yml_files:
    #ignore template.yaml file
    if not 'template.yaml' in f:
        if check_duplicate_keys(f):
            print('ERROR: Please fix duplicate yaml keys in file: '+f+'. Exiting...')
            sys.exit(1)
        parse_yml(f)

#after parsing and creating 'datasets' and 'resources' dict, make README file

#print('\n'.join(datasets))
#print('\n'.join(resources))

#sort datasets by date and assign S.No.
datasets=sorted(datasets, key=itemgetter(1),reverse=True) #sort by date
resources=sorted(resources, key=itemgetter(1)) # sort by title
dind=1
#generate S.No.
for l in datasets:
    l[0]=str(dind)
    dind+=1
rind=1
for l in resources:
    l[0]=str(rind)
    rind+=1

#add headers
datasets.insert(0,datasets_h2)
datasets.insert(0,datasets_h1)
resources.insert(0,resources_h2)
resources.insert(0,resources_h1)

#write to file
print('writing to file')
#conver to md format
datasets_md=[]
for l in datasets:
    datasets_md.append('|'.join(l))
resources_md=[]
for l in resources:
    resources_md.append('|'.join(l))

data_table='\n'.join(datasets_md)
resources_table='\n'.join(resources_md)
target='README2.md'
sep='## ##'
#get content before tables e.g. introduction section
with open(target,'r') as f:
    content=f.read().splitlines()
content='\n'.join(content).split(sep)[0]
#print(content)

#write newly parsed tables along with  content
f=open(target,'w')
f.write('\n\n'.join([content+sep,'## COVID-19-RNA-Seq-datasets',data_table,'\n\n## COVID-19-RNA-Seq Resources',resources_table]))
print('Done!')



