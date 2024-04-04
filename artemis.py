import requests
import time
import os
import sys

http = requests.get('http://localhost:5000/add')
cookies = http.cookies

html = http.text
token = html[html.index('csrf_token" value="')+19:html.index('csrf_token" value="')+59]

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

requests.post('http://localhost:5000/add', cookies=cookies, data={"csrf_token":token, "targets":target, "file":"", "tag":str(int(i)+1), "choose_modules_to_enable=":"", "module_enabled_bruter":"", "module_enabled_crtsh":"", "module_enabled_directory_index":"", "module_enabled_dns_reaper":"", "module_enabled_dns_scanner":"", "module_enabled_domain_expiration_scanner":"", "module_enabled_drupal_scanner":"", "module_enabled_ftp_bruter":"", "module_enabled_gau":"", "module_enabled_joomla_scanner":"", "module_enabled_mail_dns_scanner":"", "module_enabled_mysql_bruter":"", "module_enabled_nuclei":"", "module_enabled_port_scanner":"", "module_enabled_postgresql_bruter":"", "module_enabled_postman":"", "module_enabled_ReverseDNSLookup":"", "module_enabled_robots":"", "module_enabled_scripts_unregistered_domains":"", "module_enabled_sqlmap":"", "module_enabled_ssh_bruter":"", "module_enabled_ssl_checks":"", "module_enabled_vcs":"", "module_enabled_wordpress_bruter":"", "module_enabled_wordpress_plugins":"", "module_enabled_wp_scanner":""})

num_tasks=100
while(num_tasks != 0):
    num_tasks = int(requests.get('http://localhost:5000/api/num-queued-tasks').text)
    print(num_tasks)
    time.sleep(30)

# +str(int(i)+1)
report_path = os.popen("sudo /home/skaner/Artemis/scripts/export_emails --tag "+str(int(i)+1)).read()
report_path = '/home/skaner/Artemis/' + report_path[report_path.index('written to:')+12:-1] + '/' + target + '.html'
time.sleep(30)
os.system("mkdir "+sys.argv[1].replace('://', ''))
os.system('sudo mv ' + report_path + ' ' + sys.argv[1].replace('://', '')+'art.html')

print(report_path)

