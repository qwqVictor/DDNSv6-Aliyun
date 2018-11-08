#!/bin/bash
cd `dirname $0`
python3 -c "$(cat config_user.py app.py)"
