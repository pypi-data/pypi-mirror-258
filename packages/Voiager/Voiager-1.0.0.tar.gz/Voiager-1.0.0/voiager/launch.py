import os
import gc
import pickle
import getdist
import numpy as np
from voiager import datalib
from voiager import plotlib


def launch(vger):
    """
    Launcher of Voiager.

    Args:
        vger (object): instance of Voiager class
    """

    print('Loading data (angles, redshifts, catalog sizes, void properties)...')
    Ngc, Nvc, Xg, Xgr, Xv, rv, tv, dv, cv, mv, vv, Cv, ev, eval, evec, mgs = datalib.loadData(vger, vger.tracerPath, vger.voidPath, vger.survey, vger.sample, vger.random, vger.inputFormat, vger.inputExtension, vger.version, vger.columnNames, vger.Nmock)


    print('Generating void randoms...')
    Xvr, rvr = datalib.makeRandom(Xv, len(Xgr)/float(len(Xg)), vger.Nside, vger.Nbin_nz, rv)
    #np.savetxt(vger.outPath / 'randomVoids.txt', np.vstack((Xvr.T,rvr)).T, fmt='%.6e', header='RA [rad],  DEC [rad],   Z,           R [Mpc/h]')

    # Weights for galaxies and randoms (optional)
    wg = wr = None 

    # Size of catalogs
    Ng, Ngr, Nv, Nvr = len(Xg), len(Xgr), len(Xv), len(Xvr)

    # Define redshift arrays
    zv, zvr = Xv[:,2], Xvr[:,2]

    # Number densities as function of redshift
    zgm,  ngm  = datalib.numberDensity(Xg[:,2],  vger.Nbin_nz, vger.sky, vger.par_cosmo, vger.Nmock)
    zgrm, ngrm = datalib.numberDensity(Xgr[:,2], vger.Nbin_nz, vger.sky, vger.par_cosmo)
    zvm,  nvm  = datalib.numberDensity(Xv[:,2],  vger.Nbin_nz, vger.sky, vger.par_cosmo, vger.Nmock)
    zvrm, nvrm = datalib.numberDensity(Xvr[:,2], vger.Nbin_nz, vger.sky, vger.par_cosmo)


    print('Transforming coordinates...')
    xg  = datalib.coordTrans(Xg, vger.par_cosmo, vger.Ncpu)
    xgr = datalib.coordTrans(Xgr, vger.par_cosmo, vger.Ncpu)
    xv  = datalib.coordTrans(Xv, vger.par_cosmo,  vger.Ncpu)
    xvr = datalib.coordTrans(Xvr, vger.par_cosmo, vger.Ncpu)

    # Free up memory
    del Xg,Xgr; gc.collect()


    print('Building stacks...')
    if os.path.exists(vger.outPath / vger.stackFile): # Load existing stacks
        if vger.continueStack:
            print('=> Loading previous stack')
            Nvi, rvi, zvi, rmi, rmi2d, xip, xipE, xi, xiE, xiC, xiCI, xi2d, xi2dC, xi2dCI  = pickle.load(open(vger.outPath / vger.stackFile,"rb"))
        else:
            print('=> Deleting previous stack'); os.remove(vger.outPath / vger.stackFile)
    if not os.path.exists(vger.outPath / vger.stackFile) or not vger.continueStack:
        if not vger.project2d: # LOS-projected correlations
            DDp  = datalib.getStack(xv,  xg,  rv,  zv,  Nvc, Ngc, ngm,  zgm,  wg, vger.rmax, vger.Nrbin, vger.ell, vger.symLOS, 0, vger.Nmock, vger.Ncpu) # Void-Galaxy
            DRp  = datalib.getStack(xv,  xgr, rv,  zv,  Nvc, Ngc, ngrm, zgrm, wr, vger.rmax, vger.Nrbin, vger.ell, vger.symLOS, 0, False, vger.Ncpu)        # Void-RandomGalaxy
            RDp  = datalib.getStack(xvr, xg,  rvr, zvr, Nvc, Ngc, ngm,  zgm,  wg, vger.rmax, vger.Nrbin, vger.ell, vger.symLOS, 0, False, vger.Ncpu)        # RandomVoid-Galaxy
            RRp  = datalib.getStack(xvr, xgr, rvr, zvr, Nvc, Ngc, ngrm, zgrm, wr, vger.rmax, vger.Nrbin, vger.ell, vger.symLOS, 0, False, vger.Ncpu)        # RandomVoid-RandomGalaxy
        # Mulipoles of correlations
        DD   = datalib.getStack(xv,  xg,  rv,  zv,  Nvc, Ngc, ngm,  zgm,  wg, vger.rmax, vger.Nrbin, vger.ell, vger.symLOS, 1, vger.Nmock, vger.Ncpu) # Void-Galaxy
        DR   = datalib.getStack(xv,  xgr, rv,  zv,  Nvc, Ngc, ngrm, zgrm, wr, vger.rmax, vger.Nrbin, vger.ell, vger.symLOS, 1, False, vger.Ncpu)        # Void-RandomGalaxy
        RD   = datalib.getStack(xvr, xg,  rvr, zvr, Nvc, Ngc, ngm,  zgm,  wg, vger.rmax, vger.Nrbin, vger.ell, vger.symLOS, 1, False, vger.Ncpu)        # RandomVoid-Galaxy
        RR   = datalib.getStack(xvr, xgr, rvr, zvr, Nvc, Ngc, ngrm, zgrm, wr, vger.rmax, vger.Nrbin, vger.ell, vger.symLOS, 1, False, vger.Ncpu)        # RandomVoid-RandomGalaxy
        # POS vs. LOS 2d correlations
        DD2d = datalib.getStack(xv,  xg,  rv,  zv,  Nvc, Ngc, ngm,  zgm,  wg, vger.rmax, vger.Nrbin, vger.ell, vger.symLOS, 2, vger.Nmock, vger.Ncpu) # Void-Galaxy
        DR2d = datalib.getStack(xv,  xgr, rv,  zv,  Nvc, Ngc, ngrm, zgrm, wr, vger.rmax, vger.Nrbin, vger.ell, vger.symLOS, 2, False, vger.Ncpu)        # Void-RandomGalaxy
        RD2d = datalib.getStack(xvr, xg,  rvr, zvr, Nvc, Ngc, ngm,  zgm,  wg, vger.rmax, vger.Nrbin, vger.ell, vger.symLOS, 2, False, vger.Ncpu)        # RandomVoid-Galaxy
        RR2d = datalib.getStack(xvr, xgr, rvr, zvr, Nvc, Ngc, ngrm, zgrm, wr, vger.rmax, vger.Nrbin, vger.ell, vger.symLOS, 2, False, vger.Ncpu)        # RandomVoid-RandomGalaxy

        # Get data vectors and covariances
        if not vger.project2d:
            Nvi, rvi, zvi, rmi, rmi2d, xip, xipE, xi, xiE, xiC, xiCI, xi2d, xi2dC, xi2dCI = datalib.getData(DDp, DRp, RDp, RRp, DD, DR, RD, RR, DD2d, DR2d, RD2d, RR2d, rv, rvr, zv, zvr, vger.par, vger.par_cosmo, vger.vbin, vger.binning, vger.Nvbin, vger.Nrbin, vger.rmax, vger.ell, vger.symLOS, vger.project2d, vger.rescov, vger.Ncpu)
        else:
            Nvi, rvi, zvi, rmi, rmi2d, xip, xipE, xi, xiE, xiC, xiCI, xi2d, xi2dC, xi2dCI = datalib.getData(DD, DR, RD, RR, DD, DR, RD, RR, DD2d, DR2d, RD2d, RR2d, rv, rvr, zv, zvr, vger.par, vger.par_cosmo, vger.vbin, vger.binning, vger.Nvbin, vger.Nrbin, vger.rmax, vger.ell, vger.symLOS, vger.project2d, vger.rescov, vger.Ncpu)
        # Save stacks
        pickle.dump((Nvi, rvi, zvi, rmi, rmi2d, xip, xipE, xi, xiE, xiC, xiCI, xi2d, xi2dC, xi2dCI), open(vger.outPath / vger.stackFile,"wb"))


    # Define theory model
    rs, xips, xid, xids, Xid, Xids, xit, xits, xi2dt, xi2dts = datalib.getModel(rmi, rmi2d, rvi, xip, xipE, vger.rmax, vger.ell, vger.Nsmooth, vger.Nspline, weight=None)


    print('Finding best fit...')
    if vger.datavec=='1d': p0, p1, chi2 = datalib.bestFit(vger.par, vger.prior, vger.par_cosmo, zvi, xit, xi, xiC, xiCI, vger.ell, vger.datavec, vger.Nrskip, vger.symLOS, vger.Nmock)
    if vger.datavec=='2d': p0, p1, chi2 = datalib.bestFit(vger.par, vger.prior, vger.par_cosmo, zvi, xi2dt, xi2d, xi2dC, xi2dCI, vger.ell, vger.datavec, vger.Nrskip, vger.symLOS, vger.Nmock)
    print('=> Parameters: ',list(vger.par.keys()),'\n',p1,'\n qper/qpar: \n',p1[:,1]/p1[:,2],'\n Reduced chi-square: \n',chi2)


    print('MCMC sampling...')
    if os.path.exists(vger.outPath / vger.chainFile):
        if vger.continueChain:
            print('=> Continuing from previous chain')
        else: print('=> Deleting previous chain'); os.remove(vger.outPath / vger.chainFile)
    if vger.datavec=='1d': sampler = datalib.runMCMC(p1, vger.par, vger.prior, xit, xi, xiC, xiCI, vger.vbin, vger.ell, vger.datavec, vger.Nrskip, vger.symLOS, vger.Nmock, vger.Nwalk, vger.Nchain, vger.chainFile, vger.outPath)
    if vger.datavec=='2d': sampler = datalib.runMCMC(p1, vger.par, vger.prior, xi2dt, xi2d, xi2dC, xi2dCI, vger.vbin, vger.ell, vger.datavec, vger.Nrskip, vger.symLOS, vger.Nmock, vger.Nwalk, vger.Nchain, vger.chainFile, vger.outPath)


    # Load chains
    samples, logP, pMean, pStd, pErr, pLim = datalib.loadMCMC(vger.chainFile, vger.Nburn, vger.Nthin, vger.Nmarg, vger.Nvbin, vger.vbin, vger.outPath)


    # Measured and derived observables with fiducial reference values
    f_b_fid = datalib.f_b_z(zvi,vger.par_cosmo)
    f_b_fit = np.array(pMean)[:,0]
    f_b_err = np.array(pStd)[:,0]

    fs8_fid = datalib.fz(zvi,vger.par_cosmo)*datalib.Dz(zvi,vger.par_cosmo)*vger.par_cosmo['s8']
    fs8_fit = f_b_fit*datalib.bz(zvi,vger.par_cosmo)*datalib.Dz(zvi,vger.par_cosmo)*vger.par_cosmo['s8']
    fs8_err = f_b_err*datalib.bz(zvi,vger.par_cosmo)*datalib.Dz(zvi,vger.par_cosmo)*vger.par_cosmo['s8']

    DA_fid = datalib.DA(zvi,vger.par_cosmo)
    DA_fit = np.array(pMean)[:,1]*DA_fid
    DA_err = np.array(pStd)[:,1]*DA_fid

    DH_fid = datalib.DH(zvi,vger.par_cosmo)
    DH_fit = np.array(pMean)[:,2]*DH_fid
    DH_err = np.array(pStd)[:,2]*DH_fid

    eps, eps_fit, eps_err = [], np.zeros(vger.Nvbin), np.zeros(vger.Nvbin)
    for i in range(vger.Nvbin):
        eps.append(np.array(samples[i])[:,1]/np.array(samples[i])[:,2])
        eps_fit[i] = np.mean(eps[i])
        eps_err[i] = np.std(eps[i])

    eps_lim = np.array(list(zip(eps_fit-vger.Nmarg*eps_err,eps_fit+vger.Nmarg*eps_err)))
    for i in range(vger.Nvbin): pLim[i][1] = eps_lim[i] # AP parameter epsilon

    DAH_fid = DA_fid/DH_fid
    DAH_fit = eps_fit*DAH_fid
    DAH_err = eps_err*DAH_fid


    # Output strings in latex format
    out_tex = []
    for i in range(vger.Nvbin):
        f_b_fit_str = r'$$'+'{:6.4f}\pm{:6.4f}'.format(f_b_fit[i],f_b_err[i])+'$$'
        fs8_fit_str = r'$$'+'{:6.4f}\pm{:6.4f}'.format(fs8_fit[i],fs8_err[i])+'$$'
        eps_fit_str = r'$$'+'{:6.4f}\pm{:6.4f}'.format(eps_fit[i],eps_err[i])+'$$'
        DAH_fit_str = r'$$'+'{:6.4f}\pm{:6.4f}'.format(DAH_fit[i],DAH_err[i])+'$$'
        out_tex.append(f_b_fit_str+' & '+fs8_fit_str+' & '+eps_fit_str+' & '+DAH_fit_str)

    # Gather different measurements (only for illustration)
    tags = ['VGCF']
    fs8f, fs8e, DAHf, DAHe = [],[],[],[]

    fs8f.append(fs8_fit)
    fs8e.append(fs8_err)
    DAHf.append(DAH_fit)
    DAHe.append(DAH_err)



    print('Constraining cosmology...')
    if os.path.exists(vger.outPath / vger.cosmoFile):
        if vger.continueChain:
            print('=> Continuing from previous chain')
        else: print('=> Deleting previous chain'); os.remove(vger.outPath / vger.cosmoFile)
    sampler_cosmo = datalib.runMCMC_cosmo(zvi, vger.par_cosmo, vger.prior_cosmo, DAH_fit, DAH_err, vger.Nwalk, vger.Nchain, vger.cosmoFile, vger.cosmology, vger.outPath)
    #sampler_cosmo = datalib.runMCMC_cosmo2(zvi, vger.par_cosmo, vger.prior_cosmo, DA_fit, DA_err, DH_fit, DH_err, vger.Nwalk, vger.Nchain, vger.cosmoFile, vger.cosmology, vger.outPath)

    # Load cosmology chains:
    samples_cosmo, logP_cosmo, pBest_cosmo, pMean_cosmo, pStd_cosmo, pErr_cosmo, pLim_cosmo = datalib.loadMCMC_cosmo(vger.cosmoFile, vger.cosmology, vger.Nburn, vger.Nthin, vger.Nmarg, vger.blind, vger.outPath)

    cosmo = []
    cosmo.append(samples_cosmo)


    # Save chains as text file:
    Nsig = 1 # Number of sigmas for confidence intervals
    Ndig = 4 # Number of significant digits in headline results for MEAN and MAP (best fit)
    header = 'Posterior for Beyond-2pt challenge with void-galaxy cross-correlation analysis of the wCDM light-cone \n\n'
    for i,chain in enumerate(cosmo):
        if vger.cosmology=='LCDM':
            results  = getdist.MCSamples(samples=chain,names=['Om']).getInlineLatex('Om',limit=Nsig,err_sig_figs=Ndig)+' (MEAN), '+str(np.round(pBest_cosmo[0],Ndig))+' (MAP) \n'
        if vger.cosmology=='wCDM':
            results  = getdist.MCSamples(samples=chain,names=['Om','w0']).getInlineLatex('Om',limit=Nsig,err_sig_figs=Ndig)+' (MEAN), '+str(np.round(pBest_cosmo[0],Ndig))+' (MAP) \n'
            results += getdist.MCSamples(samples=chain,names=['Om','w0']).getInlineLatex('w0',limit=Nsig,err_sig_figs=Ndig)+' (MEAN), '+str(np.round(pBest_cosmo[1],Ndig))+' (MAP) \n'
        if vger.cosmology=='w0waCDM':
            results  = getdist.MCSamples(samples=chain,names=['Om','w0','wa']).getInlineLatex('Om',limit=Nsig,err_sig_figs=Ndig)+' (MEAN), '+str(np.round(pBest_cosmo[0],Ndig))+' (MAP) \n'
            results += getdist.MCSamples(samples=chain,names=['Om','w0','wa']).getInlineLatex('w0',limit=Nsig,err_sig_figs=Ndig)+' (MEAN), '+str(np.round(pBest_cosmo[1],Ndig))+' (MAP) \n'
            results += getdist.MCSamples(samples=chain,names=['Om','w0','wa']).getInlineLatex('wa',limit=Nsig,err_sig_figs=Ndig)+' (MEAN), '+str(np.round(pBest_cosmo[2],Ndig))+' (MAP) \n'
        np.savetxt(vger.outPath / ('chains_'+vger.cosmology+'_'+str(i+1)+'.txt'), chain, fmt='%12.8f', header=header+results)



    print('Plotting...')
    # Void sample properties
    plotlib.voidSky(Xv, Xvr, vger.plotPath)
    plotlib.voidBox(xv, zv, 45., -120., vger.plotPath)
    plotlib.voidRedshift(rv, zv, rvr, zvr, vger.plotPath)
    plotlib.voidAbundance(cv, vger.Nbin_nv, vger.zmin, vger.zmax, vger.sky, vger.par_cosmo, r'c_\mathrm{v}', '', 'density-contrast', [1e-10,1e-5], None, vger.Nmock, vger.figFormat, vger.plotPath)
    plotlib.voidAbundance(dv, vger.Nbin_nv, vger.zmin, vger.zmax, vger.sky, vger.par_cosmo, r'n_\mathrm{c}', r'[\bar{n}]', 'core-density', [1e-10,1e-5], None, vger.Nmock, vger.figFormat, vger.plotPath)
    plotlib.voidAbundance(ev, vger.Nbin_nv, vger.zmin, vger.zmax, vger.sky, vger.par_cosmo, r'e_\mathrm{v}', '', 'ellipticity', [1e-10,1e-5], None, vger.Nmock, vger.figFormat, vger.plotPath)
    plotlib.voidAbundance(mv, vger.Nbin_nv, vger.zmin, vger.zmax, vger.sky, vger.par_cosmo, r'm_\mathrm{v}', '', 'richness', [1e-10,1e-5], None, vger.Nmock, vger.figFormat, vger.plotPath)
    plotlib.voidAbundance(Cv, vger.Nbin_nv, vger.zmin, vger.zmax, vger.sky, vger.par_cosmo, r'\Delta_\mathrm{v}', r'[\bar{n}]', 'compensation', [1e-10,1e-5], None, vger.Nmock, vger.figFormat, vger.plotPath)
    plotlib.voidAbundance(rv, vger.Nbin_nv, vger.zmin, vger.zmax, vger.sky, vger.par_cosmo, r'R', r'[h^{-1}\mathrm{Mpc}]', 'effective-radius', [1e-10,1e-5], rvr, vger.Nmock, vger.figFormat, vger.plotPath)
    plotlib.redshiftDistribution(zgm, zvm, ngm, nvm, zv, zgrm, zvrm, ngrm, nvrm, vger.vbin, vger.binning, vger.Nvbin, vger.figFormat, vger.plotPath)
    plotlib.tracerBias(zgm, datalib.bz(zgm,vger.par_cosmo), vger.figFormat, vger.plotPath)

    # Data vectors and covariances
    plotlib.xi_p_test(rs, rmi, rvi, xid, [1,-0.8,2.,8.], vger.Nvbin, vger.rmax, vger.figFormat, vger.plotPath)
    plotlib.xi_p(xip, xipE, xips, xid, xipE, xids, xi, xiE, xits, rmi, rs, rvi, zvi, p1, vger.Nvbin, vger.rmax, vger.figFormat, vger.plotPath)
    plotlib.xi(xi, xiE, xits, rmi, rs, rvi, zvi, p1, chi2, vger.Nvbin, vger.rmax, vger.ell, vger.datavec, vger.figFormat, vger.plotPath)
    plotlib.xi_ell(xi, xiE, xits, rmi, rs, rvi, zvi, p1, vger.Nvbin, vger.rmax, vger.ell, vger.figFormat, vger.plotPath)
    plotlib.xi_2d(xi2d, xi2dts, rmi2d, rvi, zvi, p1, chi2, vger.Nvbin, vger.Nspline, vger.rmax, vger.datavec, vger.symLOS, vger.figFormat, vger.plotPath)
    plotlib.xi_cov(xiC, 1, vger.Nvbin, vger.ell, vger.symLOS, vger.figFormat, vger.plotPath)
    plotlib.xi_cov(xi2dC, 2, vger.Nvbin, vger.ell, vger.symLOS, vger.figFormat, vger.plotPath)

    # Cosmological constraints
    plotlib.fs8_DAH(zvi, vger.zmin, vger.zmax, fs8f, fs8e, DAHf, DAHe, tags, vger.par_cosmo, vger.Nspline, vger.figFormat, vger.plotPath)
    plotlib.triangle([samples], p0, p1, rvi, zvi, pLim, ['qpar'], vger.par, vger.Nvbin, vger.vbin, None, None, vger.figFormat, vger.plotPath)
    plotlib.triangle_cosmo(cosmo, logP_cosmo, pLim_cosmo, vger.cosmology, vger.par_cosmo, vger.blind, tags, vger.figFormat, vger.plotPath)

    # Logo background
    #plotlib.logo(xi2dts, p1, vger.Nvbin, vger.Nspline, vger.rmax, -0.8, 0.4, 10, 'Spectral_r', vger.plotPath) # color maps: terrain, bone, coolwarm, BrBG_r, YlGnBu_r, Spectral_r


    print('Done.')

    #####################
    ###### THE END ######
    #####################
