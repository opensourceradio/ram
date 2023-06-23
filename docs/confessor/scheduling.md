<!--
---
	title: Scheduling
	author: Otis Maclay  <maclay@gmail.com>
	date: Fri Jun 23 12:15:00 PM CDT 2023
---
-->
<!-- Create formatted output with one of these commands:
	pandoc --toc --standalone --self-contained -f markdown -t html -o scheduling.html scheduling.md
	pandoc --toc --standalone --self-contained -f markdown -t latex -o scheduling.pdf scheduling.md
-->

# Scheduling #
At 'Schedule Admin' in the main menu.

## Basic Ideas ##

- Scheduling is done by the week.
- Weeks are discrete entities.
- Weeks start on Sunday.
- Shows are objects you can drag and drop, move, remove, and change the length.
	- Right clicking on the name of the show opens a little drop-down which presents the choice to Remove or Change Length.
- The recorder uses the week to know what to record.
- If there is no week for the recorder to record, it will record nothing.
- Navigating weeks:
	- You can enter any date contained in the week you want in the 'Date' field (`[m]m/dd/yy`) in the Central menu.
	- You can go 'next' and 'previous' to navigate dates. If there's no week where you navigate you will get the template week.
	- To navigate from the template to the current week, go 'Next', then 'Previous'.
- Just a note: the background color is reddish when you're working the template and blue when you're working a week.
- The Central menu turns red if you've made any modifications to the schedule.
- When you return to 'Admin' after editing you will be given the option of saving the 'recorder playlist'. The recorder playlist tells the recorder what to record and when. Unless you're planning on more edits later, it never hurts to create the playlist. 
- **If you don't write a playlist for whatever changes you've made, the recorder won't see them and continue recording the earlier schedule.**

### The Template ###

The Template is the basic schedule for a week. If a week is not scheduled, the system
will insert the template for that empty week so the recorder won't stop.
If there is a week scheduled, the recorder will use that week.

When you create or modify the template, you must save it.

You can choose how many weeks ahead to save it for.

The save dialog will show the last week the template is saved to.

### Weeks ###

Weeks are exactly like the template, except they are not copied ahead by the system.

Weeks can be saved ahead like the template.

They can be saved in a pattern - i.e. every other week, every three weeks, etc. etc. This makes it easy to 
alternate shows.

The save dialog whil show the last week that show is saved to.

## How to Schedule ##

### The Template ###

1.	Create the show.
	- You can click 'New Show' in the schedule screen.
	- The 'length' number only affects the size of the show object itself. It defaults to an hour.
		- (Lengths are regular time entries without the colon. i.e. one hour is '100'. Half an hour is '30'. An hour and a half is '130').
	- If the show already exists, skip this step.

2.	Drag the show into the schedule at the day and the time where it will be heard.
	- If the length must be changed:
		1.	Right-click the show name to get the 'Remove or Change Length' dropdown.
		2.	Drag the red line to where you want the show to end.
	- You can use the same show object for any day or time, as many as it will be heard.
	- *Do not create a separate show for each day/time when it will be heard.*
	- The only reason to create more than one object for a given show is if there is an actual difference, e.g. a different host.
		 - If there is temporary host, you will double-click the show on the actual week and day that host will appear and enter the temporary hosts's name there.

3.	Repeat for each show to be scheduled.

4.	Save the template for as many weeks ahead that you want.
	- You should generally save for the same number of weeks each time you modify the template. A good number is 6-8 weeks.

### Weeks ###

1.	Scheduling a week is exactly like scheduling the template.

2.	When you go to a week, the system will write the template if that week is empty. So generally you will be editiing weeks rather than creating them.

3.	Make the changes, then save the week. If you are creating a week with alternating shows, save ahead in the pattern you're using - e.g. every other, every third, whatever.

4.	Save as many weeks as necessary to overwrite any template week that might be there.


### Alternate Weeks ###
-	To schedule alternate shows in the same timeslot:
	1.	Go to the first week the show will appear.
	2.	Put the show for that week in the time slot.
	3.	Do the same for any other shows that are alternating.
	4.	Save that week in the pattern (every other, every third, etc) to a given date which must be beyond where any template or other week was saved so that it won't revert to whatever is there.
	6.	**Repeat** 1-4 for the first week of the alternate week.
	5.	Check that the weeks are right by looking at the public schedule on the web page (or at `<confessor.url>/playlist/pub_sched.php`).

### Specials ###
1.	Go to the week where the special will be heard.
1.	Create the show object for the special.
2.  Remove and/or change the length of the show(s) you're replacing.
3.	Drag and Drop the special into that space and adjust the length (if necessary).
4.	Save 'Only This Week'.

### Overlaps ###
- Shows are not allowed to overlap. If you get the 'Fix Overlaps' window when you try to save, you will have to fix any overlaps.
- The 'Remove/Change Length' drop-down would have appeared where there are overlaps and the red change-length line will be visible. Make whatever adjustment is necessary to remove the overlap and save.
- You can check overlaps by clicking 'Check Overlaps' in the Central menu.


# Copying the Template #

Copy ahead for 20 weeks, 2 weeks later make a change and copy ahead only 10
weeks (less than the original copy ahead), after 10 weeks the schedule will
revert to the original copy.
