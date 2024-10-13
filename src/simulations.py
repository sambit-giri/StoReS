import numpy as np 
from .functions import nearest_element_idx
from .download import * 
import tools21cm as t2c 

def get_file_info(data_url, check_str, ext, verbose=True):
	data_file_list = get_file_full_list(data_url, ext=ext)
	if verbose: 
		print(f'Total length of data list at the url: {len(data_file_list)}')
	file_list = []
	for ff in data_file_list: 
		if check_str.lower() in ff.lower():
			file_list.append(ff)
	if verbose: 
		print(f'Length of data list with {check_str}: {len(file_list)}')
	return file_list

class GetData:
	'''
	The class to retrieve simulations from StoReS.
	
	'''
	def __init__(self, name='Untitled', work_dir='./', verbose=True, data_url=None,
			  			check_str='n_all.dat', ext='dat'):
		self.name = name
		self.verbose = verbose
		self.work_dir = work_dir 
		self.check_str = check_str
		self.ext = ext
		self.data_url = data_url
		if data_url is not None:
			self.set_link()
		self.file_list = []

	def set_link(self, data_url=None, check_str=None, ext=None):
		if data_url is None:
			data_url = self.data_url
		if check_str is None:
			check_str = self.check_str
		if ext is None:
			ext = self.ext
		print(f'Provided Data information:')
		print(f'Name     = {self.name}')
		print(f'check_str = {check_str}')
		print(f'ext       = {ext}')
		file_list = get_file_info(data_url, check_str, ext)
		self.file_list = file_list
		print(f'Number of files found: {len(file_list)}')
		if len(file_list)>0:
			print(f'The first file: {file_list[0]}')
		return file_list

	def get_zlist(self, converter_func=None):
		if converter_func is None:
			converter_func = lambda x: x
		zs_list = np.array([converter_func(ff) for ff in self.file_list])
		if len(zs_list)>0:
			print(f'The redshift of {self.file_list[0]} is {zs_list[0]}')
		self.zs_list = zs_list
		return zs_list

	def get_data_z(self, z, reader_func=None):
		if reader_func is None:
			reader_func = lambda ff: t2c.DensityFile(ff).cgs_density

		data_dir = self.work_dir
		if not os.path.isdir(data_dir): os.mkdir(data_dir)
		if z in self.zs_list:
			az = nearest_element_idx(self.zs_list, z, both=False)
			zz = self.zs_list[az]
			ff = download_simulation(self.file_list[az], data_dir, verbose=self.verbose)
			dn = reader_func(ff)
		else:
			az0, az1 = nearest_element_idx(self.zs_list, z, both=True)
			zz0, zz1 = self.zs_list[az0], self.zs_list[az1]
			ff0 = download_simulation(self.file_list[az0], data_dir, verbose=self.verbose)
			ff1 = download_simulation(self.file_list[az1], data_dir, verbose=self.verbose)
			dn0 = reader_func(ff0)
			dn1 = reader_func(ff1)
			ff  = [ff0,ff1]
			dn  = dn0 + (dn1-dn0)*(z-zz0)/(zz1-zz0)
			print(f'No data was found for z={z}. Therefore the output is linearly interpolated the results of data at z={zz0} and {zz1}.')
		return dn, ff


class C2RAY:
	'''
	The class to retrieve C2Ray simulations.
	
	'''
	def __init__(self, Nbody='CUBEP3M', work_dir='./', verbose=True, url_dict=None):
		self.Nbody = Nbody
		self.verbose = verbose
		self.work_dir = work_dir 
		self.url_dict = url_dict
		self.sim_file_list_dict = {}

	def set_nbody(self, nbody_url, info_type='dens', check_str='n_all.dat', ext='dat'):
		print(f'Provided N-Body information:')
		print(f'Nbody     = {self.Nbody}')
		print(f'info_type = {info_type}')
		print(f'check_str = {check_str}')
		print(f'ext       = {ext}')
		file_list = get_file_info(nbody_url, check_str, ext)
		self.sim_file_list_dict[info_type] = file_list
		print(f'Number of files found: {len(file_list)}')
		if len(file_list)>0:
			print(f'The first file: {file_list[0]}')
		# if self.Nbody.upper()=='CUBEP3M':
		# 	nbody_file_list = get_file_full_list(nbody_url, ext=ext)
		# 	file_list = []
		# 	for ff in nbody_file_list: 
		# 		if check_str in ff.lower():
		# 			file_list.append(ff)
		# 	self.sim_file_list_dict[info_type] = file_list
		# else:
		# 	print('Method to retrieve {} outputs not implemented.'.format(nbody_file_list))

	def set_c2ray(self, c2ray_url, info_type='xfrac', check_str='xfrac3d_', ext='bin'):	# info_type='temp'
		print(f'Provided C2Ray information:')
		print(f'info_type = {info_type}')
		print(f'check_str = {check_str}')
		print(f'ext       = {ext}')
		file_list = get_file_info(c2ray_url, check_str, ext)
		self.sim_file_list_dict[info_type] = file_list
		print(f'Number of files found: {len(file_list)}')
		if len(file_list)>0:
			print(f'The first file: {file_list[0]}')
			
		# c2ray_xfrac_file_list = get_file_full_list(c2ray_url, ext=ext)
		# file_list = []
		# for ff in c2ray_xfrac_file_list: 
		# 	if check_str.lower() in ff.lower():
		# 		file_list.append(ff)
		# self.sim_file_list_dict[info_type] = file_list
		# # print(file_list)

	def set_links(self, url_dict=None):
		if url_dict is None:
			url_dict = self.url_dict
		else:
			self.url_dict = url_dict
		zs_dict = {}
		if 'dens' in url_dict.keys(): 
			self.set_nbody(url_dict['dens'], info_type='dens', check_str='n_all.dat')
			zs_dict['dens'] = np.array([ff.split('/')[-1].split('n')[0] for ff in self.sim_file_list_dict['dens']]).astype(float)
		if 'xfrac' in url_dict.keys(): 
			self.set_c2ray(url_dict['xfrac'], info_type='xfrac', check_str='xfrac3d_')
			zs_dict['xfrac'] = np.array([ff.split('_')[-1].split('.b')[0] for ff in self.sim_file_list_dict['xfrac']]).astype(float)
		if 'temp' in url_dict.keys(): 
			self.set_c2ray(url_dict['temp'], info_type='temp', check_str='temper3d_')
			zs_dict['temp'] = np.array([ff.split('_')[-1].split('.b')[0] for ff in self.sim_file_list_dict['temp']]).astype(float)
		if 'vel' in url_dict.keys():
			self.set_nbody(url_dict['vel'], info_type='vel', check_str='v_all.dat')
			zs_dict['vel'] = np.array([ff.split('/')[-1].split('v')[0] for ff in self.sim_file_list_dict['vel']]).astype(float)
		self.zs_dict = zs_dict

	def get_density_data_z(self, z, reader_func=None):
		if reader_func is None:
			reader_func = lambda ff: t2c.DensityFile(ff).cgs_density

		try:
			data_dir = self.work_dir['dens']
		except:
			data_dir = self.work_dir
		if not os.path.isdir(data_dir): os.mkdir(data_dir)
		if z in self.zs_dict['dens']:
			az = nearest_element_idx(self.zs_dict['dens'], z, both=False)
			zz = self.zs_dict['dens'][az]
			ff = download_simulation(self.sim_file_list_dict['dens'][az], data_dir, verbose=self.verbose)
			dn = reader_func(ff)
		else:
			az0, az1 = nearest_element_idx(self.zs_dict['dens'], z, both=True)
			zz0, zz1 = self.zs_dict['dens'][az0], self.zs_dict['dens'][az1]
			ff0 = download_simulation(self.sim_file_list_dict['dens'][az0], data_dir, verbose=self.verbose)
			ff1 = download_simulation(self.sim_file_list_dict['dens'][az1], data_dir, verbose=self.verbose)
			dn0 = reader_func(ff0)
			dn1 = reader_func(ff1)
			ff  = [ff0,ff1]
			dn  = dn0 + (dn1-dn0)*(z-zz0)/(zz1-zz0)
		return dn, ff

	def get_ionisation_data_z(self, z, reader_func=None):
		if reader_func is None:
			reader_func = lambda ff: t2c.XfracFile(ff).xi 
		try:
			data_dir = self.work_dir['xfrac']
		except:
			data_dir = self.work_dir
		if not os.path.isdir(data_dir): os.mkdir(data_dir)
		if z in self.zs_dict['xfrac']:
			az = nearest_element_idx(self.zs_dict['xfrac'], z, both=False)
			zz = self.zs_dict['xfrac'][az]
			ff = download_simulation(self.sim_file_list_dict['xfrac'][az], data_dir, verbose=self.verbose)
			xf = reader_func(ff) 
		else:
			az0, az1 = nearest_element_idx(self.zs_dict['xfrac'], z, both=True)
			zz0, zz1 = self.zs_dict['xfrac'][az0], self.zs_dict['xfrac'][az1]
			ff0 = download_simulation(self.sim_file_list_dict['xfrac'][az0], data_dir, verbose=self.verbose)
			ff1 = download_simulation(self.sim_file_list_dict['xfrac'][az1], data_dir, verbose=self.verbose)
			xf0 = reader_func(ff0) 
			xf1 = reader_func(ff1)
			ff  = [ff0,ff1]
			xf  = xf0 + (xf1-xf0)*(z-zz0)/(zz1-zz0)
		return xf, ff
		
	def get_data_z(self, z):
		data = {}

		xf, ff = self.get_ionisation_data_z(z)
		data['xfrac'] = xf 
		data['xfrac_filename'] = ff

		dn, ff = self.get_density_data_z(z)
		data['dens'] = dn 
		data['dens_filename'] = ff

		return data







