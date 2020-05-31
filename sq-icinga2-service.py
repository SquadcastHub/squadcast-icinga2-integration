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

logger = logging.getLogger('sq-icinga2-service.py')
hdlr = logging.FileHandler('/tmp/sq-icinga2-service-py.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

def print_usage():
    """Print the script usage"""
    print("Usage:\n  sq-icinga2-service.py")

def form_payload(hostname = "",hostalias = "", service_description = "",service_state = "",notification_type = "",service_output = ""):
    """Forms the python representation of the data payload to be sent from the passed configuration"""

    payload_rep = {"hostname" : hostname,"hostalias":hostalias,"service_description":service_description,"service_state":service_state,"notification_type":notification_type,"service_output":service_output,"alert_source": "SERVICE" }

    return payload_rep

def post_to_url(url, payload):
    """Posts the formed payload as json to the passed url"""
    try:
        gcontext = ssl.SSLContext()
        req = urllib.request.Request(url, data=bytes(json.dumps(payload), "utf-8"))
        req.add_header("Content-Type", "application/json")
        resp = urllib.request.urlopen(req,context=gcontext)
        if resp.status > 299:
           logger.error("[sq-icinga2-service] Request failed with status code %s : %s" % (resp.status, resp.read()))
    except urllib.request.HTTPError as e:
        if e.code >= 400 and e.code < 500:
            logger.error("[sq-icinga2-service] Some error occured while processing the event")

if __name__ == "__main__":
    url = os.getenv("ICINGA_CONTACT_WEBHOOK")
    notification_type = os.getenv("ICINGA_NOTIFICATIONTYPE")
    service_description = os.getenv("ICINGA_SERVICEDESC")
    hostname = os.getenv("ICINGA_HOSTNAME")
    hostalias = os.getenv("ICINGA_HOSTALIAS")
    service_state = os.getenv("ICINGA_SERVICESTATE")
    service_output = os.getenv("ICINGA_SERVICEOUTPUT")
    logger.error("[sq-icinga2-service] notification_type:{}".format(notification_type))
    logger.error("[sq-icinga2-service] service_description:{}".format(service_description))
    logger.error("[sq-icinga2-service] hostname:{}".format(hostname))
    logger.error("[sq-icinga2-service] hostalias:{}".format(hostalias))
    logger.error("[sq-icinga2-service] service_state:{}".format(service_state))
    logger.error("[sq-icinga2-service] service_output:{}".format(service_output))
    print("Sending data to squadcast")
    print(form_payload(hostname,hostalias,service_description,service_state,notification_type,service_output))
    post_to_url(url, form_payload(hostname,hostalias,service_description,service_state,notification_type,service_output))
    print("Done.")
