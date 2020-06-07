#!/usr/bin/env python3
#
# Python3 script to post Icinga2 alerts to Squadcast.
# This script has been tested with Python 3.7.
#

import sys
import os
import json
import ssl
import urllib.request
import logging

logger = logging.getLogger('sq-icinga2-host.py')
hdlr = logging.FileHandler('/tmp/sq-icinga2-py.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

def print_usage():
    """Print the script usage"""
    print("Usage:\n  sq-icinga2-host.py")

def form_payload(**kwargs):
    """Forms the python representation of the data payload to be sent from the passed configuration"""
    data = {}
    if(kwargs["alert_source"]=="HOST"):
        data = {
            "host_state":kwargs["host_state"],
            "host_output":kwargs["host_output"],
            "host_num_services_ok":kwargs["host_num_services_ok"],
            "host_num_services_warning":kwargs["host_num_services_warning"],
            "host_num_services_unknown":kwargs["host_num_services_unknown"],
            "host_num_services_critical":kwargs["host_num_services_critical"],
            "host_execution_time":kwargs["host_execution_time"],
            "host_latency":kwargs["host_latency"]

        }
    elif(kwargs["alert_source"]=="SERVICE"):
        data = {
            "service_state":kwargs["service_state"],
            "service_output":kwargs["service_output"],
            "service_description":kwargs["service_description"],
            "service_duration":kwargs["service_duration"],
            "service_comment":kwargs["service_comment"],
            "service_latency":kwargs["service_latency"],
            "service_execution_time" :kwargs["service_execution_time"],
            "service_downtime_depth": kwargs["service_downtime_depth"]
        }

    payload_rep = {
        "alert_source": kwargs["alert_source"],
        "notification_type": kwargs["notification_type"],
        "hostname": kwargs["hostname"],
        "host_alias":kwargs["host_alias"],
        "data":data
    }

    return payload_rep

def post_to_url(url, payload):
    """Posts the formed payload as json to the passed url"""
    try:
        gcontext = ssl.SSLContext()
        req = urllib.request.Request(url, data=bytes(json.dumps(payload), "utf-8"))
        req.add_header("Content-Type", "application/json")
        resp = urllib.request.urlopen(req, context=gcontext)
        if resp.status > 299:
           logger.error("[sq-icinga2] Request failed with status code %s : %s" % (resp.status, resp.read()))
    except urllib.request.HTTPError as e:
        if e.code >= 400 and e.code < 500:
            logger.error("[sq-icinga2] Some error occured while processing the event")

if __name__ == "__main__":
    url = os.getenv("ICINGA_CONTACT_WEBHOOK")
    alert_source = os.getenv("ICINGA_ALERTSOURCE")
    notification_type = os.getenv("ICINGA_NOTIFICATIONTYPE")
    hostname = os.getenv("ICINGA_HOSTNAME")
    host_alias = os.getenv("ICINGA_HOSTALIAS")
    
    host_state = os.getenv("ICINGA_HOSTSTATE")
    host_output = os.getenv("ICINGA_HOSTOUTPUT")

    service_state = os.getenv("ICINGA_SERVICESTATE")
    service_output = os.getenv("ICINGA_SERVICEOUTPUT")
    service_description = os.getenv("ICINGA_SERVICEDESC")
    service_duration = os.getenv("ICINGA_SERVICEDURATIONSEC")
    service_comment = os.getenv("ICINGA_COMMENT")
    service_latency = os.getenv("ICINGA_SERVICELATENCY")
    service_execution_time = os.getenv("ICINGA_SERVICEEXECUTIONTIME")
    service_downtime_depth = os.getenv("ICINGA_SERVICEDOWNTIMEDEPTH")

    host_num_services_ok = os.getenv("ICINGA_HOSTNUMSERVICESOK")
    host_num_services_warning = os.getenv("ICINGA_HOSTNUMSERVICESWARNING")
    host_num_services_unknown = os.getenv("ICINGA_HOSTNUMSERVICESUNKNOWN")
    host_num_services_critical = os.getenv("ICINGA_HOSTNUMSERVICESCRITICAL")
    host_execution_time = os.getenv("ICINGA_HOSTEXECUTIONTIME")
    host_latency = os.getenv("ICINGA_HOSTLATENCY")
    
    

    logger.info("[sq-icinga2] notification_type:{}".format(notification_type))
    logger.info("[sq-icinga2] hostname:{}".format(hostname))
    logger.info("[sq-icinga2] host_alias:{}".format(host_alias))
    logger.info("[sq-icinga2] host_state:{}".format(host_state))
    logger.info("[sq-icinga2] host_output:{}".format(host_output))
    logger.info("[sq-icinga2] service_state:{}".format(service_state))
    logger.info("[sq-icinga2] service_output:{}".format(service_output))
    logger.info("[sq-icinga2] service_description:{}".format(service_description))

    print("Sending data to squadcast")
    post_to_url(url, form_payload(alert_source = alert_source,
        notification_type = notification_type,
        hostname = hostname,
        host_alias = host_alias,
        host_state = host_state, 
        host_output = host_output,
        service_state = service_state,
        service_output = service_output,
        service_description = service_description,
        service_duration= service_duration,
        service_comment = service_comment,
        service_latency = service_latency,
        service_execution_time = service_execution_time,
        service_downtime_depth = service_downtime_depth,
        host_num_services_ok = host_num_services_ok,
        host_num_services_warning = host_num_services_warning,
        host_num_services_unknown = host_num_services_unknown,
        host_num_services_critical = host_num_services_critical,
        host_execution_time = host_execution_time,
        host_latency  = host_latency

        ))
    print("Done.")
