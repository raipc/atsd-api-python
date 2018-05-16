from atsd_client import connect_url
from atsd_client.models import *
from atsd_client.services import *
import socket
from datetime import datetime
from sh import tail
import csv
import logging

logger = logging.getLogger()
logger.disabled = True

# nginx must be configured to write logs in CSV format
#
# geoip_country /etc/nginx/geoip/GeoIP.dat; # the country IP database
# geoip_city /etc/nginx/geoip/GeoLiteCity.dat; # the city IP database
# log_format custom '"$remote_addr","$remote_user","$time_iso8601","$host","$request_method","$server_protocol","$scheme","$request_uri",$status,$body_bytes_sent,"$http_refe$
# access_log /var/log/nginx/access.log custom;

# fieldnames must match the custom log_format
fieldnames = ['remote_addr','remote_user','time_iso8601','host','request_method','server_protocol','scheme','request_uri','status','body_bytes_sent','http_referer','http_user_agent','http_x_forwarded_for','geoip_country_code','geoip_region','geoip_region_name','geoip_city','geoip_latitude','geoip_longitude']

# string lists for ignoring requests from bots, requests to static resources. basic substring match
ignore_user_agents = ['axibase', 'feedly', 'scollector', 'rome client', 'bot', 'crawl', 'qwant', 'slurp', 'spider', 'webmaster', 'faq', 'apache', 'scan']
ignore_uris = ['.png', '.js', '.css', '.woff', '.jpg', '.gif', '.ico', 'robots.txt', '/feed/', '.ttf', '.eot', 'wp-content']
ignore_ip = ['10.20.30.40', '10.20.30.50']

def lookup(addr):
    try:
        return socket.gethostbyaddr(addr)
    except socket.herror:
        return None, None, None

conn = connect_url('https://atsd_hostname:8443', 'user', 'passwd')

svc = MessageService(conn)

# runs forever
for line in tail("-F", "/var/log/nginx/access.log", _iter=True):
    reader = csv.DictReader([line.strip()], fieldnames=fieldnames)
    for row in reader:
        # print(row)

        # Ignore HEAD requests
        if row['request_method'] == 'HEAD':
          continue

        # Ignore HTTP to HTTPS redirects
        if row['status'] == '301' and row['scheme'] == 'http':
          continue   

        store=True

        # Ignore records with http_user_agent matching ignore_user_agents list       
        user_agent = row['http_user_agent'].lower()
        for ua in ignore_user_agents:
          if ua in user_agent:
              store=False

        if store==False:continue

        # Ignore records with request_uri matching ignore_uris list            
        ruri = row['request_uri'].lower()
        for ur in ignore_uris:
          if ur in ruri:
              store=False

        if store==False:continue   

        # Ignore records with remote_addr matching ignore_ip list
        radr = row['remote_addr']
        for ar in ignore_ip:
          if ar in radr:
              store=False

        if store==False:continue

        # Reverse-resolve IP and set remote_host field in the row object
        dns = lookup(radr)[0]
        if dns != None and dns != 'localhost':
          row['remote_host'] = dns

        # Remove original timestamp in the access log
        del row['time_iso8601']

        # Remove tags with default (unknown) value -
        tags = { k:v for k,v in row.items() if v!='-' }       

        # Replace example.org with the dns name of your server
        msg = Message('web', 'access.log', 'example.org', datetime.now(), Severity.NORMAL, tags, '')
        res = svc.insert(msg)
        #print(res, msg.date, msg.tags)
