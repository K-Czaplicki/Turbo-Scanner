import requests
import time
import os
import sys

http = requests.get('http://localhost:5000/add')
cookies = http.cookies

html = http.text
token = html[html.index('csrf_token" value="')+19:html.index('csrf_token" value="')+59]
print(token)
target = sys.argv[1]
target = target[target.index('://')+3:-1]
print(target)

try:
    with open("current_tag.txt", "r") as f:
        i = f.read()
except:
    print('Creating file')
if(i==''):
    i=0
with open("current_tag.txt", "w") as f:
    f.write(str(int(i)+1))

answer = requests.post('http://localhost:5000/add', cookies=cookies, data={"csrf_token":token, "targets":target, "file":"", "tag":str(int(i)+1),"priority":"normal", "choose_modules_to_enable=":"1", "module_enabled_bruter":"", "module_enabled_crtsh":"", "module_enabled_directory_index":"", "module_enabled_dns_reaper":"", "module_enabled_dns_scanner":"", "module_enabled_domain_expiration_scanner":"", "module_enabled_drupal_scanner":"", "module_enabled_ftp_bruter":"", "module_enabled_gau":"", "module_enabled_joomla_scanner":"", "module_enabled_mail_dns_scanner":"", "module_enabled_mysql_bruter":"", "module_enabled_nuclei":"", "module_enabled_port_scanner":"", "module_enabled_postgresql_bruter":"", "module_enabled_postman":"", "module_enabled_ReverseDNSLookup":"", "module_enabled_robots":"", "module_enabled_scripts_unregistered_domains":"", "module_enabled_sqlmap":"", "module_enabled_ssh_bruter":"", "module_enabled_ssl_checks":"", "module_enabled_vcs":"", "module_enabled_wordpress_bruter":"", "module_enabled_wordpress_plugins":"", "module_enabled_wp_scanner":""})

num_tasks=100
while(num_tasks != 0):
    time.sleep(30)
    url = 'http://localhost:5000/api/num-queued-tasks'
    headers = {
        'accept': 'application/json',
        'x-api-token': '1',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    num_tasks=int(response.text)
    print(num_tasks)

# +str(int(i)+1)
os.system("Artemis/scripts/run_docker_compose build --quiet autoreporter")
report_path = os.popen('sudo Artemis/scripts/run_docker_compose run autoreporter python3 -m artemis.reporting.export.main "$@" --tag '+str(int(i)+1)).read()
report_path = 'Artemis/' + report_path[report_path.index('written to:')+12:-1] + '/' + target + '.html'
time.sleep(30)
os.system("mkdir "+sys.argv[1].replace('://', ''))
os.system('sudo mv ' + report_path + ' ' + sys.argv[1].replace('://', '')+'art.html')

print(report_path)

