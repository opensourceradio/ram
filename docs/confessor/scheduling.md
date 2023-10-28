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
- When you return to 'Admin' after editing you will be given the option of updating the 'recorder playlist'. The recorder playlist tells the recorder what to record and when. Unless you're planning on more edits later, it never hurts to update the playlist. 
- **If you don't update the recoreder playlist for whatever changes you've made, the recorder won't see them and continue recording the earlier schedule.**
- In other words, **always update the playlist unless there's something wrong with the schedule.**

### The Template ###

- The Template is the basic schedule for a week. If a week is not scheduled, the system
will insert the template for that empty week so the recorder won't stop.
- If there is a week scheduled, the recorder will use that week.

- When you create or modify the template, you must save it.

- You can choose how many weeks ahead to save it for. A good number is 3-4.

- The save dialog will show the last week the template is saved to.

*Update the recorder playlist.*

### Weeks ###

- Weeks are exactly like the template, except they are not copied ahead by the system.

- Weeks can be saved ahead like the template.

- They can be saved in a pattern - i.e. every other week, every three weeks, etc. etc. This makes it easy to 
alternate shows.

- The save dialog will show the last week that show is saved to.

*Update the recorder playlist.*

## How to Schedule ##

### The Template ###

1.	Create the show if it doesn't already exist.
	- You can click 'New Show' in the schedule screen.
	- Fill in the data you want.
	- Click 'Update'.  <br>
  

1.	Drag the show into the schedule at the day and the time where it will be heard.
	- If the length must be changed:
		1.	Right-click the show name to get the 'Remove or Change Length' dropdown.
		2.	Drag the red line to where you want the show to end.
	- You can use the same show object for any day or time, as many as it will be heard.
	- *Do not create a separate show for each day/time when it will be heard.*
	- The only reason to create more than one object for a given show is if there is an actual difference, e.g. a different host.
    - If there is temporary host, you will double-click the show on the actual week and day that host will appear and enter the temporary hosts's name there.  

3.	Repeat for each show to be scheduled.  

4.	Save the template for as many weeks ahead that you want.
	- You should generally save for the same number of weeks each time you modify the template. A good number is 3-4 weeks.

5.  *Update the recorder playlist.*

### Weeks ###

1.	Scheduling a specific week is exactly like scheduling the template.

2.	When you go to a week, the system will fill it with the schedule in the template if that week is empty so you don't have to create it from scratch.

3.	Make the changes, then save the week. If you are creating a week with alternating shows, you may save ahead in the pattern you're using - e.g. every other, every third, whatever. However, it's generally better to just do a month ahead, and do that every month.

4.	Save as many weeks as necessary to overwrite any template week that might be there.

5.  *Update the recorder playlist.*



### Alternate Shows in the Same Timeslot ###

1.	Go to the first week when the show will appear.

2.	Put the show for that week in the time slot.

3.	Do the same for any other shows that are alternating.

4.	Save that week in the pattern (every other, every third, etc) to a given date. Don't save more than a couuple of weeks ahead for the same show.

5.	**Repeat** 1-4 for the any other alternating shows.

6.  Then do the alternate show by advancing to the next week where the alernate show(s) should be scheduled.

7.  Repeat steps 1-4.

8.  *Update the recorder playlist.*

9.	Check that the weeks are right by looking at the public schedule on the web page (or at `<confessor.url>/playlist/pub_sched.php`).

### Specials ###

1.	Go to the week where the special will be heard.

1.	Create the show object for the special.

2.  Remove and/or change the length of the show(s) you're replacing.

3.	Drag and Drop the special into the space you created and adjust the length (if necessary).

4.	Save 'Only This Week'.

5.  *Update the recorder playlist.*

### Overlaps ###
- Shows are not allowed to overlap. If you get the 'Fix Overlaps' window when you try to save, you will have to fix any overlaps.
- The 'Remove/Change Length' drop-down would have appeared where there are overlaps and the red change-length line will be visible. Make whatever adjustment is necessary to remove the overlap and save.
- You can check overlaps by clicking 'Check Overlaps' in the Central menu.


# Copying the Template #

*Don't copy the template ahead for more than 3-4 weeks.*
If you were to copy ahead for 20 weeks, and then 2  weeks later make a change and copy ahead only 10
weeks (less than the first copy ahead), after 10 weeks the schedule will
revert to the schedule in the first template.
So always save the same 3-4 weeks ahead.
