import numpy as np 
import matplotlib.pyplot as plt 
import pickle, os
from glob import glob
from StoReS import * 
import tools21cm as t2c 
from tqdm import tqdm 

box_len  = 244/0.7
save_dir = '../../'
eor_hist = {}

xf_url = 'https://ttt.astro.su.se/~gmell/244Mpc/LB1/'
dn_url = 'https://ttt.astro.su.se/~gmell/244Mpc/densities/nc250/coarser_densities/'
url_dict = {'xfrac': xf_url, 'dens': dn_url, }
c2r = C2RAY(work_dir=save_dir)
c2r.set_links(url_dict)
zs = np.intersect1d(c2r.zs_dict['xfrac'], c2r.zs_dict['dens'])
xs = []
for i,z in tqdm(enumerate(zs)):
	# z = 6.905
	data = c2r.get_data_z(z)
	xf = data['xfrac']
	dn = data['dens']
	xs.append(xf.mean())
	os.remove(data['xfrac_filename'])
	os.remove(data['dens_filename'])
xs = np.array(xs)
eor_hist['LB1'] = {'z': zs, 'x': xs}

fig, ax = plt.subplots(1,1,figsize=(6,5))
fig.suptitle('Dixon et al. (2016)')
ax.plot(eor_hist['LB1']['z'], eor_hist['LB1']['x'], lw=3, label='LB1')
ax.set_xlabel('z', fontsize=14)
ax.set_ylabel('$x_\mathrm{HII}$', fontsize=14)
ax.legend()
ax.axis([6,14,-0.01,1.01])
plt.tight_layout()
plt.show()


xf_url = 'https://ttt.astro.su.se/~gmell/244Mpc/LB2/'
dn_url = 'https://ttt.astro.su.se/~gmell/244Mpc/densities/nc250/coarser_densities/'
url_dict = {'xfrac': xf_url, 'dens': dn_url, }
c2r = C2RAY(work_dir=save_dir)
c2r.set_links(url_dict)
zs = np.intersect1d(c2r.zs_dict['xfrac'], c2r.zs_dict['dens'])
xs = []
for i,z in tqdm(enumerate(zs)):
	# z = 6.905
	data = c2r.get_data_z(z)
	xf = data['xfrac']
	dn = data['dens']
	xs.append(xf.mean())
	os.remove(data['xfrac_filename'])
	os.remove(data['dens_filename'])
xs = np.array(xs)
eor_hist['LB2'] = {'z': zs, 'x': xs}


xf_url = 'https://ttt.astro.su.se/~gmell/244Mpc/LB3/'
dn_url = 'https://ttt.astro.su.se/~gmell/244Mpc/densities/nc250/coarser_densities/'
url_dict = {'xfrac': xf_url, 'dens': dn_url, }
c2r = C2RAY(work_dir=save_dir)
c2r.set_links(url_dict)
zs = np.intersect1d(c2r.zs_dict['xfrac'], c2r.zs_dict['dens'])
xs = []
for i,z in tqdm(enumerate(zs)):
	# z = 6.905
	data = c2r.get_data_z(z)
	xf = data['xfrac']
	dn = data['dens']
	xs.append(xf.mean())
	os.remove(data['xfrac_filename'])
	os.remove(data['dens_filename'])
xs = np.array(xs)
eor_hist['LB3'] = {'z': zs, 'x': xs}


xf_url = 'https://ttt.astro.su.se/~gmell/244Mpc/LB4/'
dn_url = 'https://ttt.astro.su.se/~gmell/244Mpc/densities/nc250/coarser_densities/'
url_dict = {'xfrac': xf_url, 'dens': dn_url, }
c2r = C2RAY(work_dir=save_dir)
c2r.set_links(url_dict)
zs = np.intersect1d(c2r.zs_dict['xfrac'], c2r.zs_dict['dens'])
xs = []
for i,z in tqdm(enumerate(zs)):
	# z = 6.905
	data = c2r.get_data_z(z)
	xf = data['xfrac']
	dn = data['dens']
	xs.append(xf.mean())
	os.remove(data['xfrac_filename'])
	os.remove(data['dens_filename'])
xs = np.array(xs)
eor_hist['LB4'] = {'z': zs, 'x': xs}


fig, ax = plt.subplots(1,1,figsize=(7,6))
fig.suptitle('Dixon et al. (2016)')
ax.plot(eor_hist['LB1']['z'], 1-eor_hist['LB1']['x'], lw=3, ls='-',  label='LB1')
ax.plot(eor_hist['LB2']['z'], 1-eor_hist['LB2']['x'], lw=3, ls='--', label='LB2')
ax.plot(eor_hist['LB3']['z'], 1-eor_hist['LB3']['x'], lw=3, ls='-.', label='LB3')
ax.plot(eor_hist['LB4']['z'], 1-eor_hist['LB4']['x'], lw=3, ls=':',  label='LB4')
ax.set_xlabel('z', fontsize=14)
ax.set_ylabel('$x_\mathrm{HI}$', fontsize=14)
ax.legend()
ax.axis([6,14,-0.01,1.01])
plt.tight_layout()
plt.show()

