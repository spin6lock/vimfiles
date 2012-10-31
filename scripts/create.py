#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

header = '''#!/usr/bin/env bash

function color_echo() {
	echo -e "\e[1;33m$@\e[0m"
}

bundle_path=~/.vim/bundle
mkdir -p $bundle_path
cd $bundle_path
'''

template = '''
if [ ! -d "%s" ]; then
	color_echo "Downloading %s"
	%s
fi
'''

bundle_filename = 'bundle.json'
download_filename = 'download.sh'

def main():
	with open(bundle_filename) as fh:
		lines = fh.readlines()
		plugins_json = ''.join(lines)
	plugins_info = json.loads(plugins_json)
	plugins = plugins_info["plugins"]
	commands = []
	for name_repo in plugins:
		name, repo_url= name_repo['name'], name_repo['repo']
		name += '.git'
		repo_command = 'git clone --depth 1 %s' % (repo_url, )
		"""
		elif repo_type == 'hg':
			repo_command = 'hg clone -r -1 %s %s' % (repo_url, repo_name)
		elif repo_type == 'svn':
			repo_command = 'svn checkout %s %s' % (repo_url, repo_name)
		"""
		command = template % (name, name, repo_command)
		commands.append(command)

	with open(download_filename, 'w') as download_file:
		download_file.write(header)
		download_file.write(''.join(commands))

	os.chmod(download_filename, 0744) # rwxr-xr-x
	print './%s created, double check then run it.' % download_filename

if __name__ == '__main__':
	main()
