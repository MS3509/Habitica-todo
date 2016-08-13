README

This is intended to be a two-way sync of Habitica and todoist. Any tasks that can't be found 
in both services should appear on the others, with the same status. If you complete a task on one service, 
it should appear as completed on another. Tasks that are created on Habitica should be sent to the 'Inbox' 
project on Todoist. 

INSTALLATION

You'll want to install two existing API Python wrappers that this utility depends on...

pip install habitica
pip install pytodoist

TASK DIFFICULTY
I felt that it would be good if task difficulty translated between tasks created on Todoist and 
Habitica. Therefore, task difficulty should sync with the following code by default, as laid out in $PRIORITY_DOC:

Todoist priority			Habitica difficulty
p1							Hard
p2							Medium
p3							Easy
p4							Trivial

If you'd like to change how the sync interprets difficulty or priority, please edit $PRIORITY_DOC.

USAGE

INSPIRATION
I'd like to credit several existing apps that I pulled from in order to create this. Notably: 
-existing habitica app, for a lot of initial code and many helpful explanations of how to do things 
	also for existing API! 
-Pytodoist 
-That one Dict2Obj script
-Dee Dee, for scriptabit which provided a lot of ideas 



THANKS 
