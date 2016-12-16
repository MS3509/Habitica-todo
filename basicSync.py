#!/usr/bin/env python

"""
Fuck it, I need to just get something quick and dirty that will WORK. More features to come later.
"""

#Python library imports - this will be functionalities I want to shorten
from habitica import api #Note: you will want to get a version with API 3 support. At the time of this writing, check submitted pulls on the Github. 
from os import path # will let me call files from a specific path
import requests
import scriptabit
import pickle
import todoist
from hab_task import HabTask
from todo_task import TodTask
import main
import random

from subprocess import call # useful for running command line commands in python
from urllib2 import urlopen
from bisect import bisect
import json
import logging
import netrc
import sys 
from time import sleep
from webbrowser import open_new_tab
from docopt import docopt
from pprint import pprint

#Here's where I'm putting my login stuff for Todoist.
tod_user = main.tod_login('auth.cfg')
tod_projects = tod_user.projects.all()
tod_inboxID = tod_projects[0].data['id']

#Telling the site where the config stuff for Habitica can go and get a list of habitica tasks...
auth, hbt = main.get_started('auth.cfg')  

#Todoist tasks are, I think, classes. Let's make Habitica tasks classes, too.
url = 'https://habitica.com/api/v3/tasks/user/'
response = requests.get(url,headers=auth)
hab_raw = response.json()
hab_tasklist = hab_raw['data'] #FINALLY getting something I can work with... this will be a list of dicts I want to turn into a list of objects with class hab_tasks. Hrm. Weeeelll, if I make a class elsewhere....

#keeping records of all our tasks
hab_tasks = [] 

#No habits right now, I'm afraid, in hab_tasks--Todoist gets upset. So we're going to make a list of dailies and todos instead...
for task in hab_tasklist: 
    item = HabTask(task)
    if item.category == 'reward':
        pass
    elif item.category == 'habit': 
        pass
    else:
        hab_tasks.append(item)

#Okay, now I need a list of todoist tasks. How do achieve that. 
tod_tasks = []
tod_items = tod_user.items
tod_tasklist = tod_items.all()
for i in range(0, len(tod_tasklist)):
    tod_tasks.append(TodTask(tod_tasklist[i].data))

"""
Okay, I want to write a little script that checks whether or not a task is there or not and, if not, ports it. 	
"""

pkl_file = open('habtod_matchDict.pkl','rb')
try: 
    matchDict = pickle.load(pkl_file)
except:
    matchDict = {}

pkl_file.close()

#Right. That needs to happen. Use the hab and tod tasks to update our dictionaries... 

#We'll want to just... pull all the unmatched tasks out of our lists of tasks. Yeah? 
tod_uniq, hab_uniq = main.get_uniqs(matchDict, tod_tasks, hab_tasks)

#check to pull out all the unmatched tasks we DON'T see in matchDict, our dictionary of paired habitica and todoist tasks
for tod_task in tod_uniq:
    for hab_task in hab_uniq:
        if tod_task.name == hab_task.name:
            tid = tod_task.id
            matchDict[tid] = {}
            matchDict[tid]['hab'] = hab_task
            matchDict[tid]['tod'] = tod_task
            main.add_hab_id(tid,hab_task)

tod_uniq, hab_uniq = main.get_uniqs(matchDict, tod_tasks, hab_tasks)

#Now we've confirmed that we don't have any accidental duplicates and that previously sent tasks are all knocked out of the way, it's time to add copies of the individual tasks...
for i in tod_uniq:
    hab = main.make_hab_from_tod(i)
    main.write_hab_task(hbt,hab)
'''    if ev in i.date_string:
        hab = main.make_daily_from_tod(i)
        main.write_hab_daily(hbt, hab)
    else:
        main.write_hab_todo(hbt,task)'''
    
#I'm just assuming that all these tasks can be dumped in the inbox. See above for todoist Inbox ID code, which is located under login
for task in hab_uniq:
    if task.category== "daily":
        tod_user.items.add(task.name,tod_inboxID,date_string=task.dailies_due)
    else:
        tod_user.items.add(task.name,tod_inboxID)

#I also want to make sure that any tasks which are checked off AND have paired tasks agree on completion.
#If one is checked complete, both should be...
for t in matchDict: #make sure neither of these are used elsewhere in code
    
    if matchDict[t]['tod'].complete == 0: 
        if matchDict[t]['hab'].completed == False: 
            pass
        elif matchDict[t]['hab'].completed == True: 
            tid = matchDict[t]['tod'].id
            tod = tod_items.get_by_id(tid)
            tod.complete()
        else:
            print("Hey, something's fishy here. Check out the Habitica task?")
            print(matchDict[t]['hab'].name)
    elif matchDict[t]['tod'].complete == 1:
        print(matchDict[t]['tod'])
#        if matchDict[t]['hab'].completed == True:
#            pass
#        elif matchDict[t]['hab'].completed == False: 
#            main.complete_hab_todo(hbt,matchDict[t]['hab'])
#        else:
#            print("Hey, something's fishy here. Check out the Habitica task?")            
#            print(matchDict[t]['hab'].name)
    else:
        print("uh, something's weird here. Check out the Todoist task?")
        print(matchDict[t]['tod'])

#Wrapping it all up: saving matchDict, committing changes to todoist
pkl_out = open('habtod_matchDict.pkl','w')
pickle.dump(matchDict, pkl_out)
pkl_out.close()
tod_user.commit()