import yaml
import glob
import os

#get a list of all yaml files in data
def get_files(directory,suffix):
    path=os.path.join(directory,'*.'+suffix)
    #print(path)
    result=glob.glob(path)
    return result

def parse_yml(filepath):
    with open(filepath, 'r') as stream:
        try:
            print(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)

yml_files=get_files('data','yaml')

for f in yml_files:
    if not 'template.yaml' in f:
        parse_yml(f)

#with open("example.yaml", 'r') as stream:
#    try:
#        print(yaml.safe_load(stream))
#    except yaml.YAMLError as exc:
       # print(exc)
