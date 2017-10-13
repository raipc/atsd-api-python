from atsd_client import connect_url

'''
Establishes a connection to ATSD, returns ATSD version, timezone and current time.
'''

# Connect to an ATSD server
connection = connect_url('https://atsd_hostname:8443', 'user', 'password')

# query version info from ATSD
response = connection.get('v1/version')

build_info = response['buildInfo']
date = response['date']

print('Version: %s ' % build_info['revisionNumber'])
print('Timezone: %s ' % date['timeZone']['name'])
print('Current date: %s ' % date['currentDate'])
