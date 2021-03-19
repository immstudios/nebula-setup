Nebula setup
============

Nebula installers and configuration tools.

This document describes basic Nebula installation and configuration process. Advanced techniques such as
database configuration, optimization, and backup, security, GPU acceleration support etc. are out of the scope of this guide.
For production deployment, you should get familiar with Linux security, PostgreSQL, memcached and NGINX configuration
as well as basic Python programming.

Nebula is a complex software, which can be configured to fit many different workflows, so don't be ashamed
to [get in touch with us](mailto:support@nebulabroadcast.com) and get a professional support.

Yes. This is what we do for a living.

Prerequisites
-------------

Use `prerequisites.sh` script to install all required libraries and software

## NGINX

Nebula also needs NGINX server with http push module  and mp4 module to be installed.
Use [install.nginx.sh](https://github.com/immstudios/installers/blob/master/install.nginx.sh)
and create `/var/www/yoursitename/http.conf` file.

Following configuration example assumes that:

 - your `site_name` is `nebula`
 - nginx is running on the same machine as nebula hub/core server
 - your internal network is 192.168.0.0/16
 - there is NAT configured for ports 80 and 443 to the nginx server
 - there is a DNS record "nebula.example.com" and let's encrypt configured.

```nginx
server {
    listen              80;
    server_name         nebula.example.com;
    server_tokens       off;

    location /msg_publish {
        allow                           10.0.0.0/8;
        allow                           172.16.0.0/12;
        allow                           192.168.0.0/16;
        deny                            all;
        access_log                      off;
        nchan_publisher;
        nchan_channel_id                $arg_id;
        nchan_message_buffer_length     50;
        nchan_message_timeout           10s;
    }
    
    location / {
        return                  302 https://$host$request_uri;
    }
}


server {
    listen                      443 ssl http2;
    server_name                 nebula.example.com;
    server_tokens               off;

    ssl_certificate             /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key         /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_trusted_certificate     /etc/letsencrypt/live/example.com/chain.pem;

    set $nxcore_root            /mnt/nebula_01/.nx;

    location ~ /ws/(.*) {
        nchan_subscriber        websocket;
        nchan_channel_id        $1;
        add_header              Access-Control-Allow-Headers    'origin, content-type, accept, user-agent, referer' always;
        add_header              Access-Control-Allow-Origin     '*';
    }

    location /proxy/ {
        mp4;
        mp4_max_buffer_size 5m;
        root                    $nxcore_root;
        add_header              Access-Control-Allow-Origin     '*' always;
        add_header              Access-Control-Allow-Methods    'GET';
        add_header              Access-Control-Allow-Headers    'origin, content-type, accept, user-agent, referer' always;
    }

    location /thumb/ {
        root                    $nxcore_root;
        add_header              Access-Control-Allow-Origin     '*' always;
        add_header              Access-Control-Allow-Methods    'GET';
        add_header              Access-Control-Allow-Headers    'origin, content-type, accept, user-agent, referer' always;
    }

    location ~* ^/tools/(.*)/static/(.*)$ {
        alias                   $nxcore_root/scripts/v5/webtools/$1/static/$2;
    }
    
    location /static {
        proxy_pass              http://127.0.0.1:8080;
        proxy_buffering         off;
        add_header              Access-Control-Allow-Origin     '*' always;
        add_header              Access-Control-Allow-Methods    'GET';
        add_header              Access-Control-Allow-Headers    'origin, content-type, accept, user-agent, referer' always;
        proxy_set_header        Host                            $host;
        proxy_set_header        X-Real-IP                       $remote_addr;
    }

    location ~ ^/(login|logout|ping|api|assets|detail|jobs|tool|services|passreset|settings|profile|$) {
        if ($request_method = 'OPTIONS') {
            add_header          Access-Control-Allow-Origin     '*';
            add_header          Access-Control-Allow-Methods    'GET, POST, OPTIONS';
            add_header          Access-Control-Allow-Headers    'origin, content-type, accept, user-agent, referer' always;
            add_header          Content-Type                    'text/plain; charset=utf-8';
            add_header          Content-Length                  0;
            return              204;
        }
    
        proxy_pass              http://127.0.0.1:8080;
        proxy_buffering         off;
        add_header              Access-Control-Allow-Origin     '*' always;
        add_header              Access-Control-Allow-Headers    'origin, content-type, accept, user-agent, referer' always;
        proxy_set_header        X-Real-IP                       $remote_addr;
        proxy_set_header        Host                            $host;
    }

    location / {
        return 404;
    }
}
```


## FFMpeg

Conversion nodes depend on ffmpeg. You may use
[this script](https://github.com/immstudios/installers/blob/master/install.ffmpeg.sh)
to install it.


Database schema
---------------

Create a database using `support/schema.sql`. If you are running PostgreSQL server and `nebula-setup` on the same machine,
you may use `create_db.sh` script to create database user and database and apply the schema. Credentials provided in the
`settings.json` file will be used in that case.


Site template
-------------

Create a file `template/__init__.py` in the root directory of this repository to override settings from `defaults/` folder.

Use `setup.py` to apply the template. This script can be also used later to modify site settings without tweaking database manually.

### Example configuration

Assuming there are two machines:

  - **192.168.1.90** - all in one nebula server + production storage
  - **192.168.1.91** - caspar cg playout server

```python

import socket

HOST = socket.gethostname()

from defaults import *

#
# Configured storages are mounted to /mnt/${sitename}_${idstorage}/
# By default /mnt/sitename_01/.nx/ is used to store plugins, low-res
# videos, thumbnails, reports etc.
#

data["storages"] = {
    1 : {
        "title"    : "production",
        "protocol" : "samba",
        "path"     : "//192.168.1.90/storage",
        "login"    : "nebula",
        "password" : "nebulapass"
    },

    2 : {
        "title"    : "playout",
        "protocol" : "samba",
        "path"     : "//192.168.1.91/storage",
        "login"    : "nebula",
        "password" : "nebulapass"
    }
}

#
# Currently only playout channels (type 0) are supported.
#

data["channels"] = {
    1 :  [0, {
        'title': 'Nebula TV',
        'engine' : 'casparcg',
        'controller_host' : 'localhost',
        'controller_port' : 42100,
        'caspar_host' : '192.168.1.90',
        'caspar_port' : 5250,
        'caspar_channel' : 1,
        'caspar_feed_layer' : 10,
        'playout_storage' : 2,
        'playout_dir' : "media.dir",
        'playout_container' : 'mov',
        'day_start' : [8, 0],
        'send_action' : 2,
        'rundown_accepts': "asset['content_type'] == VIDEO",
        'scheduler_accepts': "asset['id_folder'] in [1, 2]",
        'fps': 25,
        'live_source' : 'DECKLINK 2 FORMAT 1080i5000',
        'plugins': [],
        'solvers': [],
        'meta_set' : [
                ('title', {}),
                ('description', {})
            ]
    }]
}


#
# Services
#

#         type      host  title      config path                    autostart  loop_delay

data["services"] = {
    1  : ["mesg",   HOST, "mesg",    "template/services/mesg.xml",  True,      5],
    2  : ["broker", HOST, "broker",  None,                          True,      5],
    3  : ["meta",   HOST, "meta",    None,                          True,      5],
    4  : ["play",   HOST, "play",    "template/services/play.xml",  True,      5],
    5  : ["conv",   HOST, "conv01",  None,                          True,      5],
    6  : ["psm",    HOST, "psm",     None,                          True,      30],
}

```

Services
--------

### mesg

Messaging/logging service. One is needed for each network segment.

Relay address is the address of the configured NGINX server.
All multicast status messages will be relayed to its HTTP push module and served to clients
using websockets.

```xml
<service>
    <relay>http://192.168.1.90</relay>
    <log_dir>/var/log/nebula</log_dir>
    <log_ttl>30</log_ttl>
</service>
```

### play

Playout controller.

Only `id_channel` parameter must be specified in the service configuration.
There must not be two services controlling the same channel at the same time!

```xml
<settings>
    <id_channel>1</id_channel>
</settings>
```

### broker

Jobs broker. One **broker** service is needed per site. No configuration file is needed.

### meta

Metadata extraction service. Two meta services are recommended for each site.
One with no configuration file at all (scan all files) and one with the following configuration:

```xml
<settings>
    <cond>asset["status"] == CREATING</cond>
</settings>
```

This one will scan only recently changed media files, which significantly improves overal system performance.

### conv

Media transcoding service. A configuration file is optional and allows to limit service usage to
perform a particular action(s).

### psm

Playout storage monitor. One **psm** service is needed if the site uses one or more playout channels.
No configuration file is needed.

### watch

Watchfolder service creates new assets from media files.

Folder tag attributes:

 - `id_storage` (required)
 - `path` (required)
 - `id_folder` (default  12 - Incoming)
 - `recursive` (default True)
 - `hidden` (default False) - Ignore dotfiles
 - `quarantine_time` (default 10)
 - `case_sensitive_exts` (default False)

```xml
<service>
    <folder id_storage="1" path="media.dir"></folder>
</service>
```
### worker

Worker is a wrapper service, which executes given worker plugin script.

Configuration example:

```xml
<service script="dummy"/>
```

### Import

File ingest services based on Themis library.


Acknowledgements
----------------

### EBUCore

[EBU Tech 3293](https://tech.ebu.ch/MetadataEbuCore)


### EBUCore ContentGenres Czech translation

[Czech translation of the EBUContentGenre thesaurus](http://hdl.handle.net/11858/00-097C-0000-000D-EC91-2)

Ircing, Pavel, 2013,
LINDAT/CLARIN digital library at the Institute of Formal and Applied Linguistics (ÚFAL)
Faculty of Mathematics and Physics, Charles University,
