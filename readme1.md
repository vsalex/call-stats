# backup-control

Receive fresh e-mail every day that allow you to be sure by single look that everything ok with your backups. It really helps if you have at least a dozen or hundred user/server backups every day.

There are number of options that describes status (`+` or `-`) of every backup location (`endpoint`) such as: date of creation, minimum endpoint size, number of files/directories by mask, size of every file/directory etc.

Also this scripts allow you to delete old files/directories by number of files/directories in `endpoint` or by total `endpoint` size.

## Requirements

Python 3.4, jsoncomment

## Installation

Install through git:

```
mkdir ~/backup-control
cd ~/backup-control
git init
git remote add origin git@github.com:vsalex/backup-control.git
git pull origin master

```

## Usage

Add your own `config_local.py` file into backup-control root directory. It must contain MTA params in dictionary `smtp_params` and default `debug` status:
```
debug = True

smtp_params = {
    "smtp_server":    "smtp.gmail.com",
    "smtp_port":       25,
    "smtp_login":     "backup_control@gmail.com",
    "smtp_password":  "my_smtp_password",
}

```

Then create your first json `example_backup.json` configuration file that will describe backup control process:

```
{
    "email_to":           ["my_backup_control@gmail.com", "vsalex@6vi.ru"],
    "email_subject":      "My archives",

    # you can write everything that backup_control does in log
    "log_file":                "/var/log/backup_control/my_archives.log",

    "endpoints": [{
        "name": "important data from my PC",
        "endpoint": "/home/vsalex/my_backups/*work_backup*",

        "up_to_date": 5,
        "min_file_size": 1500,
        "min_number_of_files": 1,

        "rotate_by_size": 6000
    }]
}
```

Then run `python3 backup-control.py example_backup.json`.

## Advanced example

You can have a lot of `endpoints` to control and thus a lot of json configuration files for each endpoint. In this case you can put them all into specific place and write make your configuration file like this:
 ```
 {
    "email_to":           ["my_backup_control@gmail.com", "vsalex@6vi.ru"],
    "email_subject":      "My archives",

    # you can write everything that backup_control does in log
    "log_file":                "/var/log/backup_control/my_archives.log",

    "path_to_watch_directory": "/home/vsalex/backup_control/conf/server_includes"
}
 ```

 If scripts meet in current json configuration param `path_to_watch_directory` it read all json files from that directory and use them as `endpoionts` to verify.

  ` ~# ls /home/vsalex/backup_control/conf/server_includes` can be something like that:

 ```
server1.json, server2.json, server3.json, buh-server.json, www-server.json,
zabbix.json, dmz.json, mailserver.json, virtualserver1.json, virtualserver2.json,
virtualserver3.json
 ```
 `~# cat server1.json`
 ```
 [
    {
        "name": "server1-root",
        "endpoint": "/mnt/raid/server1/os/*system-root*",

        "up_to_date": 7,
        "min_file_size": 5000,

        "rotate_by_size": 20000
    },
    {
        "name": "server1-home",
        "endpoint": "/mnt/raid/server1/os/*system-home*",

        "up_to_date": 7,
        "min_file_size": 2500,

        "rotate_by_size": 10000
    },
    {
        "name": "server2-data",
        "endpoint": "/mnt/raid/server1/data*",

        "up_to_date": 2,
        "min_file_size": 30000,
        "min_number_of_files": 6,

        "rotate_by_size": 500000
    }
]
 ```
`~# ls /mnt/raid/server1/os`
```
-dev-system-home.2016_04_01.1459534921.dump  -dev-system-root.2016_03_11.1457716861.dump
-dev-system-home.2016_04_08.1460139722.dump  -dev-system-root.2016_03_18.1458321662.dump
-dev-system-home.2016_04_15.1460744521.dump  -dev-system-root.2016_03_25.1458926461.dump

```

## API
... in progress