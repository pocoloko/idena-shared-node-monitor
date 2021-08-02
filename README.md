# remote monitor for idena public shared node

This monitor was created for my [Idena public shared node setup guide using your own SSL termination](https://github.com/pocoloko/idena-shared-node)

Since we are checking the response of the end node, an alert from this script could mean anything in the HAProxy -> idena-node-proxy -> idena-go node chain could be the culprit for the alert.

WARNING: The e-mail alerts work only with a localhost MTA without authentification or encryption

Usage:

1. clone this repo
2. rename nodecheck.ini_default to nodecheck.ini
3. edit nodecheck.ini with the address of the node you wish to monitor and the email for the alerts
4. set up a cron job to run the script at whatever interval you feel comfortable with.

If you encounter any issues please double-check the configuration as no error checks are performed on the configuration parameters
