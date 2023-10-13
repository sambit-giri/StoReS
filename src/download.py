import os, time
import wget, pkg_resources

def get_file_full_list(url, ext=''):
	import requests
	from bs4 import BeautifulSoup
	page = requests.get(url).text
	soup = BeautifulSoup(page, 'html.parser')
	file_list = [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
	return file_list


def download_simulation(link_to_file, save_dir, verbose=True, overwrite=False):
	local_path = save_dir+'/{}'.format(link_to_file.split('/')[-1])
	if not os.path.exists(local_path) or overwrite:
		if verbose: print('Downloading simulation...')
		wget.download(link_to_file,   save_dir)
		print('\n')
		if verbose: print('...done')
	else:
		if verbose: print('The file already exists.')
	return local_path

