from atsd_client import connect

'''
Establishes a connection to ATSD, returns ATSD version, timezone and current time.
'''

# Connect to ATSD server
connection = connect('/path/to/connection.properties')

# query version info from ATSD
response = connection.get('v1/version')

build_info = response['buildInfo']
date = response['date']

print('Version: %s ' % build_info['revisionNumber'])
print('Timezone: %s ' % date['timeZone']['name'])
print('Current date: %s ' % date['currentDate'])
