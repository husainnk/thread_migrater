

import random
import pprint
import subprocess
import sys
import os
import json




#python3 ~/TransProc/criu-3.15/crit/crit show pstree.img

CRIT_PATH ="/users/nkhusain/TransProc/criu-3.15/crit/crit"
img =  "pstree.img"
TARGET_THREAD = 1

show_cmd = "python3 "+ CRIT_PATH + " show " + img ;
print(show_cmd)

show_out  = subprocess.run(show_cmd.split(' '),stdout=subprocess.PIPE)
show_out = show_out.stdout.decode("utf-8")

pstree_object = json.loads(show_out)

threads_list = pstree_object['entries'][0]['threads']

new_list  = []
new_list.append(threads_list[0])

pstree_object['entries'][0]['threads'] = new_list	
print(pstree_object)

json_data = json.dumps(pstree_object, indent=4)
f = open('pstree.json', 'w')
f.write(json_data)
f.close()

dump_cmd = "python3 "+ CRIT_PATH + " encode -i pstree.json -o " + img ;
dump_out = subprocess.run(dump_cmd.split(' '),stdout=subprocess.PIPE)
dump_out = dump_out.stdout.decode("utf-8")

print(dump_out)



PID=threads_list[0]


show_cmd = "python3 "+ CRIT_PATH + " show " + "core-" + str(PID) +".img" ;

show_out  = subprocess.run(show_cmd.split(' '),stdout=subprocess.PIPE)
show_out = show_out.stdout.decode("utf-8")

core_main_object = json.loads(show_out)

tc_object = core_main_object['entries'][0]['tc'];

PID=threads_list[1]
show_cmd = "python3 "+ CRIT_PATH + " show " + "core-" + str(PID) +".img" ;
show_out  = subprocess.run(show_cmd.split(' '),stdout=subprocess.PIPE)
show_out = show_out.stdout.decode("utf-8")

core_thread_object = json.loads(show_out)
core_thread_object['entries'][0]['tc'] = tc_object
json_data = json.dumps(core_thread_object, indent=4)

f = open('thread.json', 'w')
f.write(json_data)
f.close()

dump_cmd = "python3 "+ CRIT_PATH + " encode -i thread.json -o " +  "core-" + str(threads_list[0]) +".img" ;
dump_out = subprocess.run(dump_cmd.split(' '),stdout=subprocess.PIPE)
dump_out = dump_out.stdout.decode("utf-8")

print(dump_out)


if os.path.exists("thread.json"):
	os.remove("thread.json")
if os.path.exists("pstree.json"):
	os.remove("pstree.json")

