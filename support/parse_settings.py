#!/usr/bin/env python3

import os
import sys
import json

settings_files = [
        "/etc/nebula.json",
        "../settings.json",
        "settings.json"
    ]

config = {}
for settings_file in settings_files:
    if os.path.exists(settings_file):
        try:
            config.update(json.load(open(settings_file)))
        except Exception:
            pass

try:
    print (config[sys.argv[1]])
except Exception:
    sys.exit(1)
