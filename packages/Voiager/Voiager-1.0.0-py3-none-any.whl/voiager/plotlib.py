import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import optimize
import getdist
from getdist import plots
from abel.direct import direct_transform as abel
from voiager import datalib

# Plot parameters
mpl.use('Agg')
plt.rcParams['figure.dpi'] = 400
plt.rcParams.update({'figure.max_open_warning': 0})
mpl.rc('font', family='serif', size=18)
mpl.rc('text', usetex=True)
mpl.rc('xtick',labelsize=14)
mpl.rc('ytick',labelsize=14)
figsize = (6.4,4.8) # figure size
ms = 4 # marker size
lw = 1.2 # line width
fs = 20 # font size
cs = 3 # cap size of error bars
mew = 0.3 # marker edge width
vmin = -1 # minimum for contour map
vmax = 0.6 # maximum for contour map
Nlev = int((vmax-vmin)*10 + 1) # number of contour lines
lev = np.linspace(vmin,vmax,Nlev) + 0.03 # contour values
symbol = ['o','^','v','D','s','p','<','>'] # marker symbols
#color = ['b','r','g','y','c','m','k','w'] # standard colors
color = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:olive','tab:cyan'] # tableau colors
#color = ['darkblue','darkred','darkgreen','darkorange','darkviolet','darkcyan','darkseagreen','darkgoldenrod'] # dark colors
line = ['-','--',':','-.',(5, (10, 3)),(0, (5, 10)),(0, (3, 10, 1, 10)),(0, (3, 5, 1, 5, 1, 5))] # line styles


def voidSky(Xv, Xvr=None, plotPath='plots/'):
    """Plot angular distribution of void centers on the sky.

    Args:
        Xv (ndarray,[len(Xv),3]): RA, Dec, redshift of void centers
        Xvr (ndarray,[len(Xvr),3]): RA, Dec, redshift of void center randoms (default = None)
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        void_sky.png (image file): Mollweide projection of void distribution on the sky, color-coded by redshift
    """
    plt.figure(figsize=figsize)
    plt.subplot(111, projection="mollweide")
    plt.scatter(Xv[:,0], Xv[:,1], s=1, c=Xv[:,2], alpha=0.3, edgecolors='none', marker='.')
    if Xvr is not None:
        plt.scatter(Xvr[:,0], Xvr[:,1], s=0.05, c='k', alpha=0.1, edgecolors='none', marker='.')
    plt.grid(linestyle='-', linewidth=0.2)
    plt.xlabel(r'RA', fontsize=14)
    plt.ylabel(r'Dec', fontsize=14)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.savefig(Path(plotPath) / 'void_sky.png', format='png', bbox_inches="tight", dpi=800)
    plt.clf()


def voidBox(xv, zv, azim=45., elev=-120., plotPath='plots/'):
    """Plot 3d distribution of void centers in a comoving box.

    Args:
        xv (ndarray,[len(xv),3]): comoving coordinates of void centers
        zv (ndarray,len(zv)): void redshifts
        azim (float): azimuthal viewing angle in degrees (default = 45.)
        elev (float): elevation viewing angle in degrees (default = -120.)
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        void_box.png (image file): 3d view of void centers in a box, color-coded by redshift
    """
    # plt.switch_backend('TKAgg')
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(projection='3d')
    ax.scatter(xv[:,0], xv[:,1], xv[:,2], s=0.5, c=zv, depthshade=True, marker='o', linewidths=mew)
    ax.set_xlabel(r'$X_1\,[h^{-1}\mathrm{Mpc}]$', fontsize=14)
    ax.set_ylabel(r'$X_2\,[h^{-1}\mathrm{Mpc}]$', fontsize=14)
    ax.set_zlabel(r'$X_3\,[h^{-1}\mathrm{Mpc}]$', fontsize=14)
    ax.tick_params(labelsize=10)
    ax.view_init(elev, azim)
    plt.savefig(Path(plotPath) / 'void_box.png', format='png', dpi=400)
    # plt.show()
    plt.clf()


def voidRedshift(rv, zv, rvr=None, zvr=None, plotPath='plots/'):
    """Plot redshift distribution for voids of different effective radius.

    Args:
        rv (ndarray,len(rv)): effective void radii
        zv (ndarray,len(zv)): void redshifts
        rvr (ndarray,len(rvr)): effective void radii randoms (default = None)
        zvr (ndarray,len(zvr)): void redshift randoms (default = None)
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        void_redshift.png (image file): void distribution across effective radius and redshift (color-coded)
    """
    plt.figure(figsize=figsize)
    plt.scatter(rv, zv, s=4, c=zv, alpha=0.3, edgecolors='none', marker='.')
    if rvr is not None:
        plt.scatter(rvr, zvr, s=0.2, c='k', alpha=0.1, edgecolors='none', marker='.')
    plt.xlabel(r'$R \; [h^{-1}\mathrm{Mpc}]$', fontsize=fs)
    plt.ylabel(r'$Z$', fontsize=fs)
    plt.savefig(Path(plotPath) / 'void_redshift.png', format='png', bbox_inches="tight", dpi=400)
    plt.clf()


def voidAbundance(yv, Nbin, zmin, zmax, sky, par_cosmo, ysymb, yunit, ystring, ylim=[1e-10,1e-5], yvr=None, Nmock=1, figFormat='pdf', plotPath='plots/'):
    """Plot void abundance as a function of void properties.

    Args:
        yv (ndarray,len(yv)): arbitrary void property (e.g., effective radius, redshift, core density, ellipticity)
        Nbin (int): number of bins
        zmin (float): minimum redshift
        zmax (float): maximum redshift
        sky (float): sky area in square degrees
        par_cosmo (dict): cosmological parameter values
        ysymb (str): mathematical symbol of void property
        yunit (str): unit of void property
        ystring (str): name of void property (abbreviation)
        ylim (tuple,2): lower and upper y-axis limit (default = 1e-10,1e-5)
        yvr (ndarray,len(yv)): void property random (default = None)
        Nmock (int): number of mock catalogs (default = 1)
        figFormat (str): format to save figure (default 'pdf')
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        n_ystring.pdf (pdf file): void abundance distribution
    """
    ym, nm, nE = datalib.voidAbundance(yv, Nbin, zmin, zmax, sky, par_cosmo, Nmock)
    plt.plot(ym, nm,color[0], lw=lw)
    plt.errorbar(ym, nm, yerr=nE, color = color[0], fmt = '.', lw=lw, ms=6, mew=mew, elinewidth=lw, capsize=cs)
    if yvr is not None:
        yrm, nrm, nrE = datalib.voidAbundance(yvr, Nbin, zmin, zmax, sky, par_cosmo, Nmock)
        plt.plot(yrm, nrm*nm.sum()/nrm.sum(), 'k:', ms=ms, mew=mew, lw=lw)
    plt.figtext(0.65,0.8, r'$N_\mathrm{v}\,=\,$'+str(len(yv)))
    plt.xlabel(r'$'+ysymb+r'\,'+yunit+'$', fontsize=fs)
    plt.ylabel(r'$\mathrm{d}n_\mathrm{v}('+ysymb+')/\mathrm{d}\ln '+ysymb+'\;[h^3\mathrm{Mpc}^{-3}]$', fontsize=fs)
    #plt.xlim((yv.min(),yv.max()))
    plt.ylim(ylim)
    plt.yscale('log')
    plt.savefig(Path(plotPath) / ('n_'+ystring+'.'+figFormat), format=figFormat, bbox_inches="tight")
    plt.clf()


def redshiftDistribution(zgm, zvm, ngm, nvm, zv=None, zgrm=None, zvrm=None, ngrm=None, nvrm=None, vbin='zv', binning='eqn', Nvbin=2, figFormat='pdf', plotPath='plots/'):
    """Plot redshift distribution of tracers (galaxies) and voids.

    Args:
        zgm, zvm (ndarray,Nbin_nz): mean redshift of tracers, voids per bin (arithmetic mean of bin edges)
        ngm, nvm (ndarray,Nbin_nz): mean number density of tracers, voids per bin
        zv (ndarray,len(zv)): void redshifts (default = None)
        zgrm, zvrm (ndarray,Nbin_nz): mean redshift of randoms per bin (default = None)
        ngrm, nvrm (ndarray,Nbin_nz): mean number density of randoms per bin (default = None)
        vbin (str): binning strategy, 'zv': void-redshift bins (default), 'rv': void-radius bins
        binning (str / list): 'eqn' for equal number of voids (default), 'lin' for linear, 'log' for logarithmic. Alternatively, provide a list for custom bin edges.
        Nvbin (int): number of void bins (default = 2)
        figFormat (str): format to save figure (default 'pdf')
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        n_zv.pdf (pdf file): redshift distribution of tracers and voids (redshift bins indicated if used)
    """
    plt.plot(zgm, ngm, color[1], ms=ms, mew=mew, lw=2, label=r'Galaxies')
    plt.plot(zvm, nvm, color[0], ms=ms, mew=mew, lw=2, label=r'Voids')
    if zgrm is not None: plt.plot(zgrm, ngrm*ngm.sum()/ngrm.sum(), 'k:', ms=ms, mew=mew, lw=1.5)
    if zvrm is not None: plt.plot(zvrm, nvrm*nvm.sum()/nvrm.sum(), 'k:', ms=ms, mew=mew, lw=1.5)
    if vbin == 'zv':
        zbins = datalib.getBins(zv, binning, Nvbin)
        for zbin in zbins: plt.axvline(x=zbin, c='k', linestyle='--', lw=1, alpha=0.3)
        #for i in range(len(zbins)-1): plt.text((zbins[i+1]+zbins[i])/2-0.04, 5e-7,'bin '+str(i+1), fontsize=14, alpha=0.3)
    plt.xlabel(r'$z$', fontsize=fs)
    plt.ylabel(r'$n(z) \; [h^3\mathrm{Mpc}^{-3}]$', fontsize=fs)
    plt.yscale('log')
    plt.legend(loc = 'best', prop={'size':16}, fancybox=True, shadow=True)
    plt.savefig(Path(plotPath) / ('n_redshift.'+figFormat), format=figFormat, bbox_inches="tight")
    plt.clf()


def tracerBias(zg, bg, figFormat='pdf', plotPath='plots/'):
    """Plot tracer (galaxy) bias as function of redshift.

    Args:
        zg (ndarray,len(zg)): tracer redshifts
        bg (ndarray,len(zg)): tracer bias
        figFormat (str): format to save figure (default 'pdf')
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        bias.pdf (pdf file): tracer bias as function of redshift
    """
    plt.plot(zg, bg, color[0], ms=ms, mew=mew, lw=2, label=r'Galaxies')
    plt.xlabel(r'$z$', fontsize=fs)
    plt.ylabel(r'$b(z)$', fontsize=fs)
    plt.legend(prop={'size':16}, fancybox=True, shadow=True)
    plt.savefig(Path(plotPath) / ('bias.'+figFormat), format=figFormat, bbox_inches="tight")
    plt.clf()


def xi_p_test(rs, rmi, rvi, xid, p0=[1,-0.8,2.,8.], Nvbin=2, rmax=3, figFormat='pdf', plotPath='plots/'):
    """Plot projected and deprojected correlation function for best-fit HSW profile as a test template.

    Args:
        rs (ndarray,len(rs)): radial distances from void center in units of void effective radius for template
        rmi (ndarray,[Nvbin,Nrbin]): radial distances from void center for each bin
        rvi (ndarray,Nvbin): average effective void radius per bin
        xid, xidE (ndarray,[Nvbin,Nrbin]): deprojected void-tracer correlation function
        p0 (ndarray,Npar): initial parameter values for HSW profile (default r_s=1, d_c=-0.8, a=2, b=8)
        Nvbin (int): number of void bins (default = 2)
        rmax (float): maximum distance from void center in units of effective void radius (default = 3)
        figFormat (str): format to save figure (default 'pdf')
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        xi_p_test.pdf (pdf file): projected and deprojected correlation function for best-fit HSW profile
    """
    for i in range(Nvbin):
        p1 = optimize.curve_fit(datalib.HSW, rmi[i]/rvi[i], xid[i], p0=p0)
        xit = datalib.HSW(rs, *p1[0])
        xitp = abel(xit, r=rs, direction='forward')
        xitd = abel(xitp, r=rs, direction='inverse')
        plt.figure(figsize=figsize)
        plt.plot([1e-4,1e3], [0,0], 'k-', lw=0.5)
        plt.plot(rs, xit, label=r'$\xi_{\scriptscriptstyle\mathrm{HSW}}(s)$', color=color[1], linestyle=line[0], lw=1.5*lw, alpha=1)
        plt.plot(rs, xitp, label=r'$\xi^s_\mathrm{p}(s_\perp)$', color=color[2], linestyle=line[1], lw=1.5*lw)
        plt.plot(rs, xitd, label=r'$\xi(r)$', color=color[0], linestyle=line[2], lw=2.5*lw)
        plt.xlabel(r'$s/R$', fontsize=fs)
        plt.ylabel(r'$\xi(s)$', fontsize=fs)
        plt.xlim(0,rmax)
        plt.ylim(-1,0.4)
        plt.yticks(np.linspace(-1,0.4,8))
        legend = plt.legend(loc = 4, prop={'size':18}, numpoints=1, markerscale=1.5, fancybox=True, shadow=True)
        legend.get_title().set_fontsize(18)
        plt.savefig(Path(plotPath) / ('xi_p_test_'+str(i+1)+'.'+figFormat), format=figFormat, bbox_inches="tight")
        plt.clf()


def xi_p(xip, xipE, xips, xid, xidE, xids, xi, xiE, xits, rmi, rs, rvi, zvi, p1, Nvbin=2, rmax=3, figFormat='pdf', plotPath='plots/'):
    """Plot projected and deprojected correlation function with its redshift-space monopole.

    Args:
        xip, xipE (ndarray,[Nvbin,Nrbin]): LOS projected void-tracer correlation function and its error
        xips (ndarray,[Nvbin,Nspline]): spline of LOS projected void-tracer correlation function
        xid, xidE (ndarray,[Nvbin,Nrbin]): deprojected void-tracer correlation function and its error
        xids (ndarray,[Nvbin,Nspline]): spline of deprojected void-tracer correlation function
        xi, xiE (ndarray,[Nvbin,len(ell),Nrbin]): multipoles of void-tracer correlation function and its error
        xits (ndarray,[Nvbin,len(ell),Nspline]): spline of theory model for multipoles of void-tracer correlation function
        rmi (ndarray,[Nvbin,Nrbin]): radial distances from void center for each bin
        rs (ndarray,Nspline): splined radial distances from void center in units of void effective radius
        rvi (ndarray,Nvbin): average effective void radius per bin
        zvi (ndarray,Nvbin): average void redshift per bin
        p1 (ndarray,[Nvbin,Npar]): best-fit model parameter values
        Nvbin (int): number of void bins (default = 2)
        rmax (float): maximum distance from void center in units of effective void radius (default = 3)
        figFormat (str): format to save figure (default 'pdf')
        plotPath (path): name of output path for plot (default = '/plots/')

    Returns:
        xi_p.pdf (pdf file): projected and deprojected correlation function with its redshift-space monopole (and best fit)
    """
    for i in range(Nvbin):
        plt.figure(figsize=figsize)
        plt.plot([1e-4,1e3], [0,0], 'k-', lw=0.5)
        plt.errorbar(rmi[i]/rvi[i], xip[i], label=r'$\xi^s_\mathrm{p}(s_\perp)$', yerr = xipE[i], color=color[2], fmt = 'v', lw=lw, ms=ms, mew=mew, elinewidth=lw, capsize=cs)
        plt.errorbar(rmi[i]/rvi[i], xid[i], label=r'$\xi(r)$', yerr = xidE[i], color=color[1], fmt = '^', lw=lw, ms=ms, mew=mew, elinewidth=lw, capsize=cs)
        plt.errorbar(rmi[i]/rvi[i], xi[i,0,:], label=r'$\xi^s_0(s)$', yerr = xiE[i,0,:], color=color[0], fmt = 'o', lw=lw, ms=ms, mew=mew, elinewidth=lw, capsize=cs)
        plt.plot(rs, xips[i], color=color[2], linestyle=line[1], lw=lw)
        plt.plot(rs, xids[i], color=color[1], linestyle=line[2], lw=lw)
        plt.plot(rs, xits[i](*p1[i])[0,:], color=color[0], linestyle=line[0], lw=lw)
        plt.xlabel(r'$s/R$', fontsize=fs)
        plt.ylabel(r'$\xi(s)$', fontsize=fs)
        plt.xlim(0,rmax)
        plt.ylim(-1,0.4)
        plt.yticks(np.linspace(-1,0.4,8))
        plt.figtext(0.6,0.73,r'$\bar{R} = '+'{:>4.1f}'.format(np.round(rvi[i],1))+'h^{-1}\mathrm{Mpc}$')
        plt.figtext(0.6,0.8,r'$\bar{Z} = '+'{:>3.2f}'.format(np.round(zvi[i],2))+'$')
        legend = plt.legend(loc = 4, prop={'size':18}, numpoints=1, markerscale=1.5, fancybox=True, shadow=True)
        legend.get_title().set_fontsize(18)
        plt.savefig(Path(plotPath) / ('xi_p_'+str(i+1)+'.'+figFormat), format=figFormat, bbox_inches="tight")
        plt.clf()


def xi(xi, xiE, xits, rmi, rs, rvi, zvi, p1, chi2, Nvbin=2, rmax=3, ell=[0,], datavec='2d', figFormat='pdf', plotPath='plots/'):
    """Plot multipoles of correlation function with the best-fit model.

    Args:
        xi, xiE (ndarray,[Nvbin,len(ell),Nrbin]): multipoles of void-tracer correlation function and their error
        xits (ndarray,[Nvbin,len(ell),Nspline]): spline of theory model for multipoles of void-tracer correlation function
        rmi (ndarray,[Nvbin,Nrbin]): radial distances from void center for each bin
        rs (ndarray,Nspline): splined radial distances from void center in units of void effective radius
        rvi (ndarray,Nvbin): average effective void radius per bin
        zvi (ndarray,Nvbin): average void redshift per bin
        p1 (ndarray,[Nvbin,Npar]): best-fit model parameter values
        chi2 (ndarray,Nvbin): reduced chi-squared values of best fit
        Nvbin (int): number of void bins (default = 2)
        rmax (float): maximum distance from void center in units of effective void radius (default = 3)
        ell (int list): multipole orders to calculate (default = [0,])
        datavec (str): Define data vector, '1d': multipoles, '2d': POS vs. LOS 2d correlation function (default)
        figFormat (str): format to save figure (default 'pdf')
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        xi_ell.pdf (pdf file): multipoles of correlation function with the best-fit model
    """
    for i in range(Nvbin):
        plt.figure(figsize=figsize)
        plt.plot([1e-4,1e3], [0,0], 'k-', lw=0.5)
        for (l,ll) in enumerate(ell):
            plt.errorbar(rmi[i]/rvi[i], xi[i,l,:], yerr = xiE[i,l,:], label=r'$\ell='+'{:>1n}'.format(ell[l])+'$', color=color[l], fmt = symbol[l], lw=lw, ms=ms, mew=mew, elinewidth=lw, capsize=cs)
            plt.plot(rs, xits[i](*p1[i])[l,:], color=color[l], linestyle=line[l], lw=lw, ms=ms, mew=mew)
        plt.xlabel(r'$s/R$', fontsize=fs)
        plt.ylabel(r'$\xi^s_\ell(s)$', fontsize=fs)
        plt.xlim(0,rmax)
        plt.ylim(-1,0.4)
        plt.yticks(np.linspace(-1,0.4,8))
        plt.figtext(0.6,0.73,r'$\bar{R} = '+'{:>4.1f}'.format(np.round(rvi[i],1))+'h^{-1}\mathrm{Mpc}$')
        plt.figtext(0.6,0.8,r'$\bar{Z} = '+'{:>3.2f}'.format(np.round(zvi[i],2))+'$')
        if (datavec == '1d'): plt.figtext(0.68, 0.4, r'$\chi^2_\mathrm{red} \,=\, '+'{:>3.2f}'.format(np.round(chi2[i],2))+'$')
        legend = plt.legend(loc = 4, prop={'size':18}, numpoints=1, markerscale=1.5, fancybox=True, shadow=True)
        legend.get_title().set_fontsize(18)
        plt.savefig(Path(plotPath) / ('xi_ell_'+str(i+1)+'.'+figFormat), format=figFormat, bbox_inches="tight")
        plt.clf()


def xi_ell(xi, xiE, xits, rmi, rs, rvi, zvi, p1, Nvbin=2, rmax=3, ell=[0,], figFormat='pdf', plotPath='plots/'):
    """Plot multipoles of the same order for all void bins with the best-fit models.

    Args:
        xi, xiE (ndarray,[Nvbin,len(ell),Nrbin]): multipoles of void-tracer correlation function and their error
        xits (ndarray,[Nvbin,len(ell),Nspline]): spline of theory model for multipoles of void-tracer correlation function
        rmi (ndarray,[Nvbin,Nrbin]): radial distances from void center for each bin
        rs (ndarray,Nspline): splined radial distances from void center in units of void effective radius
        rvi (ndarray,Nvbin): average effective void radius per bin
        zvi (ndarray,Nvbin): average void redshift per bin
        p1 (ndarray,[Nvbin,Npar]): best-fit model parameter values
        Nvbin (int): number of void bins (default = 2)
        rmax (float): maximum distance from void center in units of effective void radius (default = 3)
        ell (int list): multipole orders to calculate (default = [0,])
        figFormat (str): format to save figure (default 'pdf')
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        xi_ell=.pdf (pdf file): multipoles of the same order with the best-fit models
    """
    for l in ell:
        plt.figure(figsize=figsize)
        plt.plot([1e-4,1e3], [0,0], 'k-', lw=0.5)
        for i in range(Nvbin):
            label = r'${:>4.1f},\;{:>4.2f}'.format(np.round(rvi[i],1),np.round(zvi[i],2))+'$'
            if l==0:
                plt.errorbar(rmi[i]/rvi[i], xi[i,ell.index(l),:], yerr = xiE[i,ell.index(l),:], fmt = symbol[i], color = color[i], label=label, ms=ms, mew=mew, elinewidth=lw, capsize=cs)
            else:
                plt.errorbar(rmi[i]/rvi[i], xi[i,ell.index(l),:], yerr = xiE[i,ell.index(l),:], fmt = symbol[i], color = color[i], ms=ms, mew=mew, elinewidth=lw, capsize=cs)
            plt.plot(rs, xits[i](*p1[i])[ell.index(l),:], color=color[i], linestyle=line[i], lw=lw, ms=ms, mew=mew)
        plt.xlabel(r'$s/R$', fontsize=fs)
        plt.ylabel(r'$\xi^s_{:>1n}'.format(l)+'(s)$', fontsize=fs)
        plt.xlim(0,rmax)
        if l==0: plt.ylim(-1,0.4)
        else: plt.ylim(-0.2,0.2)
        if l==0:
            legend = plt.legend(loc = 4, title = r'$\bar{R} \, [h^{-1}\mathrm{Mpc}],\; \bar{Z}$ ',prop={'size':18}, numpoints=1, markerscale=1.5, fancybox=True, shadow=True)
            legend.get_title().set_fontsize(fs)
        plt.savefig(Path(plotPath) / ('xi_ell='+str(l)+'.'+figFormat), format=figFormat, bbox_inches="tight")
        plt.clf()


def xi_2d(xi2d, xi2dts, rmi2d, rvi, zvi, p1, chi2, Nvbin=2, Nspline=200, rmax=3, datavec='2d', symLOS=True, figFormat='pdf', plotPath='plots/'):
    """Plot POS vs. LOS 2d correlation function with the best-fit model.

    Args:
        xi2d (ndarray,[Nvbin,Nrbin2d,(2*)Nrbin2d]): POS vs. LOS 2d void-tracer correlation function
        xi2dts (ndarray,[Nvbin,10*Nspline,20*Nspline]): spline of theory model for POS vs. LOS 2d void-tracer correlation function
        rmi2d (ndarray,[Nvbin,(2*)Nrbin2d]): POS and LOS distances from void center for each bin
        rvi (ndarray,Nvbin): average effective void radius per bin
        zvi (ndarray,Nvbin): average void redshift per bin
        p1 (ndarray,[Nvbin,Npar]): best-fit model parameter values
        chi2 (ndarray,Nvbin): reduced chi-squared values of best fit
        Nvbin (int): number of void bins (default = 2)
        Nspline (int): number of nodes for spline if Nsmooth > 0 (default = 200)
        rmax (float): maximum distance from void center in units of effective void radius (default = 3)
        datavec (str): Define data vector, '1d': multipoles, '2d': POS vs. LOS 2d correlation function (default)
        symLOS (bool): if True, assume symmetry along LOS (default)
        figFormat (str): format to save figure (default 'pdf')
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        xi_2d.pdf (pdf file): POS vs. LOS 2d correlation function with the best-fit model
    """
    for i in range(Nvbin):
        plt.figure(figsize=figsize)
        plt.axes().set_aspect('equal')
        rpar = np.linspace(-rmax,rmax,2*10*Nspline) # for 2d splines (more nodes required)
        rper = rpar[rpar > 0.]
        if symLOS: # symmetrize along LOS
            rmi = np.hstack((-rmi2d[i,::-1],rmi2d[i]))
            xi = np.hstack((xi2d[i,:,::-1],xi2d[i]))
            xi = np.vstack((xi[::-1,:],xi))
        else:
            rmi = rmi2d[i]
            xi = np.vstack((xi2d[i,::-1,:],xi2d[i]))
        plt.pcolormesh(rmi/rvi[i], rmi/rvi[i], xi.T, cmap=plt.get_cmap('Spectral_r'), vmin=vmin, vmax=vmax, shading='gouraud')
        cbar = plt.colorbar(pad=0.03, format='%+.1f')
        cbar.solids.set_edgecolor("face")
        signal = plt.contour(rmi/rvi[i], rmi/rvi[i], xi.T, lev, vmin=vmin, vmax=vmax, colors='k', linewidths=0.3)
        plt.clabel(signal, fontsize=6, fmt='%1.1f')
        model = plt.contour(rper, rpar, xi2dts[i](*p1[i]).T, lev, vmin=vmin, vmax=vmax, colors='w', linewidths=1, alpha=0.9)
        plt.contour(-rper, rpar[::-1], xi2dts[i](*p1[i]).T, lev, vmin=vmin, vmax=vmax, colors='w', linewidths=1, alpha=0.9)
        plt.clabel(model, fontsize=6, fmt='%1.1f')
        plt.xlabel(r'$s_\perp/R$', fontsize=fs)
        plt.ylabel(r'$s_\parallel/R$', fontsize=fs)
        xymax = np.floor(rmax/np.sqrt(2))
        plt.xlim(np.array([-1,1])*xymax)
        plt.ylim(np.array([-1,1])*xymax)
        plt.xticks(np.arange(-xymax, xymax+1, step=1))
        plt.yticks(np.arange(-xymax, xymax+1, step=1))
        if (datavec == '2d'): plt.figtext(0.55, 0.13, r'$\chi^2_\mathrm{red} \,=\, '+'{:>3.2f}'.format(np.round(chi2[i],2))+'$')
        plt.savefig(Path(plotPath) / ('xi_2d_'+str(i+1)+'.'+figFormat), format=figFormat, bbox_inches="tight")
        plt.clf()


def xi_cov(xiC, dim=1, Nvbin=2, ell=[0,], symLOS=True, figFormat='pdf', plotPath='plots/'):
    """Plot normalized covariance matrix of correlation function.

    Args:
        xiC (ndarray,[Nvbin,*,*]): covariance of (either 1d or 2d) correlation function
        dim (int): dimension of data vector [1: multipoles (default), 2: POS vs. LOS]
        Nvbin (int): number of void bins (default = 2)
        ell (int list): multipole orders to calculate (default = [0,])
        symLOS (bool): if True, assume symmetry along LOS (default)
        figFormat (str): format to save figure (default 'pdf')
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        cov_ell.pdf (pdf file): covariance of multipoles (if dim=1) \n
        cov_2d.pdf (pdf file): covariance of POS vs. LOS 2d correlation function (if dim=2)
    """
    for i in range(Nvbin):
        plt.figure(figsize=figsize)
        plt.axes().set_aspect('equal')
        coords = np.meshgrid(np.arange(len(xiC[i])),np.arange(len(xiC[i])))[0]/float(len(xiC[i]))
        matrix = xiC[i]/np.sqrt(np.outer(xiC[i].diagonal(), xiC[i].diagonal()))
        pcol = plt.pcolor(coords[0], coords[1], matrix, cmap=plt.get_cmap('Spectral_r'), rasterized=True, shading='auto') #, vmin=-1, vmax=1)
        pcol.set_edgecolor("face")
        cbar = plt.colorbar(pad=0.03, format='%.1f')
        cbar.solids.set_edgecolor("face")
        if dim==1:
            plt.xlabel(r'$\ell$', fontsize=fs)
            plt.ylabel(r'$\ell$', fontsize=fs)
            plt.xticks(np.linspace(1, max(ell)+1, len(ell))/len(ell)/2, ell)
            plt.yticks(np.linspace(1, max(ell)+1, len(ell))/len(ell)/2, ell)
            plt.savefig(Path(plotPath) / ('cov_ell_'+str(i+1)+'.'+figFormat), format=figFormat, dpi=300, bbox_inches="tight")
        if dim==2:
            plt.xlabel(r'$i$', fontsize=fs)
            plt.ylabel(r'$j$', fontsize=fs)
            Nbin = np.sqrt(len(xiC[i])) if symLOS else np.sqrt(len(xiC[i])/2) # symmetry along LOS
            plt.xticks(np.arange(1,Nbin+1)/(Nbin), np.arange(1,Nbin+1).astype(int), fontsize=8)
            plt.yticks(np.arange(1,Nbin+1)/(Nbin), np.arange(1,Nbin+1).astype(int), fontsize=8)
            plt.savefig(Path(plotPath) / ('cov_2d_'+str(i+1)+'.'+figFormat), format=figFormat, dpi=300, bbox_inches="tight")
        plt.clf()


def fs8_DAH(zvi, zmin, zmax, fs8, fs8e, DAH, DAHe, legend, par_cosmo, Nspline=200, figFormat='pdf', plotPath='plots/'):
    """Plot measurements of f*sigma_8 and D_A*H/c against redshift.

    Args:
        zvi (ndarray,Nvbin): average void redshift per bin
        zmin (float): minimum redshift
        zmax (float): maximum redshift
        fs8, fs8e (ndarray list,[len(fs8),Nvbin]): measured values and uncertainties of f*sigma_8
        DAH, DAHe (ndarray list,[len(DAH),Nvbin]): measured values and uncertainties of D_A*H/c
        legend (str list): legend labels for different measurements
        par_cosmo (dict): cosmological parameter values
        Nspline (int): number of nodes for spline if Nsmooth > 0 (default = 200)
        figFormat (str): format to save figure (default 'pdf')
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        fs8_DAH.pdf (pdf file): measurements of f*sigma_8 and D_A*H/c and fiducial cosmological model prediction
    """
    z = np.linspace(0.,3.,Nspline)
    fs8_fid = datalib.fz(z,par_cosmo)*datalib.Dz(z,par_cosmo)*par_cosmo['s8']
    DAH_fid = datalib.DA(z,par_cosmo)/datalib.DH(z,par_cosmo)
    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(8.,4.5))
    fig.subplots_adjust(hspace=0)
    axs[0].tick_params(axis='both', which='major', labelsize=12)
    for i in range(len(fs8)):
        axs[0].errorbar(zvi+int(i/2+1)*0.005*(-1)**(i+1), fs8[i], yerr = fs8e[i], mfc=color[i], mec='k', ecolor='k', fmt=symbol[i], ms=1.3*ms, mew=2*mew, elinewidth=1, capsize=1.5*cs)
    axs[0].plot(z, fs8_fid, color='k', linestyle=line[2], lw=lw, alpha=0.6)
    axs[0].set_ylabel(r'$f\sigma_8$', fontsize=12)
    axs[0].set_xlim(zmin,zmax)
    axs[0].set_ylim(0.25,0.6)
    axs[1].tick_params(axis='both', which='major', labelsize=12)
    for i in range(len(DAH)):
        axs[1].errorbar(zvi+int(i/2+1)*0.005*(-1)**(i+1), DAH[i], yerr = DAHe[i], label=legend[i], mfc=color[i], mec='k', ecolor='k', fmt=symbol[i], ms=1.3*ms, mew=2*mew, elinewidth=1, capsize=1.5*cs)
    axs[1].plot(z, DAH_fid, color='k', linestyle=line[2], lw=lw, alpha=0.6)
    axs[1].set_xlabel(r'$z$', fontsize=12)
    axs[1].set_ylabel(r'$D_\mathrm{A}H/c$', fontsize=12)
    axs[1].set_xlim(zmin,zmax)
    axs[1].set_ylim(1.0,1.85)
    legend = axs[1].legend(loc=4, prop={'size':14}, numpoints=1, markerscale=1.5, fancybox=True, shadow=True)
    legend.get_title().set_fontsize(fs)
    plt.savefig(Path(plotPath) / ('fs8_DAH.'+figFormat), format=figFormat, bbox_inches="tight")
    plt.clf()


def triangle(samples, p0, p1, rvi, zvi, pLim, pop, par, Nvbin=2, vbin='zv', legend=None, title=None, figFormat='pdf', plotPath='plots/'):
    """Make triangle plot of MCMC posterior.

    Args:
        samples (ndarray list,[len(samples),Nvbin,Nchain,Npar]): list of MCMC samples after thinning and burn-in removal
        p0 (ndarray list,[len(samples),Nvbin,Npar]): fiducial model parameter values
        p1 (ndarray list,[len(samples),Nvbin,Npar]): best-fit model parameter values
        rvi (ndarray,Nvbin): average effective void radius per bin
        zvi (ndarray,Nvbin): average void redshift per bin
        pLim (ndarray list,[len(samples),Nvbin,Npar,2]): limits for parameter margins around their mean value
        pop (str list,[len(samples),len(pop)]): parameters to exclude from plot, for no exclusion use None
        par (dict): model parameter values
        Nvbin (int): number of void bins (default = 2)
        vbin (str): binning strategy, 'zv': void-redshift bins (default), 'rv': void-radius bins
        legend (str list,len(samples)): legend labels for different samples (default = None)
        title (str): plot title (default = None)
        figFormat (str): format to save figure (default 'pdf')
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        triangle.pdf (pdf file): triangle plot of posterior parameter distribution
    """
    name = list(par.keys()) # parameter names
    label = [r'f/b', r'q_\perp/q_\parallel', r'q_\parallel', r'\mathcal{M}', r'\mathcal{Q}'] # parameter labels
    for i in range(Nvbin):
        pops = []
        if pop is not None:
            for p in pop: pops.append(list(par.keys()).index(p))
        sample = []
        for s in samples:
            si = np.copy(s[i])
            si[:,1] /= si[:,2] # AP parameter epsilon
            sample.append(np.delete(si,pops,1))
        pfid = np.delete(p0[i],pops)
        pfid[-2:] = None  # Remove fiducial lines for M,Q
        pfit = np.copy(p1)
        pfit[i,1] /= pfit[i,2] # AP parameter epsilon
        pfit = np.delete(pfit[i],pops)
        plim = np.delete(pLim[i],pops,axis=0)
        names = np.delete(name,pops)
        labels = np.delete(label,pops)
        pSample = []
        if len(samples) > 1:
            for s in sample: pSample.append(getdist.MCSamples(samples=s, names=names, labels=labels, ignore_rows=0))
        else: pSample.append(getdist.MCSamples(samples=sample, names=names, labels=labels, ignore_rows=0))
        gd = getdist.plots.get_subplot_plotter()
        gd.settings.axes_fontsize = fs
        gd.settings.lab_fontsize = fs
        gd.settings.legend_fontsize = fs
        gd.settings.alpha_filled_add=0.8
        gd.settings.title_limit_labels = None
        gd.settings.title_limit_fontsize = 18
        gd.triangle_plot(pSample, names,
            filled_compare=True,
            legend_labels=legend,
            legend_loc='upper right',
            line_args=[{'lw':2, 'color':color[0]}, {'lw':2, 'color':color[1]}, {'lw':2, 'color':color[2]}, {'lw':2, 'color':color[3]}],
            contour_colors=color,
            title_limit=1)
        fig = gd.fig
        if title is not None: fig.text(0.58, 0.9, title)
        if vbin == 'rv': fig.text(0.6, 0.8, r'$\bar{R} = '+'{:>4.1f}'.format(np.round(rvi[i],1))+'h^{-1}\mathrm{Mpc}$', fontsize=24)
        if vbin == 'zv': fig.text(0.6, 0.8, r'$\bar{Z} = '+'{:>3.2f}'.format(np.round(zvi[i],2))+'$', fontsize=22)
        for k in range(len(pfid)):
            for (j,ax) in enumerate(gd.subplots[:,k]):
                if ax: ax.axvline(pfid[k], color='gray', ls='--')
                if (j>k):
                    ax.axhline(pfid[j], color='gray', ls='--')
                    ax.plot(pfit[k], pfit[j], 'x', color='w', ms=ms)
                    ax.set_xlim(plim[k])
                    ax.set_ylim(plim[j])
                #if (j==k): ax.set_title('$'+pSample[0].getInlineLatex(names[j],limit=1,err_sig_figs=2)+'$',fontsize=10)
        gd.export(str(Path(plotPath) / ('triangle_'+str(i+1)+'.'+figFormat)))


def triangle_cosmo(samples, logP, pLim, cosmology, par_cosmo, blind=True, legend=None, figFormat='pdf', plotPath='plots/'):
    """Make triangle plot of MCMC posterior for cosmological parameters.

    Args:
        samples (ndarray list,[len(samples),Nchain,Npar]): list of MCMC samples after thinning and burn-in removal
        logP (ndarray,Nchain): log likelihood values of first sample
        pLim (ndarray list,[len(samples),Npar,2]): limits for parameter margins around their mean value
        cosmology (str): cosmological model to consider [either 'LCDM', 'wCDM', or 'w0waCDM']
        par_cosmo (dict): cosmological parameter values
        blind (bool): If true, subtract mean from chains (default = True)
        legend (str list,len(samples)): legend labels for different samples (default = None)
        figFormat (str): format to save figure (default 'pdf')
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        triangle_cosmology.pdf (pdf file): triangle plot of posterior cosmological parameter distribution
    """
    if cosmology == 'LCDM':
        p0 = [par_cosmo['Om']]
        names = ['Om']
        labels = [r'\Omega_\mathrm{m}']
        title = r'Flat $\Lambda\mathrm{CDM}$'
    if cosmology == 'wCDM':
        p0 = [par_cosmo['Om'],par_cosmo['w0']]
        names = ['Om','w0']
        labels = [r'\Omega_\mathrm{m}',r'w']
        title = r'Flat $w\mathrm{CDM}$'
    if cosmology == 'w0waCDM':
        p0 = [par_cosmo['Om'],par_cosmo['w0'],par_cosmo['wa']]
        names = ['Om','w0','wa']
        labels = [r'\Omega_\mathrm{m}',r'w_0',r'w_a']
        title = r'Flat $w_0w_a\mathrm{CDM}$'

    p1 = samples[0][np.argmax(logP)]
    pSample = []
    if len(samples) > 1:
        for s in samples: pSample.append(getdist.MCSamples(samples=s, names=names, labels=labels, ignore_rows=0))
    else: pSample.append(getdist.MCSamples(samples=samples, names=names, labels=labels, ignore_rows=0))
    gd = getdist.plots.get_subplot_plotter() # subplot_size_ratio=1.2
    gd.settings.axes_fontsize = 14
    gd.settings.lab_fontsize = 14
    gd.settings.legend_fontsize = 10
    gd.settings.alpha_filled_add= 0.6
    gd.settings.title_limit_labels = None
    gd.settings.title_limit_fontsize = 14
    gd.triangle_plot(pSample, names,
        filled_compare=True,
        legend_labels=legend,
        legend_loc='upper right',
        line_args=[{'lw':1, 'color':color[0], 'ls':line[0]}, {'lw':1, 'color':color[1], 'ls':line[1]}, {'lw':1, 'color':color[2], 'ls':line[2]}, {'lw':1, 'color':color[3], 'ls':line[3]}, {'lw':1, 'color':color[4], 'ls':line[4]}],
        contour_colors=color,
        title_limit=None)
    fig = gd.fig
    #if title is not None: fig.text(0.64, 0.96, title, fontsize=12)
    #fig.text(0.89,0.17,r'$\mathrm{Author~et~al.~2021}$', fontsize=9,rotation=90, rotation_mode='anchor',color='grey')
    for k in range(len(p0)):
        for (j,ax) in enumerate(gd.subplots[:,k]):
            if ax:
                ax.set_xlim(pLim[j])
                if blind == False: ax.axvline(p0[k], color='gray', ls='--')
            if (j>k):
                if blind == False: ax.axhline(p0[j], color='gray', ls='--')
                ax.plot(p1[k], p1[j], 'x', color='w', ms=ms)
                ax.set_xlim(pLim[k])
                ax.set_ylim(pLim[j])
            if (j==k): ax.set_title('$'+pSample[0].getInlineLatex(names[j],limit=1,err_sig_figs=2)+'$',fontsize=12)

    gd.export(str(Path(plotPath) / ('triangle_'+cosmology+'.'+figFormat)))


def logo(xi2dts, p1, Nvbin=2, Nspline=200, rmax=3., vmin=-0.8, vmax=0.4, Nlev=10, cmap='Spectral_r', plotPath='plots/'):
    """Plot Voiager logo background.

    Args:
        xi2dts (ndarray,[Nvbin,10*Nspline,20*Nspline]): spline of theory model for POS vs. LOS 2d void-tracer correlation function
        p1 (ndarray,[Nvbin,Npar]): best-fit model parameter values
        Nvbin (int): number of void bins (default = 2)
        Nspline (int): number of nodes for spline if Nsmooth > 0 (default = 200)
        rmax (float): maximum distance from void center in units of effective void radius (default = 3)
        vmin, vmax (float): minimum and maximum for contour map (default = -0.8, 0.4)
        Nlev (int): number of contour lines (default = 10)
        cmap (str): colormap from matplotlib (default = 'Spectral_r'), see https://matplotlib.org/stable/tutorials/colors/colormaps.html
        plotPath (path): name of output path for plot (default = 'plots/')

    Returns:
        logo.png (image file): Voiager logo background
    """
    levels = np.linspace(vmin,vmax,Nlev) + 0.03 # contour values
    for i in range(Nvbin):
        plt.figure(figsize=figsize)
        plt.axes().set_aspect('equal')
        rpar = np.linspace(-rmax,rmax,2*10*Nspline) # for 2d splines (more nodes required)
        rper = rpar[rpar > 0.]
        plt.pcolormesh(rper, rpar, xi2dts[i](*p1[i]).T, cmap=plt.get_cmap(cmap), vmin=vmin, vmax=vmax, shading='auto')
        plt.pcolormesh(-rper, rpar[::-1], xi2dts[i](*p1[i]).T, cmap=plt.get_cmap(cmap), vmin=vmin, vmax=vmax, shading='auto')
        plt.contour(rper, rpar, xi2dts[i](*p1[i]).T, levels, vmin=vmin, vmax=vmax, colors='k', linewidths=0.5, alpha=0.5)
        plt.contour(-rper, rpar[::-1], xi2dts[i](*p1[i]).T, levels, vmin=vmin, vmax=vmax, colors='k', linewidths=0.5, alpha=0.5)
        xymax = np.floor(rmax/np.sqrt(2))
        plt.xlim(np.array([-1,1])*xymax)
        plt.ylim(np.array([-1,1])*xymax)
        plt.xticks([])
        plt.yticks([])
        plt.savefig(Path(plotPath) / ('logo_'+str(i+1)+'.png'), format='png', bbox_inches="tight", dpi=800)
        plt.clf()
