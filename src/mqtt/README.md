# How to send mqtt to thingsboard :space_invader: :space_invader:

The script that send info to the Thingsboard Server Host is `pi_to_thingsboard.py`

Before execute `python3 pi_to_thingsboard.py` on the cmd we should execute de .sh script to stablish the environment variables to access the broker.

so we must run the next lines in the cmd

`. variables.sh`

On the raspberry pi tha enviromental variables can be configured by editing the file /etc/environment, just use:

`sudo nano /etc/environment` or `sudo vim /etc/environment`

`python3 pi_to_thingsboard.py`


## Sending Logs to MinIO :floppy_disk:

We will use an script in python to send the log files to a MinIO storage on radiatus. `log_to_minio.py`

need to install the library by running pip install minio in your command line.


## Capture audio :loud_sound:

This script has been done to capture 5 sec audios in order to take a test of the data capture in `pi_to_thingsboard.py`
