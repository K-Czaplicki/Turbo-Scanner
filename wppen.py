import json
import os
import cloudscraper
import time
from time import gmtime, strftime
from semantic_version import SimpleSpec
from semantic_version import Version
import sys

def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

target = 'http://wppentest.j.pl/'
target = sys.argv[1]

filename = target.replace('://', '')+'/wpscan'
cmd = 'wpscan --url '+target+' --ignore-main-redirect --plugins-detection mixed -o '+filename+'.json -f json'
#print(cmd+'\n')
os.system(cmd)
f = open(filename+'.json')
data = json.load(f)
f.close()

url_wp_theme  = "https://wpscan.com/theme/"
url_wp_plugin = "https://wpscan.com/plugin/"

def num_there(s):
    return any(i.isdigit() for i in s)

# THEME
print("##### THEME #####")
if(data['main_theme'] != None):
	print("------> "+data['main_theme']['slug']+" <------")
	scraper = cloudscraper.create_scraper()
	site = scraper.get(url_wp_theme+data['main_theme']['slug']+'/').text
	indexes_vulns = list(find_all(site, 'vulnerabilities__table--row'))
	for i in range(len(indexes_vulns)):
		cutted = site[indexes_vulns[i]:]
		ahref_index = cutted.index('a href')
		div_index = ahref_index+cutted[ahref_index:].index('div')
		vuln = cutted[ahref_index+8:div_index]
		url = vuln[:vuln.index('"')]
		title = vuln[vuln.index('>')+4:]
		title = title[:title.index('<')]
		while(not title[-1].isalpha()):
				title = title[:-1]
		title = html_decode(title)
		print('    number: '+data['main_theme']['version']['number'])
		divided = title.split(' ')
		for a in range(len(divided)):
			if("." in divided[a] and num_there(divided[a])):
				if('<' in divided[a-1] or '=' in divided[a-1] or '>' in divided[a-1]):
					vuln_ver = divided[a-1]+divided[a]
				else:
					vuln_ver = divided[a]

		if(data['main_theme']['version'] == None or SimpleSpec(vuln_ver).match(Version(data['main_theme']['version']['number']))):
			print('    -> '+title+' -> '+url)


# PLUGINS
print("##### PLUGINS #####")

plugins_name = []
plugins_version = []
for i in data['plugins']:
	plugins_name.append(i)
	plugins_version.append(data['plugins'][i]['version'])

for j in range(len(plugins_name)):
	print("------> "+plugins_name[j]+" <------")

	if(plugins_version[j] != None):
		for key, value in plugins_version[j].items():
			if(key == "number" and len(value.split("."))==2):
				plugins_version[j]['number'] = plugins_version[j]['number'] + ".0"
			print('    '+key+': '+str(value))
	else:
		print('    number: ?')

	print("    ---- VULNS ----")

	scraper = cloudscraper.create_scraper()
	site = scraper.get(url_wp_plugin+plugins_name[j]+'/').text
	indexes_vulns = list(find_all(site, 'vulnerabilities__table--row'))
	if(len(indexes_vulns) != 0):
		for i in range(len(indexes_vulns)):
			cutted = site[indexes_vulns[i]:]
			ahref_index = cutted.index('a href')
			div_index = ahref_index+cutted[ahref_index:].index('div')
			vuln = cutted[ahref_index+8:div_index]
			url = vuln[:vuln.index('"')]
			title = vuln[vuln.index('>')+4:]
			title = title[:title.index('<')]
			while(not title[-1].isalpha()):
				title = title[:-1]
			title = html_decode(title)
			divided = title.split(' ')
			for a in range(len(divided)):
				if("." in divided[a] and num_there(divided[a])):
					if('<' in divided[a-1] or '=' in divided[a-1] or '>' in divided[a-1]):
						vuln_ver = divided[a-1]+divided[a]
					else:
						vuln_ver = divided[a]

			if(plugins_version[j] != None):
				for key, value in plugins_version[j].items():
					if(key == 'number'):
						if(SimpleSpec(vuln_ver).match(Version(value))):
							print('    -> '+title+' -> '+url)
			else:
				print('    -> '+title+' -> '+url)

	print('')
	time.sleep(10)
