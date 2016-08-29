# Rivendell systemd Unit Files

These unit files may be used to start and stop the Rivendell service daemons.

After copying the unit files to */etc/systemd/system*, enable the services with:
```
sudo systemctl enable caed@rivendell.service
sudo systemctl enable ripcd@rivendell.service
sudo systemctl enable rdcatchd@rivendell.service
```
This assumes you want to run the Rivendell services as the system user *rivendell*. Subsitute *@rivendell* with the name of the user as which you intend to run the Rivendell daemons (e.g. *rd*, *rduser*, etc.).

Set *rivendell.target* as the default with:
```
sudo systemctl set-default rivendell.target
```
After setting all this up you start the daemons with:
```
sudo systemctl isolate rivendell.target
```
You can stop the daemons with:
```
sudo systemctl isolate multi-user.target
```
or
```
sudo systemctl isolate graphical.target
```
Edit the unit file *rivendell.target* to specify whether you're depending on the multi-user target (no GUI apps expected to run on this system) or the graphical target (all the GUI apps installed and used on this system). Relevant settings are:

```
Requires=multi-user.target
After=multi-user.target
```

After making changes to any of the unit files in */etc/systemd/system* you must run the command:
```
sudo systemctl daemon-reload
```
