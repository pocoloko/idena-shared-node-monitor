# Remote monitor for idena public shared node

![Screenshot](screenshot_nodewatch.png)

This monitor was created for my [Idena public shared node setup guide using your own SSL termination](https://github.com/pocoloko/idena-shared-node), it is meant to run on a remote server, not the one where the node is running as that wouldn't provide proper monitoring.

Since we are checking the response of the end node, an alert from this script could mean anything in the `HAProxy -> idena-node-proxy -> idena-go node` chain could be the culprit for the alert.

If you receive an email with `EXCEPTION DETECTED : HTTPSConnectionPool(host='blabla.bla', port=443): Max retries exceeded with url: / (Caused by NewConnectionError(': Failed to establish a new connection: [Errno -2] Name or service not known'))` it could mean there is a network issue between the server you are checking from and your node. Check for packet loss using something like `mtr`.

WARNING: The e-mail alerts work only with a localhost MTA without authentification or encryption

Usage:

1. clone this repo
2. make sure you have the [requests python library](https://docs.python-requests.org/en/master/) installed
3. rename `nodecheck.ini_default` to `nodecheck.ini`
4. edit nodecheck.ini with the address of the node you wish to monitor and the email for the alerts
5. set up a cron job to run the script at whatever interval you feel comfortable with. For example: `*/15 * * * * cd /home/itsme/idena-shared-node-monitor/ && ./nodecheck.py`

If you encounter any issues please double-check the configuration as no error checks are performed on the configuration parameters

---
Found this script useful? I accept iDNA donations to address `0x8dc26a6fbdbe2fdb8b5284ab55f56e720b3c42ad`
