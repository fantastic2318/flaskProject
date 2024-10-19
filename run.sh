export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source /usr/local/bin/virtualenvwrapper.sh
cd  /root/JenkinsHome/jobs/PythonWeb/workspace
nohup python3 run.py >./my_log.log 2>&1 &
sleep 3
echo 'server started '
