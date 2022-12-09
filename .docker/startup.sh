#!/bin/bash
if [ ! -d "/tmp/check" ]; then
    mkdir /tmp/check
    echo `date` > /tmp/check/first_`date +%Y%m%d_%H%M%S`
    cp -rfT /tmp/${USER} ${HOME}
else
    echo `date` > /tmp/check/second_`date +%Y%m%d_%H%M%S`
fi

# pip install -r requirements.txt --user
# bash code-server_extentions_install_batch.sh

# nohup code-server --host 0.0.0.0 --port 9000 /home/coder/project_sandenretailsystem/project_sandenretailsystem.code-workspace
# /bin/bash code-server --host 0.0.0.0 --port 9999 /home/coder/share

# /bin/bash jupyter notebook /home/nb-user --ip=0.0.0.0 --port 10001 --allow-root
# /bin/bash jupyter notebook --ip=0.0.0.0 --port 10001 --allow-root
/bin/bash
