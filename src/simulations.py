import numpy as np 
from .functions import nearest_element_idx
from .download import * 
import tools21cm as t2c 

class C2RAY:
	'''
	The class to retrieve C2Ray simulations.
	
	'''
	def __init__(self, Nbody='CUBEP3M', work_dir='./', verbose=True):
		self.Nbody = Nbody
		self.verbose = verbose
		self.work_dir = work_dir 
		self.sim_file_list_dict = {}

	def set_nbody(self, nbody_url, info_type='dens', check_str='n_all.dat'):
		if self.Nbody.upper()=='CUBEP3M':
			nbody_file_list = get_file_full_list(nbody_url, ext='dat')
			file_list = []
			for ff in nbody_file_list: 
				if check_str in ff:
					file_list.append(ff)
			self.sim_file_list_dict[info_type] = file_list
		else:
			print('Method to retrieve {} outputs not implemented.'.format(nbody_file_list))

	def set_c2ray(self, c2ray_url, info_type='xfrac', check_str='xfrac3d_'):	# info_type='temp'
		c2ray_xfrac_file_list = get_file_full_list(c2ray_url, ext='bin')
		file_list = []
		for ff in c2ray_xfrac_file_list: 
			if check_str in ff:
				file_list.append(ff)
		self.sim_file_list_dict[info_type] = file_list

	def set_links(self, url_dict):
		zs_dict = {}
		self.set_nbody(url_dict['dens'], info_type='dens', check_str='n_all.dat')
		zs_dict['dens'] = np.array([ff.split('/')[-1].split('n')[0] for ff in self.sim_file_list_dict['dens']]).astype(float)
		self.set_c2ray(url_dict['xfrac'], info_type='xfrac', check_str='xfrac3d_')
		zs_dict['xfrac'] = np.array([ff.split('_')[-1].split('.b')[0] for ff in self.sim_file_list_dict['xfrac']]).astype(float)
		if 'temp' in url_dict.keys(): 
			self.set_c2ray(url_dict['temp'], info_type='temp', check_str='Temper3D_')
			zs_dict['temp'] = np.array([ff.split('_')[-1].split('.b')[0] for ff in self.sim_file_list_dict['temp']]).astype(float)
		if 'vel' in url_dict.keys():
			self.set_nbody(url_dict['vel'], info_type='vel', check_str='v_all.dat')
			zs_dict['vel'] = np.array([ff.split('/')[-1].split('v')[0] for ff in self.sim_file_list_dict['vel']]).astype(float)
		self.zs_dict = zs_dict
		
	def get_data_z(self, z):
		data = {}

		if z in self.zs_dict['xfrac']:
			az = nearest_element_idx(self.zs_dict['xfrac'], z, both=False)
			zz = self.zs_dict['xfrac'][az]
			ff = download_simulation(self.sim_file_list_dict['xfrac'][az], self.work_dir, verbose=self.verbose)
			xf = t2c.XfracFile(ff).xi 
		else:
			az0, az1 = nearest_element_idx(self.zs_dict['xfrac'], z, both=True)
			zz0, zz1 = self.zs_dict['xfrac'][az0], self.zs_dict['xfrac'][az1]
			ff0 = download_simulation(self.sim_file_list_dict['xfrac'][az0], self.work_dir, verbose=self.verbose)
			ff1 = download_simulation(self.sim_file_list_dict['xfrac'][az1], self.work_dir, verbose=self.verbose)
			xf0 = t2c.XfracFile(ff0).xi 
			xf1 = t2c.XfracFile(ff1).xi 
			ff  = [ff0,ff1]
			xf  = xf0 + (xf1-xf0)*(z-zz0)/(zz1-zz0)
		data['xfrac'] = xf 
		data['xfrac_filename'] = ff

		if z in self.zs_dict['dens']:
			az = nearest_element_idx(self.zs_dict['dens'], z, both=False)
			zz = self.zs_dict['dens'][az]
			ff = download_simulation(self.sim_file_list_dict['dens'][az], self.work_dir, verbose=self.verbose)
			dn = t2c.DensityFile(ff).cgs_density
		else:
			az0, az1 = nearest_element_idx(self.zs_dict['dens'], z, both=True)
			zz0, zz1 = self.zs_dict['dens'][az0], self.zs_dict['dens'][az1]
			ff0 = download_simulation(self.sim_file_list_dict['dens'][az0], self.work_dir, verbose=self.verbose)
			ff1 = download_simulation(self.sim_file_list_dict['dens'][az1], self.work_dir, verbose=self.verbose)
			dn0 = t2c.DensityFile(ff0).cgs_density
			dn1 = t2c.DensityFile(ff1).cgs_density
			ff  = [ff0,ff1]
			dn  = dn0 + (dn1-dn0)*(z-zz0)/(zz1-zz0)
		data['dens'] = dn 
		data['dens_filename'] = ff

		return data







