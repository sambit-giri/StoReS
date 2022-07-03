import numpy as np 
import matplotlib.pyplot as plt 
import pickle
from glob import glob
from StoReS import * 
import tools21cm as t2c 

box_len  = 244/0.7
save_dir = '../../'

xf_url = 'https://ttt.astro.su.se/~gmell/244Mpc/LB1/'
dn_url = 'https://ttt.astro.su.se/~gmell/244Mpc/densities/nc250/coarser_densities/'
url_dict = {'dens': dn_url, 'xfrac': xf_url}

c2r = C2RAY(work_dir=save_dir)
c2r.set_links(url_dict)
z = 6.905
data = c2r.get_data_z(z)
xf = data['xfrac']
dn = data['dens']

# dn_file_link = 'https://ttt.astro.su.se/~gmell/244Mpc/densities/nc250/coarser_densities/6.905n_all.dat'
# xf_file_link = 'https://ttt.astro.su.se/~gmell/244Mpc/LB1/xfrac3d_6.905.bin'
# dn_filename = download_simulation(dn_file_link, save_dir, verbose=True, overwrite=False)
# xf_filename = download_simulation(xf_file_link, save_dir, verbose=True, overwrite=False)
# print(dn_filename, xf_filename)
# dn = t2c.DensityFile(dn_filename).cgs_density
# xf = t2c.XfracFile(xf_filename).xi

print(dn.shape, xf.shape)

fig, axs = plt.subplots(1,2,figsize=(13,6))
axs[0].pcolormesh(np.linspace(0,box_len,dn.shape[0]+1), 
				  np.linspace(0,box_len,dn.shape[1]+1), 
				  dn[:,:,0],
				  cmap='jet')
axs[0].set_xlabel('[Mpc]', fontsize=13)
axs[0].set_ylabel('[Mpc]', fontsize=13)
axs[1].pcolormesh(np.linspace(0,box_len,xf.shape[0]+1), 
				  np.linspace(0,box_len,xf.shape[1]+1), 
				  xf[:,:,0],
				  cmap='jet')
axs[1].set_xlabel('[Mpc]', fontsize=13)
axs[1].set_ylabel('[Mpc]', fontsize=13)
plt.tight_layout()
plt.show()


fig, axs = plt.subplots(1,2,figsize=(13,6))
dt = t2c.calc_dt(xf, dn, z)
ps, ks = t2c.power_spectrum_1d(dt, kbins=20, box_dims=box_len)
axs[0].pcolormesh(np.linspace(0,box_len,dt.shape[0]+1), 
				  np.linspace(0,box_len,dt.shape[1]+1), 
				  dt[:,:,0],
				  cmap='jet')
axs[0].set_xlabel('[Mpc]', fontsize=13)
axs[0].set_ylabel('[Mpc]', fontsize=13)
axs[1].loglog(ks, ps*ks**3/2/np.pi**2, lw=3, 
	label='$z={:.3f}$, $x_\mathrm{{HII}}={:.1f}$'.format(z,xf.mean()))
axs[1].legend(fontsize=14)
axs[1].set_xlabel('$k$ [1/Mpc]', fontsize=13)
axs[1].set_ylabel('$k^3 P/(2\pi^2)$ [mK$^2$]', fontsize=13)
plt.tight_layout()
plt.show()



