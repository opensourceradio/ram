# Kuchota (Swahili for "fetch")
Kuchota is an app that fills the RSS-feed-fetch void in Rivendell. Use Kuchota to configure, retrieve and import audio from arbitrary RSS feeds.

## Installation

(Someday this will be an installable package for at least one Linux distro.)

### Requirements

* _zsh_
* _mysql_ client app
* _podget_ not from repo, from github source
* _wget_
* _/usr/local/bin/zsh-functions_ also in this repo
* _/usr/local/bin/pmw-podget-wrapper_ also in this repo
* all commands listed in ourCommands in _kuchota_ and in _pmw-podget-wrapper_
* replace the placeholder %PODGET\_DIR\_CONFIG% with its actual value in _kuchota_ and _pmw-podget-wrapper_
* directory structure (where *$KUCHOTA* is the "home" directory of the kuchota app):

	+ *$KUCHOTA*/configuration
	+ *$KUCHOTA*/log
	+ *$KUCHOTA*/tmp

* $KUCHOTA/configuration:

	+ _conf.msmtp_ Depending on the location declared in *$MAILER_CONFIG* in _notifyrc_.
	+ _notifyrc_ Set all variables appropriately.
	+ _podgetrc_ Set the following variables:
		+ DIR\_SESSION=%PODGET\_DIR\_SESSION%
		+ DIR\_LIBRARY=%PODGET\_DIR\_LIBRARY%
		+ DIR\_LOG=%PODGET\_DIR\_LOG%
	+ _serverlist_ Should be empty except for the comments.

### Text GUI configuration

* Place _kuchota.desktop_ in _/usr/share/applications_
* As the "target" user, run:
		XDG_UTILS_DEBUG_LEVEL=999 xdg-desktop-menu install --novendor /usr/share/applications/kuchota.desktop
* Place _kuchota.svg_ in _/usr/share/icons/gnome/scalable/apps_
	+ run `gtk-update-icon-cache /usr/share/icons/gnome` or `gtk-update-icon-cache-3.0 /usr/share/icons/gnome`
* _GNOME terminal_ create a "kuchota" profile:

		dconf load /org/gnome/terminal/legacy/profiles:/$(uuidgen):/ << EOF
		[/]
		foreground-color='rgb(0,0,0)'
		visible-name='kuchota'
		palette=['rgb(0,0,0)', 'rgb(170,0,0)', 'rgb(0,170,0)', 'rgb(170,85,0)', 'rgb(0,0,170)', 'rgb(170,0,170)', 'rgb(0,170,170)', 'rgb(170,170,170)', 'rgb(85,85,85)', 'rgb(255,85,85)', 'rgb(85,255,85)', 'rgb(255,255,85)', 'rgb(85,85,255)', 'rgb(255,85,255)', 'rgb(85,255,255)', 'rgb(255,255,255)']
		default-size-columns=132
		default-size-rows=32
		use-theme-colors=false
		exit-action='hold'
		background-color='rgb(255,255,221)'
		scrollbar-policy='never'
		EOF

		profiles=$(dconf list /org/gnome/terminal/legacy/profiles:/ |
			grep '^:' |
			tr '\012' ' ' |
			tr -d : |
			sed -e "s/^/['/" -e "s/ *$/']/" -e "s/ /', '/" -e "s,/,,g")
		dconf write /org/gnome/terminal/legacy/profiles:/list "${profiles}"

### Running

Invoke Kuchota either from the command line in a terminal window, or by clicking on the desktop icon. The menu leads you through adding, deleting (or disabling), enabling, listing and otherwise managing the list of podcasts and Rivendell dropboxes.
