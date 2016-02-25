# Rivendell unit files

These unit files may be used to start and stop the Rivendell service daemons.

After copying the unit files to /etc/systemd/system, enable the services with:
```
sudo systemctl enable caed@rivendell.service
sudo systemctl enable ripcd@rivendell.service
sudo systemctl enable rdcatchd@rivendell.service
```
Set rivendell.target as the default with:
```
sudo systemctl set-default rivendell.target
```
After setting all this up you bring up the daemons with:
```
sudo systemctl isolate rivendell.target
```
You can stop the daemons with something like:
```
sudo systemctl isolate multi-user.target
```
or
```
sudo systmectl isolate graphical.target
```
Edit the unit file rivendell.target to specify whether you're depending on the multi-user target (no GUI apps expected to run on this system) or the graphical target (all the GUI apps installed and used on this system).

After making changes to any of the unit files in /etc/systemd/system you must run the command:
```
sudo systemctl daemon-reload
```

