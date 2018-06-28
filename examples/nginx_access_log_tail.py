from atsd_client import connect, connect_url
from atsd_client.models import Message
from atsd_client.services import MessageService, Severity
import socket
from datetime import datetime
# Install sh module separately
from sh import tail
import csv
import logging

logger = logging.getLogger()
logger.disabled = True

# nginx must be configured to write logs in CSV format:
#
# geoip_country /etc/nginx/geoip/GeoIP.dat;    # country IP database
# geoip_city /etc/nginx/geoip/GeoLiteCity.dat; # city IP database
# geoip_org /etc/nginx/geoip/GeoIPASNum.dat;   # org/network database
#
# log_format custom '"$remote_addr","$remote_user","$time_iso8601","$host","$request_method","$server_protocol","$scheme","$request_uri",$status,$body_bytes_sent,"$http_referer","$http_user_agent","$http_x_forwarded_for","$geoip_country_code","$geoip_region",$geoip_region_name","$geoip_city",$geoip_latitude,$geoip_longitude,"$geoip_org"';
# access_log /var/log/nginx/access.log custom;

# fieldnames must match the custom log_format
fieldnames = ['remote_addr','remote_user','time_iso8601','host','request_method','server_protocol','scheme','request_uri','status','body_bytes_sent','http_referer','http_user_agent','http_x_forwarded_for','geoip_country_code','geoip_region','geoip_region_name','geoip_city','geoip_latitude','geoip_longitude', 'geoip_org']

# string lists for ignoring requests from bots, requests to static resources. basic substring match
ignore_user_agents = ['axibase', 'feedly', 'scollector', 'rome client', 'bot', 'crawl', 'qwant', 'slurp', 'spider', 'webmaster', 'faq', 'apache', 'scan']
ignore_uris = ['.png', '.js', '.css', '.woff', '.jpg', '.gif', '.jpeg', '.ico', '.svg', 'robots.txt', '/feed/', '.ttf', '.eot', 'wp-content', '.lzma', '.xz', '.bz2']
ignore_ip = ['10.20.30.40', '127.0.0.1']

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# Initialize services
svc = MessageService(connection)

def lookup(addr):
    try:
        return socket.gethostbyaddr(addr)[0]
    except socket.herror:
        return None

def has_containing_element(lst, str):
    for item in lst:
        if item in str:
            return True
    return False

# Current user must read permissions to access.log file, including after rollover
# sudo chmod 0644 /var/log/nginx/access.log
# sudo nano /etc/logrotate.d/nginx
#      create 0644 www-data adm
for line in tail("-F", "/var/log/nginx/access.log", _iter=True):
    reader = csv.DictReader([line.strip()], fieldnames=fieldnames)
    for row in reader:
        # print(row)

        # Ignore HEAD requests
        if row['request_method'] == 'HEAD':
          continue

        # Ignore HTTP>HTTPS requests
        if row['status'] == '301' and row['scheme'] == 'http':
          continue   

        # Ignore bots
        user_agent = row['http_user_agent'].lower()
        if has_containing_element(ignore_user_agents, user_agent):
          continue

        # Ignore static file requests
        ruri = row['request_uri'].lower()
        if has_containing_element(ignore_uris, ruri):
          continue

	      # Ignore 404 requests for apt language translation files
        if row['status'] == '404' and '/repository/deb/./' in ruri:
          continue
   
        # Ignore requests from ignored IP addresses
        radr = row['remote_addr']
        if has_containing_element(ignore_ip, radr):
          continue 

        dns = lookup(radr)
        if dns != None and 'localhost' not in dns:
          row['remote_host'] = dns

        # Handle proxy-forwarded requests
        xadr = row['http_x_forwarded_for']       
        if xadr != None and xadr != '-':
          if has_containing_element(ignore_ip, xadr):
            continue
          xdns = lookup(xadr)
          if xdns != None and 'localhost' not in xdns:
            row['remote_x_host'] = xdns

        sev = Severity.NORMAL

        # Remove original timestamp in the access log
        del row['time_iso8601']

        # Remove tags with default (unknown) value -
        tags = { k:v for k,v in row.items() if v!='-' }   

        # Replace example.org with actual DNS name
        msg = Message('web', 'access.log', 'example.org', datetime.now(), sev, tags, '')

        try:
          res = svc.insert(msg)
          print(res, msg.date, msg.tags)
        except IOError as ioe:
          print "IOError ({0}):{1}".format(ioe.errno,ioe.strerror)
          print(msg.date, msg.tags)
        except:
          print('Other error')
          print(msg.date, msg.tags)	
