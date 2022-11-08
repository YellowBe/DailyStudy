## linux sh脚本开机自启
+ https://www.linode.com/docs/guides/start-service-at-boot/
### if systemctl says roscore command can not found
+ source it: https://answers.ros.org/question/290599/how-to-run-roscore-or-roslaunch-when-i-boot/
+ source /opt/ros/kinetic/setup.bash
### and systemctl can not found the python module
+ just define the current user to construct the python environment.
+ https://stackoverflow.com/questions/35641414/python-import-of-local-module-failing-when-run-as-systemd-systemctl-service, user is depended on your username
```
[Unit]
Description=web server monitor

[Service]
WorkingDirectory=/home/<user>/
User=<user>
ExecStart=/home/<user>/heartbeat.py
Restart=always

[Install]
WantedBy=multi-user.target
```

# 10.31
## Markdown to PDF
+ VSCode install markdown pdf