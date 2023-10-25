<!--
---
	title: Pacifica Confessor and Daylight Savings Time
	author: David Klann <dklann@broadcasttool.com>
	date: Wed Oct 25 02:36:34 PM CDT 2023
---
-->
<!-- Create PDF formatted output with this command:
	pandoc --toc --embed-resources --resource-path=DST -f markdown -t latex -o DST.pdf DST.md
-->
# Pacifica Confessor and Daylight Saving Time #

Currently, in most US time zones there are two time changes each year: one when
we switch our clocks to _[Daylight Saving
Time](https://en.wikipedia.org/wiki/Daylight_saving_time)_ (_DST_), and one when
we switch them back to _Standard Time_.

As of this writing (October, 2023), the change **from** _Standard Time_ **to**
_Daylight Saving Time_ occurs on the second Sunday in March at 2 AM (more about
this later). The change **from** _Daylight Saving Time_ **to** _Standard Time_
occurs on the first Sunday in November at 2 AM.

The switch **to** _DST_ (from _Standard Time_) causes us to change our clocks to
one hour **earlier**. The actual change is done at what would be 2:00 AM on the
day of change by simply eliminating the 2AM hour: the time jumps from 1:59:59 AM
to 3:00 AM eliminating the 2AM hour.

The switch **from** _DST_ (to _Standard Time_) is done at 2:00 AM on the day of
change by setting the time **back** to 1:00 AM, thus adding one hour to the day:
the time jumps from 1:59:59 AM to 1:00 AM repeating the 1AM hour.

These changes require action on your part in order to keep your archived audio
consistent with the time on the clock (in whichever direction it changes).

<!--toc-->

## _DST_ and the Confessor ##

Switching between _Standard Time_ and _DST_ requires action on your part: you
must adjust your schedule in the Confessor in order to maintain the integrity of
your show's archives.

The reason this cannot be automated is that the Confessor cannot know _how_ you
want to adjust your schedule. You need to tell it at each seasonal transition.

## Adjusting Your Station's Schedule ##

In the "Spring" your schedule must be shortened by one hour (just as the day is
shortened by one hour). You can either remove the one-hour show that airs
between 2:00 AM and 3:00 AM (if there is one), or you can simply shorten the
show that crosses the 2:00 AM hour (if that's how your schedule is set up).

You must lengthen your schedule in the "Fall" (by adding an hour of programming
to the schedule), just as the day is one hour longer when switching to _Standard
Time_.

How this "shortening" and "lengthening" happens is more or less up to you and
your station's schedule.

### Spring Forward (Lose an Hour of Programming) ###

When you log in to your Confessor and navigate to your station's schedule for
the week of the time change **to** _DST_ you will notice that there is no 2AM hour
for that Sunday. But the length of the show which either starts at or crosses
2AM is still the same length. In other words, the total length of all the shows
for that Sunday is 24 hours, even though there are only 23 hours in that day.

In order to "fix" this, you must remove one hour from the scheduled shows for
that Sunday. If you don't do this, all recordings after 1:59 AM will start one
hour later than the actual clock time because the show that starts at (or
crosses) 2AM is one hour longer than the length of that day.

As shown in the example screenshots, the show that starts at 2AM ('TBA OPEN
TBA') in standard time (Sun 5) starts at 3AM in _DST_ (Sun 12). And all
subsequent shows start one hour later.

<table>
 <tr>
  <td width="30%"><img src="ScreenShot_2023-02-21_at_9.24.46_AM.png" /></td>
  <td width="30%"><img src="ScreenShot_2023-02-21_at_9.25.35_AM.png" /></td>
  <td width="30%"><img src="ScreenShot_2023-02-21_at_9.45.08_AM.png" /></td>
 </tr>
 <tr>
  <td>DST, 24 Hours</td>
  <td>Standard Time, uncorrected</td>
  <td>Standard Time, corrected</td>
 </tr>
</table>

The show ("TBA OPEN TBA") length is 3 hours, i.e. from 2AM to 5AM. In _DST_
(before correction) it’s still 3 hours long, i.e. from 3AM to 6AM. The next show
actually starts at 5AM, but now appears in the schedule to start at 6AM.

#### Shorten your schedule in the Spring ####

  1. browse to _Schedule Admin_ and click _Next_ in the schedule (upper right)
     until the first Sundy in November is visible; you'll see a "gap" or empty
     hour at the end of that day

  1. remove the hour from 2AM to 3AM (or shorten the length of the show that
     covers the 2AM hour)

  1. move every subsequent show up one hour so each starts at the proper time

  1. after your schedule is set the way you want it, click _Back to Admin_ and,
     when prompted save the playlist, as shown:

      ![](confessor-save-playlist-1.png)

  1. choose _Save Only This Week_ as shown in the next
     screenshot:

      ![](confessor-save-playlist-2.png)

  1. Confessor than offers to update the recorder playlist; choose _Update
     Playlist_ at the next prompt, as shown:

      ![](confessor-save-playlist-3.png)

  1. in the _Confessor Playlist Generator_ screen, simply click _Write Playlist_
     to save the archive recorder playlist file:

      ![](confessor-save-playlist-4.png)

  1. finally, also in the _Confessor Playlist Generator_ screen, the _Write
     Playlist_ button is replaced with a green _Done_ button:

      ![](confessor-save-playlist-5.png)

  1. you'll be returned to the main menu when you click _Back to Admin_

  1. go back to the week you changed and make sure the times are right

### Fall Back (Add an Hour of Programming) ###

On the first Sunday in November (as of 2023), you'll notice an extra hour of
time when you look at the schedule (_Schedule Admin_ from the main menu). You
need to fill this hour in order to keep all your archiving on time.

#### Lengthen your schedule in the Fall ####

  1. browse to _Schedule Admin_ and click _Next_ in the schedule (upper right)
     until the first Sundy in November is visible; you'll see a "gap" or empty
     hour at the end of that day
     
  1. rearrange your first-Sunday-in-November schedule either by adding an
     hour-long show (or two half-hour shows), or by lengthening the show that
     normally ends on or before 2:00am Sunday morning (technically, you can make
     up the one-hour of programming any time that day, but doing it over night
     makes for the best listening experience)

  1. after your schedule is set the way you want it, click _Back to Admin_ and,
     when prompted save the playlist, as shown:

      ![](confessor-save-playlist-1.png)

  1. choose _Save Only This Week_ as shown in the next
     screenshot:

      ![](confessor-save-playlist-2.png)

  1. Confessor than offers to update the recorder playlist; choose _Update
     Playlist_ at the next prompt, as shown:

      ![](confessor-save-playlist-3.png)

  1. in the _Confessor Playlist Generator_ screen, simply click _Write Playlist_
     to save the archive recorder playlist file:

      ![](confessor-save-playlist-4.png)

  1. finally, also in the _Confessor Playlist Generator_ screen, the _Write
     Playlist_ button is replaced with a green _Done_ button:

      ![](confessor-save-playlist-5.png)

  1. you'll be returned to the main menu when you click _Back to Admin_

You can check your work after saving the playlists: return to _Schedule Admin_
and click the _Next_ button to view the week you changed. Make any additional
changes, or simply return to the main menu.

Set yourself a calendar reminder to return in the Spring to adjust for the
switch to Daylight Savings Time.
