#!/usr/bin/env python

"""
Main.py overdue for an overhaul! Let's see.
"""

"""Here's where we import stuff we need..."""
import todoist
from habitica import api 
import requests
import json
from hab_task import HabTask
from todo_task import TodTask
import os
import logging
try:
    import ConfigParser as configparser
except:
    import configparser	



"""
Version control, basic paths
"""

VERSION = 'Habitica-todo version 0.1.0'
TASK_VALUE_BASE = 0.9747  # http://habitica.wikia.com/wiki/Task_Value
HABITICA_REQUEST_WAIT_TIME = 0.5  # time to pause between concurrent requests
HABITICA_TASKS_PAGE = '/#/tasks'
# https://trello.com/c/4C8w1z5h/17-task-difficulty-settings-v2-priority-multiplier
PRIORITY = {'easy': 1,
            'medium': 1.5,
            'hard': 2}
AUTH_CONF = os.path.expanduser('~') + '/.config/habitica/auth.cfg'
CACHE_CONF = os.path.expanduser('~') + '/.config/habitica/cache.cfg'

SECTION_CACHE_QUEST = 'Quest'

"""
Small utilities written by me start here.
"""

def tod_login(configfile):
    logging.debug('Loading todoist auth data from %s' % configfile)

    try:
        cf = open(configfile)
    except IOError:
        logging.error("Unable to find '%s'." % configfile)
        exit(1)

    config = configparser.SafeConfigParser()
    config.readfp(cf)

    cf.close()

    # Get data from config
    try:
        rv = config.get('Todoist', 'api-token')

    except configparser.NoSectionError:
        logging.error("No 'Todoist' section in '%s'" % configfile)
        exit(1)

    except configparser.NoOptionError as e:
        logging.error("Missing option in auth file '%s': %s" % (configfile, e.message))
        exit(1)
    
    tod_user = todoist.TodoistAPI(rv)
    #tod_user = todoist.login_with_api_token(rv)
    # Return auth data
    return tod_user

def get_started(config):
    """
    Intended to get everything up and running for a first pass. This should run first. 
    """
    from main import load_auth
    from habitica import api 
    auth = load_auth(config)
    hbt = api.Habitica(auth=auth)
    return auth, hbt 

def make_daily_from_tod(tod_task):
    new_hab = {'type':'daily'}
    new_hab['text'] = tod_task.name
    new_hab
    if tod_task.priority == 1:
        new_hab['priority'] = 2
    elif tod_task.priority == 2:
        new_hab['priority'] = 1.5
    elif tod_task.priority == 3:
        new_hab['priority'] = 1
    elif tod_task.priority == 4:
        new_hab['priority'] = .1
    return new_hab

def make_hab_from_tod(tod_task):
    new_hab = {'type':'todo'}
    new_hab['text'] = tod_task.name
    new_hab['date'] = tod_task.due_date
    if tod_task.priority == 1:
        new_hab['priority'] = 2
    elif tod_task.priority == 2:
        new_hab['priority'] = 1.5
    elif tod_task.priority == 3:
        new_hab['priority'] = 1
    elif tod_task.priority == 4:
        new_hab['priority'] = .1
    return new_hab
    


def write_hab_task(hbt,task): 
    """
    writes a task, if inserted, to Habitica API as a todo. 
    To be added: functionality allowing you to specify things like difficulty
    """
    import requests
    import json
    auth, hbt = get_started('auth.cfg')
    url = 'https://habitica.com/api/v3/tasks/user/'
    hab = json.dumps(task)
    requests.post(headers=auth, url=url, data=hab)
        
def load_auth(configfile):
    """Get Habitica authentication data from the AUTH_CONF file."""

    logging.debug('Loading habitica auth data from %s' % configfile)

    try:
        cf = open(configfile)
    except IOError:
        logging.error("Unable to find '%s'." % configfile)
        exit(1)

    config = configparser.SafeConfigParser()
    config.readfp(cf)

    cf.close()

    # Get data from config
    rv = {}
    try:
        rv = {'url': config.get('Habitica', 'url'),
              'x-api-user': config.get('Habitica', 'login'),
              'x-api-key': config.get('Habitica', 'password')}

    except configparser.NoSectionError:
        logging.error("No 'Habitica' section in '%s'" % configfile)
        exit(1)

    except configparser.NoOptionError as e:
        logging.error("Missing option in auth file '%s': %s"
                      % (configfile, e.message))
        exit(1)

    # Return auth data as a dictionnary
    return rv

def complete_hab_todo(hbt, task):
    """
    pushes a completed task to the api.
    """
    hbt.user.tasks(_id=task.id, _direction='up', _method='post')
    
def check_matchDict(matchDict):
    """Troubleshooting"""
    for t in matchDict:
        if matchDict[t].complete == 0:
            if t.completed == False:
                print("both undone")
            elif t.completed == True:
                print("hab done, tod undone")
            else: 
                print("something is wroooong check hab")
        elif matchDict[t].complete == 1:
            if t.completed == False:
                print("hab undone, tod done")
                print(t.name)
            elif t.completed == True:
                print("both done")
            else:
                print("something is weird check hab")
        else:
            print("something is weird check tod")
