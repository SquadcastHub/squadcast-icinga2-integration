#!/usr/bin/env python3
#
# Python3 script to post Icinga2 alerts to Squadcast.
# This script has been tested with Python 3.6.
#

import sys
import os
import json
import ssl
import urllib.request
import logging

logger = logging.getLogger('sq-icinga2-host.py')
hdlr = logging.FileHandler('/tmp/sq-icinga2-host-py.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

def print_usage():
    """Print the script usage"""
    print("Usage:\n  sq-icinga2-host.py")

def form_payload(notification_type="",host_name="",host_alias="",host_state="", host_output=""):
    """Forms the python representation of the data payload to be sent from the passed configuration"""

    payload_rep = {"notification_type" : notification_type,"host_name":host_name,"host_alias":host_alias,"host_state":host_state,"host_output":host_output ,"alert_source": "HOST"}

    return payload_rep

def post_to_url(url, payload):
    """Posts the formed payload as json to the passed url"""
    try:
        gcontext = ssl.SSLContext()
        req = urllib.request.Request(url, data=bytes(json.dumps(payload), "utf-8"))
        req.add_header("Content-Type", "application/json")
        resp = urllib.request.urlopen(req,context=gcontext)
        if resp.status > 299:
           logger.error("[sq-icinga2-host] Request failed with status code %s : %s" % (resp.status, resp.read()))
    except urllib.request.HTTPError as e:
        if e.code >= 400 and e.code < 500:
            logger.error("[sq-icinga2-host] Some error occured while processing the event")

if __name__ == "__main__":
    url = os.getenv("ICINGA_CONTACT_WEBHOOK")
    notification_type = os.getenv("ICINGA_NOTIFICATIONTYPE")
    host_name = os.getenv("ICINGA_HOSTNAME")
    host_alias = os.getenv("ICINGA_HOSTALIAS")
    host_state = os.getenv("ICINGA_HOSTSTATE")
    host_output = os.getenv("ICINGA_HOSTOUTPUT")

    logger.error("[sq-icinga2-host] notification_type:{}".format(notification_type))
    logger.error("[sq-icinga2-host] host_name:{}".format(host_name))
    logger.error("[sq-icinga2-host] host_alias:{}".format(host_alias))
    logger.error("[sq-icinga2-host] host_state:{}".format(host_state))
    logger.error("[sq-icinga2-host] host_output:{}".format(host_output))
    print("Sending data to squadcast")
    print(form_payload(notification_type,host_name,host_alias,host_state, host_output))
    post_to_url(url, form_payload(notification_type,host_name,host_alias,host_state, host_output))
    print("Done.")
