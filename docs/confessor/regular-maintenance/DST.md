<!--
---
	title: Pacifica Confessor and Daylight Savings Time
	author: David Klann <dklann@broadcasttool.com>
	date: Wed Feb 22 12:03:37 PM CST 2023
---
-->
<!-- Create formatted output with one of these commands:
	pandoc --toc --standalone --self-contained -f markdown -t html -o DST.html DST.md
	pandoc --toc --standalone --self-contained -f markdown -t latex -o DST.pdf DST.md
-->
# Pacifica Confessor and Daylight Saving Time #

Currently, in most US time zones there are two time changes each year: one when
we switch our clocks to _[Daylight Saving
Time](https://en.wikipedia.org/wiki/Daylight_saving_time)_ (DST), and one when
we switch them back to _Standard Time_.

As of this writing (October, 2023), the change from _Standard Time_ to DST
occurs on the second Sunday in March at 2 AM (more about this later). The change
from DST to _Standard Time_ occurs on the first Sunday in November at 2 AM.

The switch to DST causes us to move our clocks to one hour **earlier** than
_Standard Time_. The actual change is done at what would be 2:00 AM on the day
of change by simply eliminating the 2AM hour. The time jumps from 1:59:59 AM to
3:00 AM eliminating the 2AM hour.

These changes require action on your part in order to keep your archived audio
consistent with the time on the clock (in whichever direction it changes).

<!--toc-->

## DST and the Confessor ##

When you log in to your Confessor and navigate to your station's schedule for
the week of the time change to DST you will notice that there is no 2AM hour for
that Sunday. But the length of the show which either starts at or crosses 2AM is
still the same length. In other words, the total length of all the shows for
that Sunday is still 24 hours, even though there are only 23 hours in that day.

In order to "fix" this, you must remove one hour from the scheduled shows for
that Sunday. If you don't do this, all recordings after 1:59AM will start one
hour later than the actual DST clock time because the show that starts at (or
crosses) 2AM is one hour longer than the length of that day allows.

As you can see in the example screenshots, the show that starts at 2AM ('TBA
OPEN TBA') in standard time (Sun 5) starts at 3AM in DST (Sun 12). And all
subsequent shows start one hour later.

<table>
 <tr>
  <td width="30%"><img src="/confessor/regular-maintenance/assets/ScreenShot_2023-02-21_at_9.24.46_AM.png" /></td>
  <td width="30%"><img src="/confessor/regular-maintenance/assets/ScreenShot_2023-02-21_at_9.25.35_AM.png" /></td>
  <td width="30%"><img src="/confessor/regular-maintenance/assets/ScreenShot_2023-02-21_at_9.45.08_AM.png" /></td>
 </tr>
 <tr>
  <td>DST, 24 Hours</td>
  <td>Standard Time, uncorrected</td>
  <td>Standard Time, corrected</td>
 </tr>
</table>

Its length in the schedule is 3 hours, i.e. from 2AM to 5AM. In DST (before
correction) it’s still 3 hours long, i.e. from 3AM to 6AM. The next show
actually starts at 5AM, but now appears in the schedule to start at 6AM.

You may be asking yourself, "How can I correct this situation?" (you may also be
wondering why the computer can't just fix it for you!).

## Adjusting Your Station's Schedule ##

The answer is that in the "Spring" (usually still the dead of Winter in the
upper reaches of the US) one show must be shortened by one hour (just as the day
is shortened by one hour). Alternatively, you can simply remove the one-hour
show that airs between 2:00AM and 3:00AM (if there is one).

You must lengthen your schedule in the "Fall" (by adding an hour of programming
to the schedule), just as the day is one hour longer when switching to _Standard
Time_.

How this "shortening" and "lengthening" happens is more or less up to you and
your station's schedule.

### Spring Forward (Lose an Hour of Programming) ###

Shorten your schedule for a day in the Spring:

  1. Remove the hour from 2AM to 3AM

  1. Move every subsequent show up one hour so each starts at the proper time

  1. Save "Only This Week"

  1. Go ‘Back to Admin’ and save the playlist

  1. Go back to the week you changed and make sure the times are right

### Fall Back (Add an Hour of Programming) ###

On the first Sunday in November (as of 2023), you'll notice an extra hour of
time when you look at the schedule (_Schedule Admin_ from the main menu). You
need to fill this hour in order to keep all your archiving on time.

To add one hour of programming to your schedule for a day in the Fall:

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

      ![](/confessor/regular-maintenance/assets/confessor-save-playlist-1.png)

  1. choose _Save Only This Week_ as shown in the next
     screenshot:

      ![](/confessor/regular-maintenance/assets/confessor-save-playlist-2.png)

  1. Confessor than offers to update the recorder playlist; choose _Update
     Playlist_ at the next prompt, as shown:

      ![](/confessor/regular-maintenance/assets/confessor-save-playlist-3.png)

  1. in the _Confessor Playlist Generator_ screen, simply click _Write Playlist_
     to save the archive recorder playlist file:

      ![](/confessor/regular-maintenance/assets/confessor-save-playlist-4.png)

  1. and finally, also in the _Confessor Playlist Generator_ screen, the _Write Playlist_ button is replaced with a green _Done_ button:

      ![](/confessor/regular-maintenance/assets/confessor-save-playlist-5.png)

  1. you'll be returned to the main menu when you click _Back to Admin_

You can check your work after saving the playlists: return to _Schedule Admin_
and click the _Next_ button to view the week you changed. Make any additional
changes, or simply return to the main menu.

Set yourself a calendar reminder to return in the Spring to adjust for the
switch to Daylight Savings Time.
