#! /usr/bin/python

# Check if idena node is online and notify via email if something is wrong
# Meant to be used on a remote host, not the one where the node is running
# supports local MTA for e-mailing only, without authentication and without encryption

import requests # http magic
import configparser # external config file loading
import os, logging # disk and logging stuff
import smtplib # for sending results to email
from email.message import EmailMessage # for composing the email in an easy way, thanks python!
from urllib.parse import urlparse # to beautify URL for email

#Set up basic logging to file
logging.basicConfig(filename = ('nodecheck.log'), level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')


# Initial setup of configuration.
def setup():
    ##### CONFIGURATION ##### use config.ini for edits, edit the path to file below as needed
    config_file = 'nodecheck.ini' # The configuration file, edit this if your config file is not in folder you are running the script from!

    # If we have a config file, load it. Note this doesn't necessarily mean that the config file is valid, just that it exists
    if os.path.exists(config_file) and os.path.getsize(config_file) > 0:
        config = configparser.ConfigParser(interpolation=None) # this is not ideal but disabling interpolation due to having % in URLs
        config.read(config_file) # Lets read our config file
    else: # If we don't have a config file, stop execution
        logging.error(f"A config file is required, we didn't find a config file where expected: {config_file}")
        raise SystemExit # Stops execution, throws an exception
    return config

# check the node and return the results
def check_node(url, the_params):
    try:
        logging.info("CHECK START")
        res = requests.get(url, json=the_params)
        res.raise_for_status()
    except Exception as e:
        logging.error(f"CHECK FAILED: {str(e)}")
        result = f"EXCEPTION DETECTED : {str(e)}"
    else:
        if res.status_code == 200:
            result = f"OK"
            result_json = res.json()
            logging.info(f"CHECK OK: {result_json['result']}")
        else:
            result = f"WRONG HTTP RESPONSE CODE : {res.status_code}" # not sure I'll ever hit this as all exceptions should be caught above
    return result

# composing email for later sending, used only if node check is not OK
def compose_email(the_results):
    email_data = '<br>' #empty string for email data
    email_data += (the_results)
    logging.info('Composed email data')
    return email_data

# Send an email, used only if node check is not OK
def send_email(local_conf, the_url, email_data):
    the_url = (urlparse(the_url)).netloc
    themail = EmailMessage()
    themail.set_content(email_data, subtype='html')
    themail['Subject'] = (f"Idena node {the_url} error!")
    themail['From'] = (local_conf['MAIL']['FROM'])
    themail['To'] = (local_conf['MAIL']['TO'])
    try: # Lets send the email (use "with" instead?)
        smtp = smtplib.SMTP((local_conf['MAIL']['SERVER']))
        smtp.send_message(themail)
        logging.info('Sent e-mail of error')
    except smtplib.SMTPException as e: # log the error if any
        logging.error('Something went wrong! Couldn\'t send email: ' + e.args)
    return

def main(config):
    if not (config['DEFAULT'].getboolean('LOGGING')):
        logging.disable(logging.CRITICAL) # disables all logging
    logging.info('--------------------------------START--------------------------------')

    url = config['DEFAULT']['URL'] # fetch url from config file
    # json parameters as a dictionary, I'm using 1111 as the ID so I can easily find these calls in the server's logs
    params = {"method":"dna_epoch","params":[],"id": 1111, "key":config['DEFAULT']['NODEKEY']}

    results = check_node(url,params)
    if results != "OK": # we'll only send the email if the node check result is not good, ie. the node is actually down
        send_email(config, url, compose_email(results))
    logging.info('--------------------------------STOP--------------------------------')

if __name__ == "__main__":
    main(setup()) # Call main with the configuration as parameter, which is loaded via setup()
