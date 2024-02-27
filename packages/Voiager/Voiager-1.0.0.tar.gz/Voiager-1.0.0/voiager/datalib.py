import gc
import numpy as np
import multiprocessing as mp
from functools import partial
from pathlib import Path
from scipy import integrate, interpolate, optimize
from scipy.special import legendre
from scipy.spatial import cKDTree
from abel.direct import direct_transform as abel
from astropy.table import Table, vstack
from astropy.cosmology import FlatLambdaCDM
import emcee
import healpy
import vide.voidUtil as vu

# Physical constants
G_Newton = 6.67385e-11 # Newton's constant in m^3/kg/s^2
c = 299792.458 # Speed of light in km/s
KmMpc = 3.24078e-20 # km in Mpc
KgMsol = 5.02740e-31 # kg in solar masses
DegRad = 3.14159/180. # degrees in radians


################################
######## Data functions ########
################################

def loadData(vger, tracerPath, voidPath, survey, sample, random, inputFormat, inputExtension, version, columnNames, Nmock=1, mockid='_{0:04d}'):
    """Load tracer and void catalogs (from observation or mocks).

    Args:
        vger (object): instance of Voiager class
        tracerPath (path): name of input folder for tracer file(s)
        voidPath (path): name of input folder fot void file(s)
        survey (str): name of survey
        sample (str): name of tracer sample
        random (str): name of random sample
        inputFormat (str): file type for input tracer and random catalogs
        inputExtension (str): filename extension for input tracer and random catalogs
        version (str): name of void sample
        columnNames (str list): names of column headers for [RA, DEC, Z] in tracer and random catalog (angles in degrees)
        Nmock (int): number of mock realizations if Nmock > 1 (default = 1)
        mockid (str): format string for mock id in file names (e.g. '_1234' as default)

    Returns:
        Ngc, Nvc (int list): number of objects in each tracer and void catalog \n
        Xg, Xr, Xv (ndarray,[len(X),3]): RA, Dec, redshift of tracers, randoms, voids \n
        rv (ndarray,sum(Nvc)): effective void radii \n
        tv (ndarray,sum(Nvc)): tree levels in void hierarchy \n
        dv (ndarray,sum(Nvc)): void core (minimum) densities in units of mean \n
        cv (ndarray,sum(Nvc)): void density contrasts \n
        mv (ndarray,sum(Nvc)): void richness (number of tracers) \n
        vv (ndarray,sum(Nvc)): void volumes \n
        Cv (ndarray,sum(Nvc)): void compensations (average void densities in units of mean) \n
        ev (ndarray,sum(Nvc)): void ellipticities \n
        eval (ndarray,sum(Nvc)): eigenvalues of void inertia tensor \n
        evec (ndarray,sum(Nvc)): eigenvectors of void inertia tensor \n
        mgs (ndarray,sum(Nvc)): mean tracer (galaxy) separation at void redshift in units of effective void radius
    """
    galaxyCatalog, voidCatalog = [],[]
    randomFile = tracerPath / survey / sample / (random+'.'+inputExtension)
    randomData = Table.read(randomFile, format=inputFormat)
    randomCatalog = Table(randomData[columnNames], names=('RA','DEC','Z'))

    mocks = (mockid.format(i+1) for i in range(Nmock)) if (Nmock>1) else [''] # mock indices
    for idm in mocks:
        galaxyFile = tracerPath / survey / sample / (sample+idm+'.'+inputExtension)
        galaxyData = Table.read(galaxyFile, format=inputFormat)
        galaxyCatalog.append(Table(galaxyData[columnNames], names=('RA','DEC','Z')))
        voidFile = voidPath / survey / ('sample_'+sample+version+idm)
        voidCatalog.append(vu.loadVoidCatalog(str(voidFile), dataPortion="central", untrimmed=True, loadParticles=False))

    Ngc = []
    for (i,gC) in enumerate(galaxyCatalog):
        galaxyCatalog[i] = gC[(gC['Z'] >= vger.zmin) & (gC['Z'] <= vger.zmax)]
        Ngc.append(len(galaxyCatalog[i]))

    galaxyCatalog = vstack(galaxyCatalog, join_type='exact')
    randomCatalog = randomCatalog[(randomCatalog['Z'] > vger.zmin) & (randomCatalog['Z'] < vger.zmax)]

    # Galaxies
    Xg = np.vstack([np.array(galaxyCatalog['RA']),np.array(galaxyCatalog['DEC']),np.array(galaxyCatalog['Z'])]).T
    Xg[:,0:2] *= DegRad
    zgm, ngm = numberDensity(Xg[:,2], vger.Nbin_nz, vger.sky, vger.par_cosmo, Nmock)

    # Randoms
    Xr = np.vstack([np.array(randomCatalog['RA']),np.array(randomCatalog['DEC']),np.array(randomCatalog['Z'])]).T
    Xr[:,0:2] *= DegRad

    # Voids
    Nvc, Xv, rv, tv, dv, cv, mv, vv, Cv, ev, eval, evec, mgs = [],[],[],[],[],[],[],[],[],[],[],[],[]
    for i,vC in enumerate(voidCatalog):
        Xv.append(np.vstack((vu.getArray(vC.voids,'RA'),vu.getArray(vC.voids,'Dec'),vu.getArray(vC.voids,'redshift'))).T)
        rv.append(vu.getArray(vC.voids, 'radius'))
        tv.append(vu.getArray(vC.voids, 'treeLevel'))
        dv.append(vu.getArray(vC.voids, 'coreDens')*vC.volNorm/np.interp(Xv[i][:,2],zgm,ngm))
        cv.append(vu.getArray(vC.voids, 'densCon'))
        mv.append(vu.getArray(vC.voids, 'numPart'))
        vv.append(vu.getArray(vC.voids, 'voidVol')/vC.volNorm)
        Cv.append(mv[i]/vv[i]/np.interp(Xv[i][:,2],zgm,ngm))
        ev.append(vu.getArray(vC.voids, 'ellipticity'))
        evali,eveci = [],[]
        for vi in vC.voids:
            evali.append(vi.eigenVals)
            eveci.append(vi.eigenVecs)
        eval.append(np.array(evali))
        evec.append(np.array(eveci))
        # Mean galaxy separation in units of effective void radius as function of redshift
        mgs.append((4*np.pi/3*np.interp(Xv[i][:,2],zgm,ngm))**(-1./3.) / rv[i])

        # Filter voids
        idx_zv = (Xv[i][:,2] >= vger.zvmin) & (Xv[i][:,2] <= vger.zvmax)
        idx_rv = (rv[i] >= vger.rvmin) & (rv[i] <= vger.rvmax)
        idx_mv = (mv[i] >= vger.mvmin) & (mv[i] <= vger.mvmax)
        idx_dv = (dv[i] >= vger.dvmin) & (dv[i] <= vger.dvmax)
        idx_Cv = (Cv[i] >= vger.Cvmin) & (Cv[i] <= vger.Cvmax)
        idx_ev = (ev[i] >= vger.evmin) & (ev[i] <= vger.evmax)
        idx_mgs = (mgs[i] <= 1/vger.mgsmin) & (mgs[i] >= 1/vger.mgsmax)
        idx = idx_zv & idx_rv & idx_mv & idx_dv & idx_Cv & idx_ev & idx_mgs
        Nvc.append(sum(idx))
        Xv[i] = Xv[i][idx]
        rv[i] = rv[i][idx]
        tv[i] = tv[i][idx]
        dv[i] = dv[i][idx]
        cv[i] = cv[i][idx]
        mv[i] = mv[i][idx]
        vv[i] = vv[i][idx]
        Cv[i] = Cv[i][idx]
        ev[i] = ev[i][idx]
        eval[i] = eval[i][idx]
        evec[i] = evec[i][idx]
        mgs[i] = mgs[i][idx]

    Xv = np.vstack(Xv)
    rv = np.hstack(rv)
    tv = np.hstack(tv)
    dv = np.hstack(dv)
    cv = np.hstack(cv)
    mv = np.hstack(mv)
    vv = np.hstack(vv)
    Cv = np.hstack(Cv)
    ev = np.hstack(ev)
    eval = np.vstack(eval)
    evec = np.vstack(evec)
    mgs = np.hstack(mgs)

    Xv[:,0:2] *= DegRad
    del galaxyCatalog,randomCatalog
    gc.collect()

    return Ngc, Nvc, Xg, Xr, Xv, rv, tv, dv, cv, mv, vv, Cv, ev, eval, evec, mgs


def makeRandom(X, N=10., Nside=128, Nbin_nz=20, rv=None, seed=1):
    """Produce unclustered randoms from a spatial distribution of objects (tracers or voids).

    Args:
        X (ndarray,[len(X),3]): RA, Dec, redshift of input catalog
        N (float): number of desired randoms per number of input objects (default = 10)
        Nside (int): healpix resolution (default = 128)
        Nbin_nz (int): number of bins for redshift distribution
        rv (ndarray,len(rv)): if given, generates random void radii from an input void radius distribution (default = None)
        seed (int): seed for generation of randoms (default = 1)

    Returns:
        Xr (ndarray,[N*len(X),3]): RA, Dec, redshift of random catalog \n
        rvr (ndarray,N*len(rv)): if rv is given, random void radii
    """
    # Define mask
    npix = healpy.nside2npix(Nside)
    mask = np.zeros((npix), dtype=bool)
    pix = healpy.ang2pix(Nside, np.pi/2.-X[:,1], X[:,0])
    mask[pix] = True
    skyfrac = 1.*len(mask[mask>0])/len(mask)

    # Generate random sky coordinates
    np.random.seed(seed)
    Xr = np.random.rand(int(N*len(X)/skyfrac),3).astype(np.float32)
    Xr[:,0] *= 2*np.pi # RA
    Xr[:,1] = np.arccos(1.-2*Xr[:,1]) # Dec
    Xr[:,2] = Xr[:,2]*(X[:,2].max()-X[:,2].min()) + X[:,2].min() # Redshift

    (n,z) = np.histogram(X[:,2], bins=Nbin_nz) # Calculate n(z) from catalog
    nr = np.interp(Xr[:,2],(z[:-1]+z[1:])/2.,n) # Interpolate n(z) for randoms
    Xr[:,2] = np.random.choice(Xr[:,2],int(N*len(X)/skyfrac),p=nr/np.sum(nr)) # Draw a random realization from that n(z)

    pixr = healpy.ang2pix(Nside, Xr[:,1], Xr[:,0]) # Masked pixels
    Xr = Xr[mask[pixr],:] # Apply mask to randoms
    Xr[:,1] = np.pi/2. - Xr[:,1]

    # Generate random void radii by reshuffling input voids
    if rv is not None:
        idr = np.random.choice(np.where(rv)[0],len(Xr)) # Generate random indices from input void catalog
        rvr = rv[idr] # Randomly select from input void radius distribution
        Xr[:,2] = X[idr,2] # Use the same selection for void redshift distribution
        return Xr, rvr
    else:
        return Xr


def getBins(yv, binning='eqn', Nbin=2):
    """Define a binning scheme.

    Args:
        yv (ndarray,len(yv)): void property to use for binning
        binning (str / list): 'eqn' for equal number of voids (default), 'lin' for linear, 'log' for logarithmic. Alternatively, provide a list for custom bin edges.
        Nbin (int): number of bins (default = 2)

    Returns:
        bins (ndarray,Nbin+1): bin edges
    """
    if  binning == 'eqn':
        bins = np.zeros(Nbin+1)
        bins[-1] = yv.max()
        bins[:-1] = [np.array_split(np.sort(yv),Nbin)[i][0] for i in range(Nbin)]
    elif binning == 'lin':
        bins = yv.min() + (yv.max() - yv.min())* np.linspace(0,1,Nbin+1)
    elif binning == 'log':
        bins = yv.min() * (yv.max() / yv.min())**np.linspace(0,1,Nbin+1)
    elif type(binning) is list:
        bins = binning
    else: print("Binning scheme not recognized! Options: 'eqn', 'lin', 'log', list")
    return bins


def numberDensity(z, Nbin, sky, par_cosmo, Nmock=1):
    """Number density as function of redshift.

    Args:
        z (ndarray,len(z)): redshifts of all objects
        Nbin (int): number of redshift bins
        sky (float): sky area in square degrees
        par_cosmo (dict): cosmological parameter values
        Nmock (int): number of mock catalogs (default = 1)

    Returns:
        zm (ndarray,Nbin): mean redshift per bin (arithmetic mean of bin edges) \n
        nm (ndarray,Nbin): mean number density
    """
    nm, zm = np.histogram(z, bins=Nbin)
    Vol = sky*DegRad**2/3*(DA0(zm[1:], par_cosmo)**3 - DA0(zm[:-1], par_cosmo)**3)
    zm = (zm[1:]+zm[:-1])/2
    nm = nm/Vol/Nmock
    return zm, nm


def voidAbundance(yv, Nbin, zmin, zmax, sky, par_cosmo, Nmock=1):
    """Void abundance function.

    Args:
        yv (ndarray,len(yv)): arbitrary void property (e.g., effective radius, redshift, core density, ellipticity)
        Nbin (int): number of bins
        zmin (float): minimum redshift
        zmax (float): maximum redshift
        sky (float): sky area in square degrees
        par_cosmo (dict): cosmological parameter values
        Nmock (int): number of mock catalogs (default = 1)

    Returns:
        ym (ndarray,Nbin): mean void property per bin (arithmetic mean of bin edges) \n
        nm (ndarray,Nbin): mean number density of voids per logarithmic bin (dn/dlnx) \n
        nE (ndarray,Nbin): error on mean space density of voids, assuming Poisson statistics
    """
    nm,ym = np.histogram(yv,Nbin)
    ym = (ym[1:]+ym[:-1])/2.
    dym = (ym[1:]-ym[:-1]).mean()
    Vol = sky*DegRad**2/3*(DA0(zmax, par_cosmo)**3 - DA0(zmin, par_cosmo)**3)
    nm = nm/Vol/dym*ym/Nmock
    nE = np.sqrt(nm/Vol/dym*ym)
    return ym, nm, nE


def coordTrans(X, par_cosmo, Ncpu=1):
    """Transformation from angles and redshifts to comoving coordinates.

    Args:
        X (ndarray,[len(X),3]): RA, Dec, redshift
        par_cosmo (dict): cosmological parameter values
        Ncpu (int): number of CPUs for parallel calculation (default = 1 for serial)

    Returns:
        x (ndarray,[len(X),3]): x1, x2, x3
    """
    DA0_ = partial(DA0, par_cosmo=par_cosmo)
    pool = mp.Pool(processes=Ncpu)
    R = np.hstack(pool.map(DA0_, (np.array_split(X[:,2],Ncpu))))
    pool.close(); pool.join()
    x = np.vstack((R*np.cos(X[:,0])*np.cos(X[:,1]),R*np.sin(X[:,0])*np.cos(X[:,1]),R*np.sin(X[:,1]))).T
    return x


def mockShift(x, N, Nmock=1, Lmock=1e5):
    """Coordinate shift of mock catalog. Needed to associate tracers with voids from the same mock.

    Args:
        x (ndarray,[len(x),3]): comoving coordinates
        N (int list,len(N)): number of objects in each mock catalog
        Nmock (int): number of mock catalogs (default = 1)
        Lmock (float): comoving distance between mock catalogs (along x1 axis)

    Returns:
        xs (ndarray,[len(x),3]): shifted comoving coordinates
    """
    xs = np.copy(x)
    for i in range(Nmock):
        xs[sum(N[:i]):sum(N[:i+1]),0] += i*Lmock
    return xs


def getStack(xv, xg, rv, zv, Nv, Ng, ngz, zgm, wg=None, rmax=3, Nbin=20, ell=[0,], symLOS=True, dim=1, Nmock=1, Ncpu=1):
    """Stacked void density profiles from tracer (galaxy) distribution, as a function of void-centric distance in units of effective void radius.

    Args:
        xv (ndarray,[len(xv),3]): comoving coordinates of void centers
        xg (ndarray,[len(xg),3]): comoving coordinates of tracers (galaxies)
        rv (ndarray,len(rv)): effective void radii
        zv (ndarray,len(zv)): void redshifts
        Nv (int list,len(Nv)): number of voids (in each mock catalog)
        Ng (int list,len(Ng)): number of tracers (in each mock catalog)
        ngz (ndarray,len(ngz)): number density of tracers as function of redshift
        zgm (ndarray,len(zgm)): binned tracer redshifts for ngz
        wg (ndarray,len(wg)): weights for tracers (default = None)
        rmax (float): maximum distance from void center in units of effective void radius (default = 3)
        Nbin (int): number of distance bins per dimension  (default = 20)
        ell (int list): multipole orders to calculate (default = [0,])
        symLOS (bool): if True, assume symmetry along LOS (default)
        dim (int): dimension of data vector [0: projected, 1: multipoles (default), 2: POS vs. LOS]
        Nmock (int): number of mock catalogs (default = 1)
        Ncpu (int): number of CPUs for parallel calculation (default = 1 for serial)

    Returns:
        Void density profile, normalized by mean tracer density \n
        n (ndarray,[len(xv),Nrbin]) if dim=0, projected along line-of-sight \n
        n (ndarray,[len(xv),len(ell),Nrbin]) if dim=1, multipoles \n
        n (ndarray,[len(xv),Nrbin,Nrbin]) if dim=2, POS vs. LOS
    """
    # Shift each mock to guarantee correspondence of tracers (not needed for randoms)
    if (Nmock>1):
        xvs = mockShift(xv, Nv)
        xgs = mockShift(xg, Ng)
    else: xvs, xgs = xv, xg

    # Mean tracer density at center position:
    ngz = np.interp(zv,zgm,ngz)
    if dim==0: ngz *= rv # 2*rmax

    # Perform stack
    prof = partial(profile, xv, xg, xvs, xgs, rv, ngz, wg, rmax, Nbin, ell, symLOS, dim)
    idv = np.array_split(range(len(xv)),Ncpu)
    #n = profile(range(len(xv))) # Serial
    pool = mp.Pool(processes=Ncpu) # Parallel
    n = pool.map(prof, idv)
    pool.close(); pool.join()
    n = np.hstack(n)
    n = np.array([n[i] for i in range(len(xv))])
    return n


def profile(xv, xg, xvs, xgs, rv, ngz, wg, rmax, Nbin, ell, symLOS, dim, idv):
    """Wrapper of profile1() with KDTree construction. Needed for parallel execution in getStack(), cannot be pickled inside function.
    """
    # Construct KDTree
    #xgTree = cKDTree.PeriodicCKDTree(np.array([-1,-1,-1]), xgs) # VIDE periodic tree
    #xgTree = cKDTree.cKDTree(xgs) # VIDE standard tree
    xgTree = cKDTree(xgs)
    prof = partial(profile1, xv, xg, xvs, xgs, xgTree, rv, ngz, wg, rmax, Nbin, ell, symLOS, dim)
    prof = np.vectorize(prof, otypes=[np.ndarray])
    return prof(idv)


def profile1(xv, xg, xvs, xgs, xgTree, rv, ngz, wg=None, rmax=3, Nbin=20, ell=[0,], symLOS=True, dim=1, idv=0):
    """Individual void density profile from tracer (galaxy) distribution, as a function of void-centric distance in units of effective void radius.

    Args:
        xv (ndarray,[len(xv),3]): comoving coordinates of void centers
        xg (ndarray,[len(xg),3]): comoving coordinates of tracers (galaxies)
        xvs (ndarray,[len(xv),3]): shifted comoving coordinates of void centers if Nmock > 1
        xgs (ndarray,[len(xg),3]): shifted comoving coordinates of tracers (galaxies) if Nmock > 1
        xgTree (object): instance of KDTree class of tracer (galaxy) distribution
        rv (ndarray,len(rv)): effective void radii
        ngz (ndarray,len(ngz)): mean number density of tracers at redshift of void center
        wg (ndarray,len(wg)): weights for tracers (default = None)
        rmax (float): maximum distance from void center in units of effective void radius (default = 3)
        Nbin (int): number of distance bins per dimension (default = 20)
        ell (int list): multipole orders to calculate (default = [0,])
        symLOS (bool): if True, assume symmetry along LOS (default)
        dim (int): dimension of data vector [0: projected, 1: multipoles (default), 2: POS vs. LOS]
        idv (int): void id (default = 0)

    Returns:
        Void density profile, normalized by mean tracer density \n
        n/ngz (ndarray,Nrbin) if dim==0, projected along line-of-sight \n
        n/ngz (ndarray,[len(ell),Nrbin]) if dim==1, multipoles \n
        n/ngz (ndarray,[Nrbin,Nrbin]) if dim==2, POS vs. LOS
    """
    # Select void id
    xv   = xv[idv,:]
    xvs  = xvs[idv,:]
    rv   = rv[idv]
    ngz  = ngz[idv]

    # Select tracers
    ind = xgTree.query_ball_point(xvs, r=rmax*rv)
    wg = wg[ind] if wg is not None else None
    xg = xg[ind]

    # Calculate distances
    dx = xg - xv
    dx /= rv
    xpar = np.sum(dx*xv,1) # Void-center LOS component
    xv = np.sum(xv**2)
    xv = np.sqrt(xv)
    xpar /= xv
    dx = np.sum(dx**2,1)
    dx = np.sqrt(dx)

    if dim==0: # LOS projected profile
        xper = np.sqrt(abs(dx**2-xpar**2))
        ind = abs(xpar) <= rmax # projection range
        n,r = np.histogram(xper[ind], bins=Nbin, range=(0.,rmax), weights=wg)
        if wg is not None: n /= wg.mean()

    if dim==1: # Multipoles (using weighted histograms based on arXiv:1705.05328)
        mu = xpar/dx
        n = np.zeros((len(ell),Nbin))
        for (j,l) in enumerate(ell):
            Pl = (2*l+1.)*legendre(l)(mu)
            if wg is not None:
                n[j,:],r = np.histogram(dx, bins=Nbin, range=(0.,rmax), weights=wg*Pl)
                n[j,:] /= wg.mean()
            else:
                n[j,:],r = np.histogram(dx, bins=Nbin, range=(0.,rmax), weights=Pl)

    elif dim==2: # POS vs. LOS profile
        xper = np.sqrt(abs(dx**2-xpar**2))
        if symLOS: # Symmetrize along LOS:
            n,r,rr = np.histogram2d(xper, abs(xpar), bins=[Nbin,Nbin], range=[[0,rmax],[0,rmax]], weights=wg)
            n /= 2.
        else:
            n,r,rr = np.histogram2d(xper, xpar, bins=[Nbin,2*Nbin], range=[[0,rmax],[-rmax,rmax]], weights=wg)

        if wg is not None: n /= wg.mean()

    return n/ngz


def getData(DDp, DRp, RDp, RRp, DD, DR, RD, RR, DD2d, DR2d, RD2d, RR2d, rv, rvr, zv, zvr, par, par_cosmo, vbin='zv', binning='eqn', Nvbin=2, Nrbin=20, rmax=3, ell=[0,], symLOS=True, project2d=True, rescov=False, Ncpu=1):
    """Retrieve data vectors for two-point correlations and covariances.

    Args:
        DDp, DRp, RDp, RRp (ndarray,[len(rv),Nrbin]): projected void density profiles between data and randoms
        DD, DR, RD, RR (ndarray,[len(rv),len(ell),Nrbin]): multipoles of void density profiles between data and randoms
        DD2d, DR2d, RD2d, RR2d (ndarray,[len(rv),Nrbin,Nrbin]): POS vs. LOS void density profiles between data and randoms
        rv (ndarray,len(rv)): effective void radii
        rvr (ndarray,len(rvr)): effective void radii randoms
        zv (ndarray,len(zv)): void redshifts
        zvr (ndarray,len(zv)): void redshifts randoms
        par (dict): model parameter values
        par_cosmo (dict): cosmological parameter values
        vbin (str): binning strategy, 'zv': void-redshift bins (default), 'rv': void-radius bins
        binning (str / list): 'eqn' for equal number of voids (default), 'lin' for linear, 'log' for logarithmic. Alternatively, provide a list for custom bin edges.
        Nvbin (int): number of void bins (default = 2)
        Nrbin (int): number of distance bins per dimension (default = 20)
        rmax (float): maximum distance from void center in units of effective void radius (default = 3)
        ell (int list): multipole orders to calculate (default = [0,])
        symLOS (bool): if True, assume symmetry along LOS (default)
        project2d (bool): if True, use POS vs. LOS void density profiles to calculate projected void density profiles (default = True)
        rescov (bool): if True, calculate covariance matrix for residuals between data and model (default = False, experimental!)
        Ncpu (int): number of CPUs for parallel calculation (default = 1 for serial)

    Returns:
        Nvi (ndarray,Nvbin): number of voids per bin \n
        rvi (ndarray,Nvbin): average effective void radius per bin \n
        zvi (ndarray,Nvbin): average void redshift per bin \n
        rmi (ndarray,[Nvbin,Nrbin]): radial distances from void center for each bin \n
        rmi2d (ndarray,[Nvbin,(2*)Nrbin2d]): POS and LOS distances from void center for each bin \n
        xip, xipE (ndarray,[Nvbin,Nrbin]): LOS projected void-tracer correlation function and its error \n
        xi, xiE (ndarray,[Nvbin,len(ell),Nrbin]): multipoles of void-tracer correlation function and its error \n
        xiC, xiCI (ndarray,[Nvbin,len(ell)*Nrbin,len(ell)*Nrbin]): covariance of multipoles and its inverse \n
        xi2d (ndarray,[Nvbin,Nrbin2d,(2*)Nrbin2d]): POS vs. LOS 2d void-tracer correlation function \n
        xi2dC, xi2dCI (ndarray,[Nvbin,(2*)Nrbin2d**2,(2*)Nrbin2d**2]): covariance of POS vs. LOS 2d void-tracer correlation function and its inverse \n
    """
    # Initialize binned quantities
    Nell = len(ell)
    Nvi = np.zeros(Nvbin)
    Nvri = np.zeros(Nvbin)
    rvi = np.zeros(Nvbin)
    rvri = np.zeros(Nvbin)
    zvi = np.zeros(Nvbin)
    rmi = np.zeros((Nvbin,Nrbin))
    rm = np.linspace(0,rmax,Nrbin+1)
    Npar = len(par.values())
    p0 = np.zeros((Nvbin,Npar))
    p0[:] = list(par.values())

    # Projected correlation
    if not project2d:
        DDpm = np.zeros((Nvbin,Nrbin))
        Vp = np.pi*(rm[1:]**2-rm[:-1]**2)

    # Multipoles
    DDm = np.zeros((Nvbin,Nell,Nrbin))
    V = 4*np.pi/3*(rm[1:]**3-rm[:-1]**3)

    # POS vs. LOS 2d correlation
    if symLOS:
        rmi2d = np.zeros((Nvbin,Nrbin))
        DD2dm = np.zeros((Nvbin,Nrbin,Nrbin))
        V2d = np.zeros((Nrbin,Nrbin))
        r2d = np.linspace(0,rmax,Nrbin+1)
        for i in range(Nrbin):
            for j in range(Nrbin):
                V2d[i,j] = np.pi*(r2d[i+1]**2-r2d[i]**2)*(r2d[j+1]-r2d[j])
    else:
        rmi2d = np.zeros((Nvbin,2*Nrbin))
        DD2dm = np.zeros((Nvbin,Nrbin,2*Nrbin))
        V2d = np.zeros((Nrbin,2*Nrbin))
        r2d = np.linspace(-rmax,rmax,2*Nrbin+1)
        for i in range(Nrbin):
            for j in range(2*Nrbin):
                V2d[i,j] = np.pi*(r2d[Nrbin+i+1]**2-r2d[Nrbin+i]**2)*(r2d[j+1]-r2d[j])

    # Define binning
    if vbin == 'rv': yv, yvr = np.copy([rv,rvr])
    if vbin == 'zv': yv, yvr = np.copy([zv,zvr])
    bins = getBins(yv,binning,Nvbin)

    # Stack individual void profiles and normalize by shell volumes (not necessary, but useful. Cancels out in LS estimator)
    DDpj, DRpj, DDj, DRj, DD2dj, DR2dj = [],[],[],[],[],[]
    if not project2d: DRpm, RDpm, RRpm = np.copy([DDpm,DDpm,DDpm])
    DRm, RDm, RRm = np.copy([DDm,DDm,DDm])
    DR2dm, RD2dm, RR2dm = np.copy([DD2dm,DD2dm,DD2dm])
    for i in range(Nvbin):
        idx  = (yv  > bins[i]) & (yv  <= bins[i+1])
        idxr = (yvr > bins[i]) & (yvr <= bins[i+1])
        Nvi[i] = len(yv[idx])
        Nvri[i] = len(yvr[idxr])
        rvi[i] = np.mean(rv[idx])
        rvri[i] = np.mean(rvr[idxr])
        zvi[i] = np.mean(zv[idx])
        rmi[i] = (rm[1:]+rm[:-1])*rvi[i]/2.
        rmi2d[i] = (r2d[1:]+r2d[:-1])*rvi[i]/2.

        if not project2d:
            DDpm[i] = np.sum(DDp[idx] ,0)/Nvi[i]/Vp/rvi[i]**2
            DRpm[i] = np.sum(DRp[idx] ,0)/Nvi[i]/Vp/rvi[i]**2
            RDpm[i] = np.sum(RDp[idxr],0)/Nvri[i]/Vp/rvri[i]**2
            RRpm[i] = np.sum(RRp[idxr],0)/Nvri[i]/Vp/rvri[i]**2

        DDm[i] = np.sum(DD[idx] ,0)/Nvi[i]/V/rvi[i]**3
        DRm[i] = np.sum(DR[idx] ,0)/Nvi[i]/V/rvi[i]**3
        RDm[i] = np.sum(RD[idxr],0)/Nvri[i]/V/rvri[i]**3
        RRm[i] = np.sum(RR[idxr],0)/Nvri[i]/V/rvri[i]**3

        DD2dm[i] = np.sum(DD2d[idx] ,0)/Nvi[i]/V2d/rvi[i]**3
        DR2dm[i] = np.sum(DR2d[idx] ,0)/Nvi[i]/V2d/rvi[i]**3
        RD2dm[i] = np.sum(RD2d[idxr],0)/Nvri[i]/V2d/rvri[i]**3
        RR2dm[i] = np.sum(RR2d[idxr],0)/Nvri[i]/V2d/rvri[i]**3

        # Jackknives
        if not project2d:
            DDpj.append(jackknife(DDp[idx], DDpm[i], rv[idx], Vp, dim=2, Ncpu=Ncpu))
            DRpj.append(jackknife(DRp[idx], DRpm[i], rv[idx], Vp, dim=2, Ncpu=Ncpu))
        DDj.append(jackknife(DD[idx], DDm[i], rv[idx], V, dim=3, Ncpu=Ncpu))
        DRj.append(jackknife(DR[idx], DRm[i], rv[idx], V, dim=3, Ncpu=Ncpu))
        DD2dj.append(jackknife(DD2d[idx], DD2dm[i], rv[idx], V2d, dim=3, Ncpu=Ncpu))
        DR2dj.append(jackknife(DR2d[idx], DR2dm[i], rv[idx], V2d, dim=3, Ncpu=Ncpu))

    # Mean of RR2d inside void radius
    indmax = int(len(RR2dm[0])/rmax)
    RR_mean = RR2dm[:,:indmax,:indmax].mean(axis=(1,2))

    # Range where POS vs. LOS 2d correlation function is non-zero
    Nrcut = Nrbin - int(Nrbin/np.sqrt(2)+1)
    Nrbin2d = Nrbin - Nrcut

    # Landy & Szalay estimator
    xip = np.zeros((Nvbin,Nrbin))
    xi = np.zeros((Nvbin,Nell,Nrbin))
    xi2d = np.zeros((Nvbin,Nrbin,Nrbin)) if symLOS else np.zeros((Nvbin,Nrbin,2*Nrbin))
    xipC = np.zeros((Nvbin,Nrbin,Nrbin))
    xiC = np.zeros((Nvbin,Nell*Nrbin,Nell*Nrbin))
    xi2dC = np.zeros((Nvbin,Nrbin**2,Nrbin**2)) if symLOS else np.zeros((Nvbin,2*Nrbin**2,2*Nrbin**2))
    for i in range(Nvbin):
        xi[i] = estimator(DDm[i], DRm[i], RDm[i], RRm[i], 1, rmax)
        xi2d[i] = estimator(DD2dm[i], DR2dm[i], RD2dm[i], RR2dm[i], 2, rmax)
        if project2d:
            if symLOS: xip[i,:-Nrcut] = 2*np.trapz(xi2d[i,:-Nrcut,:-Nrcut], x=rmi2d[i,:-Nrcut]/rvi[i], axis=1)
            else:      xip[i,:-Nrcut] = np.trapz(xi2d[i,:-Nrcut,Nrcut:-Nrcut], x=rmi2d[i,Nrcut:-Nrcut]/rvi[i], axis=1)
        else:
            xip[i] = estimator(DDpm[i], DRpm[i], RDpm[i], RRpm[i], 0, rmax)

        # Jackknives of data
        xipj = np.zeros((Nvbin,int(Nvi[i]),Nrbin))
        xij = np.zeros((Nvbin,int(Nvi[i]),Nell,Nrbin))
        xi2dj = np.zeros((Nvbin,int(Nvi[i]),Nrbin,Nrbin)) if symLOS else np.zeros((Nvbin,int(Nvi[i]),Nrbin,2*Nrbin))
        if rescov:
            ximj = np.copy(xij)
            xi2dmj = np.copy(xi2dj)
        for j in range(int(Nvi[i])):
            xij[i,j] = estimator(DDj[i][j], DRj[i][j], RDm[i], RRm[i], 1, rmax)
            xi2dj[i,j] = estimator(DD2dj[i][j], DR2dj[i][j], RD2dm[i], RR2dm[i], 2, rmax)
            if project2d:
                if symLOS: xipj[i,j,:-Nrcut] = 2*np.trapz(xi2dj[i,j,:-Nrcut,:-Nrcut], x=rmi2d[i,:-Nrcut]/rvi[i], axis=1)
                else:      xipj[i,j,:-Nrcut] = np.trapz(xi2dj[i,j,:-Nrcut,Nrcut:-Nrcut], x=rmi2d[i,Nrcut:-Nrcut]/rvi[i], axis=1)
            else:
                xipj[i,j] = estimator(DDpj[i][j], DRpj[i][j], RDpm[i], RRpm[i], 0, rmax)

        # Jackknives of model
            if rescov:
                p0[:,0] = f_b_z(zvi, par_cosmo) # Fiducial f/b values
                ximj[i,j] = getModel(rmi,rmi2d,rvi,xipj[:,j,:],xipj[:,j,:],rmax,ell,0.)[2][i](*p0[i])
                xi2dmj[i,j,:-Nrcut,:-Nrcut] = getModel(rmi,rmi2d[:,:-Nrcut],rvi,xipj[:,j,:],xipj[:,j,:],rmax,ell,0.)[3][i](*p0[i])

        # Covariance
        xipC[i] = (Nvi[i]-1.)**2/Nvi[i]*np.cov(xipj[i], rowvar=0)*RR_mean[i]**2 # Volume normalization from randoms
        if rescov: # for residuals between data and model
            xiC[i] = (Nvi[i]-1.)**2/Nvi[i]*np.cov((xij[i]-ximj[i]).reshape((int(Nvi[i]),Nell*Nrbin)), rowvar=0)*RR_mean[i]**2
            if symLOS: xi2dC[i] = (Nvi[i]-1.)**2/Nvi[i]*np.cov((xi2dj[i]-xi2dmj[i]).reshape((int(Nvi[i]),  Nrbin**2)), rowvar=0)*RR_mean[i]**2
            else:      xi2dC[i] = (Nvi[i]-1.)**2/Nvi[i]*np.cov((xi2dj[i]-xi2dmj[i]).reshape((int(Nvi[i]),2*Nrbin**2)), rowvar=0)*RR_mean[i]**2
        else: # for data only
            xiC[i] = (Nvi[i]-1.)**2/Nvi[i]*np.cov(xij[i].reshape((int(Nvi[i]),Nell*Nrbin)), rowvar=0)*RR_mean[i]**2
            if symLOS: xi2dC[i] = (Nvi[i]-1.)**2/Nvi[i]*np.cov(xi2dj[i].reshape((int(Nvi[i]),  Nrbin**2)), rowvar=0)*RR_mean[i]**2
            else:      xi2dC[i] = (Nvi[i]-1.)**2/Nvi[i]*np.cov(xi2dj[i].reshape((int(Nvi[i]),2*Nrbin**2)), rowvar=0)*RR_mean[i]**2

    # Cut zeros in POS vs. LOS 2d correlation function and covariance
    if symLOS: # Symmetric along LOS
        rmi2d = rmi2d[:,:-Nrcut]
        xi2d  = xi2d[:,:-Nrcut,:-Nrcut]
        xi2dC = xi2dC.reshape((Nvbin,Nrbin,Nrbin,Nrbin,Nrbin))
        xi2dC = xi2dC[:,:-Nrcut,:-Nrcut,:-Nrcut,:-Nrcut]
        xi2dC = xi2dC.reshape((Nvbin,Nrbin2d**2,Nrbin2d**2))
    else:
        rmi2d = rmi2d[:,Nrcut:-Nrcut]
        xi2d  = xi2d[:,:-Nrcut,Nrcut:-Nrcut]
        xi2dC = xi2dC.reshape((Nvbin,Nrbin,2*Nrbin,Nrbin,2*Nrbin))
        xi2dC = xi2dC[:,:-Nrcut,Nrcut:-Nrcut,:-Nrcut,Nrcut:-Nrcut]
        xi2dC = xi2dC.reshape((Nvbin,2*Nrbin2d**2,2*Nrbin2d**2))

    # Standard deviation and inverse covariance with Hartlap correction
    xiE = np.zeros((Nvbin,Nell,Nrbin))
    xipE = np.zeros((Nvbin,Nrbin))
    xiCI = np.copy(xiC)
    xi2dCI = np.copy(xi2dC)
    # Mean error along LOS
    for i in range(Nvbin):
        if project2d:
            if symLOS: xipE[i,:Nrbin2d] = np.sqrt(np.mean(np.diagonal(xi2dC[i,:,:]).reshape((Nrbin2d,Nrbin2d)), axis=1))
            else:      xipE[i,:Nrbin2d] = np.sqrt(np.mean(np.diagonal(xi2dC[i,:,:]).reshape((Nrbin2d,2*Nrbin2d)), axis=1))
        else:
            xipE[i,:] = np.diagonal(xipC[i,:,:])**0.5

        xiCI[i,:,:] = np.linalg.inv(xiC[i,:,:])*(Nvi[i]-Nell*Nrbin-2.)/(Nvi[i]-1.) # Hartlap factor
        for j in range(Nell):
            xiE[i,j,:] = (np.diagonal(xiC[i,:,:])**0.5)[j*Nrbin:(j+1)*Nrbin]

        if symLOS: xi2dCI[i,:,:] = np.linalg.inv(xi2dC[i,:,:])*(Nvi[i]-Nrbin2d**2-2.)/(Nvi[i]-1.)
        else:      xi2dCI[i,:,:] = np.linalg.inv(xi2dC[i,:,:])*(Nvi[i]-2*Nrbin2d**2-2.)/(Nvi[i]-1.)

    return Nvi, rvi, zvi, rmi, rmi2d, xip, xipE, xi, xiE, xiC, xiCI, xi2d, xi2dC, xi2dCI


def estimator(DDm, DRm, RDm, RRm, dim=1, rmax=3):
    """Landy-Szalay estimator.

    Args:
        DDm, DRm, RDm, RRm (ndarray,*): stacked void-tracer correlations between data and randoms
        dim (int): dimension of data vector [0: projected, 1: multipoles (default), 2: POS vs. LOS]
        rmax (float): maximum distance from void center in units of effective void radius (default = 3)


    Returns:
        xi (ndarray,*): void-tracer correlation function [0: projected, 1: multipoles (default), 2: POS vs. LOS]
    """
    if dim==0: # projected correlation
        xi = np.divide(DDm - DRm - RDm + RRm, RRm, where=(RRm!=0.))*2*rmax # Multiply by projection range
    if dim==1: # multipoles
        xi = np.divide(DDm - DRm - RDm + RRm, RRm[0,:], where=(RRm[0,:]!=0.)) # Only divide by RR monopole
    if dim==2: # POS vs. LOS 2d correlation
        xi = np.divide(DDm - DRm - RDm + RRm, RRm, where=(RRm!=0.))
    return xi


def jackknife(DD, DDm, rv, V, dim=1, Ncpu=1):
    """Generate jackknife samples from all void density profiles.

    Args:
        DD (ndarray,[len(rv),*]): void density profiles
        DDm (ndarray,*): stacked void density profile
        rv (ndarray,len(rv)): effective void radii
        V (ndarray,*): shell volumes
        dim (int): dimension of data vector [0: projected, 1: multipoles (default), 2: POS vs. LOS]
        Ncpu (int): number of CPUs for parallel calculation (default = 1 for serial)

    Returns:
        DDj (ndarray,[len(rv),*]): jackknife samples of stacked void density profile
    """
    jkn = partial(jackknife1, DD, DDm, rv, V, dim)
    jkn = np.vectorize(jkn, otypes=[np.ndarray])
    #DDj = jkn(range(int(len(DD)))) # Serial
    args = np.array_split(range(int(len(DD))),Ncpu)
    pool = mp.Pool(processes=Ncpu)
    DDj = pool.map(jkn, args)
    pool.close(); pool.join()
    DDj = np.hstack(DDj)
    DDj = np.array([DDj[i] for i in range(int(len(DD)))])
    return DDj


def jackknife1(DD, DDm, rv, V, dim=1, idv=0):
    """Generate a single delete-one jackknife sample from all void density profiles.

    Args:
        DD (ndarray,[len(rv),*]): void density profiles
        DDm (ndarray,*): stacked void density profile
        rv (ndarray,len(rv)): effective void radii
        V (ndarray,*): shell volumes
        dim (int): dimension of data vector [0: projected, 1: multipoles (default), 2: POS vs. LOS]
        idv (int): void id (default = 0)

    Returns:
        DDj (ndarray,[len(rv),*]): jackknife sample of void density profile
    """
    DDj = np.sum(np.delete(DD,idv,axis=0),0)/(len(DD)-1)/V/np.mean(np.delete(rv,idv))**dim - DDm
    return DDj


def getModel(rmi, rmi2d, rvi, xip, xipE, rmax=3, ell=[0,], Nsmooth=0., Nspline=200, weight=None):
    """Retrieve theory model for two-point correlations.

    Args:
        rmi (ndarray,[Nvbin,Nrbin]): radial distances from void center for each bin
        rmi2d (ndarray,[Nvbin,(2*)Nrbin2d]): POS and LOS distances from void center for each bin
        rvi (ndarray,Nvbin): average effective void radius per bin
        xip, xipE (ndarray,[Nvbin,Nrbin]): LOS projected void-tracer correlation function and its error
        rmax (float): maximum distance from void center in units of effective void radius (default = 3)
        ell (int list): multipole orders to calculate (default = [0,])        
        Nsmooth (float): smoothing factor for spline of xip and xid in units of average variance, increase for more smoothing (default = 0 for no spline)
        Nspline (int): number of nodes for spline if Nsmooth > 0 (default = 200)
        weight (ndarray,[Nvbin,Nrbin]): weights for spline (default = None)

    Returns:
        rs (ndarray,Nspline): splined radial distances from void center in units of void effective radius (if Nsmooth > 0) \n
        xips (ndarray,[Nvbin,Nspline]): spline of LOS projected void-tracer correlation function (if Nsmooth > 0) \n
        xid (ndarray,[Nvbin,Nrbin]): deprojected void-tracer correlation function \n
        xids (ndarray,[Nvbin,Nspline]): spline of deprojected void-tracer correlation function (if Nsmooth > 0) \n
        Xid (ndarray,[Nvbin,Nrbin]): radially averaged deprojected void-tracer correlation function \n
        Xids (ndarray,[Nvbin,Nspline]): spline of radially averaged deprojected void-tracer correlation function (if Nsmooth > 0) \n
        xit (ndarray,[Nvbin,len(ell),Nrbin]): theory model for multipoles of void-tracer correlation function \n
        xits (ndarray,[Nvbin,len(ell),Nspline]): spline of theory model for multipoles of void-tracer correlation function (if Nsmooth > 0) \n
        xi2dt (ndarray,[Nvbin,Nrbin2d,(2*)Nrbin2d]): theory model for POS vs. LOS 2d void-tracer correlation function \n
        xi2dts (ndarray,[Nvbin,10*Nspline,20*Nspline]): spline of theory model for POS vs. LOS 2d void-tracer correlation function (if Nsmooth > 0)
    """
    Nvbin = len(rvi)
    Nrbin = len(rmi[0])

    if Nsmooth>0.:
        rs = np.linspace((rmi[0]/rvi[0]).min(),(rmi[0]/rvi[0]).max(),Nspline)  # np.linspace(1e-3,rmax,Nspline)
        xips = np.zeros((Nvbin,len(rs)))
        for i in range(Nvbin):
            w = weight[i]/weight[i].mean() if weight is not None else None
            s = np.mean(xipE[i,:sum(xipE[0]>0.)]**2)
            spline = interpolate.UnivariateSpline(rmi[i,:]/rvi[i], xip[i,:], w=w, s=Nsmooth*s, k=3) #, ext=3)
            xips[i,:] = spline(rs)

    # Deprojected correlation function
    xid = np.zeros((Nvbin,Nrbin))
    for i in range(Nvbin): xid[i] = abel(xip[i], r=rmi[i]/rvi[i], direction='inverse', correction=True)
    if Nsmooth>0.:
        xids = np.zeros((Nvbin,Nspline))
        for i in range(Nvbin):
            w = weight[i]/weight[i].mean() if weight is not None else None
            s = np.mean(xipE[i,:sum(xipE[0]>0.)]**2)
            spline = interpolate.UnivariateSpline(rmi[i,:]/rvi[i], xid[i,:], w=w, s=Nsmooth*s, k=3) #, ext=3)
            xids[i] = spline(rs)
            #xids[i] = abel(xips[i], r=rs, direction='inverse', correction=True)

    # Deprojected radially averaged correlation function (with correction for first bin)
    Xid = np.zeros((Nvbin,Nrbin))
    for i in range(Nvbin):
        Xid[i] = 3/rmi[i]**3*integrate.cumtrapz(xid[i]*rmi[i]**2, rmi[i], initial=0.) + xid[i,1]*(rmi[i][0]/rmi[i])**3

    if Nsmooth>0.:
        Xids = np.zeros((Nvbin,Nspline))
        for i in range(Nvbin):
            Xids[i] = 3/rs**3*integrate.cumtrapz(xids[i]*rs**2, rs, initial=0.) + xids[i,1]*(rs[0]/rs)**3

    # Theory model correlation functions
    xit,xits,xi2dt,xi2dts = [],[],[],[]
    for i in range(Nvbin):
        xit.append(partial(xi_model, ell, rmi[i], rmi[i], xid[i], Xid[i])) # no spline
        xi2dt.append(partial(xi_model, None, rmi2d[i], rmi[i], xid[i], Xid[i]))
        if Nsmooth>0.:
            rspar = np.linspace(-rmax,rmax,2*10*Nspline) # for 2d splines (more nodes required)
            xits.append(partial(xi_model, ell, rs, rs, xids[i], Xids[i]))
            xi2dts.append(partial(xi_model, None, rspar, rs, xids[i], Xids[i]))

    if Nsmooth>0.:
        return rs, xips, xid, xids, Xid, Xids, xit, xits, xi2dt, xi2dts
    else:
        return xid, Xid, xit, xi2dt



################################
##### Likelihood functions #####
################################

def bestFit(par, prior, par_cosmo, zvi, xit, xi, xiC, xiCI, ell=[0,], datavec='2d', Nrskip=1, symLOS=True, Nmock=1):
    """Find best fit of model to data.

    Args:
        par (dict): model parameter values
        prior (dict): boundary values for uniform parameter priors
        par_cosmo (dict): cosmological parameter values
        zvi (ndarray,Nvbin): average void redshift per bin
        xit (ndarray,[Nvbin,*]): theory model for void-tracer correlation function (either multipoles or POS vs. LOS)
        xi  (ndarray,[Nvbin,*]): data for void-tracer correlation function (either multipoles or POS vs. LOS)
        xiC, xiCI (ndarray,[Nvbin,*]): covariance of void-tracer correlation function and its inverse
        ell (int list): multipole orders to calculate (default = [0,])
        datavec (str): Define data vector, '1d': multipoles, '2d': POS vs. LOS 2d correlation function (default)
        Nrskip (int): Number of radial bins to skip in fit (starting from the first bin, default = 1)
        symLOS (bool): if True, assume symmetry along LOS (default)
        Nmock (int): number of mock realizations if Nmock > 1 (default = 1)

    Returns:
        p0 (ndarray,[Nvbin,Npar]): fiducial model parameter values used as initial guess \n
        p1 (ndarray,[Nvbin,Npar]): best-fit model parameter values \n
        chi2 (ndarray,Nvbin): reduced chi-squared values of best fit
    """
    Nvbin = len(zvi)
    Nrbin = len(xi[0,0])
    Npar = len(par.values())
    p0 = np.zeros((Nvbin,Npar))
    p0[:] = list(par.values())
    p0[:,0] = f_b_z(zvi, par_cosmo)
    pr = list(prior.values()) # prior

    if datavec=='1d': Ndof = len(ell)*(Nrbin-Nrskip) - Npar
    if datavec=='2d': Ndof = len(xi[0])**2 - Nrskip**2 - Npar if symLOS else 2*(len(xi[0])**2-Nrskip**2) - Npar

    p1, chi2 = np.zeros((Nvbin,Npar)), np.zeros(Nvbin)
    for i in range(Nvbin):
        p1[i,:], chi2[i] = minChi2(p0[i], pr, xit[i], xi[i], xiC[i], xiCI[i], ell, Nrskip, symLOS, Ndof, Nmock)

    return p0, p1, chi2


def minChi2(par, prior, xit, xi, xiC, xiCI, ell=[0,], Nrskip=1, symLOS=True, Ndof=1, Nmock=1):
    """Minimize the reduced chi-square.

    Args:
        par (ndarray,Npar): fiducial model parameter values used as initial guess
        prior (dict): boundary values for uniform parameter priors
        xit (ndarray,[Nvbin,*]): theory model for void-tracer correlation function (either multipoles or POS vs. LOS)
        xi  (ndarray,[Nvbin,*]): data for void-tracer correlation function (either multipoles or POS vs. LOS)
        xiC, xiCI (ndarray,[Nvbin,*]): covariance of void-tracer correlation function and its inverse
        ell (int list): multipole orders to calculate (default = [0,])
        Nrskip (int): Number of radial bins to skip in fit (starting from the first bin, default = 1)
        symLOS (bool): if True, assume symmetry along LOS (default)
        Ndof (int): number of degrees of freedom (data points - free parameters)
        Nmock (int): number of mock realizations if Nmock > 1 (default = 1)

    Returns:
        fit.x (ndarray,Npar): best-fit model parameter values \n
        fit.fun (float): reduced chi-squared value of best fit
    """
    fit = optimize.minimize(Chi2, par, args=(prior, xit, xi, xiC, xiCI, ell, Nrskip, symLOS, Ndof, Nmock), method='Nelder-Mead')
    return fit.x, fit.fun


def Chi2(par, prior, xit, xi, xiC, xiCI, ell=[0,], Nrskip=1, symLOS=True, Ndof=1, Nmock=1):
    """Reduced chi-square.

    Args:
        par (ndarray,Npar): fiducial model parameter values used as initial guess
        prior (dict): boundary values for uniform parameter priors
        xit (ndarray,*): theory model for void-tracer correlation function (either multipoles or POS vs. LOS)
        xi  (ndarray,*): data for void-tracer correlation function (either multipoles or POS vs. LOS)
        xiC, xiCI (ndarray,*): covariance of void-tracer correlation function and its inverse
        ell (int list): multipole orders to calculate (default = [0,])
        Nrskip (int): Number of radial bins to skip in fit (starting from the first bin, default = 1)
        symLOS (bool): if True, assume symmetry along LOS (default)
        Ndof (int): number of degrees of freedom (data points - free parameters)
        Nmock (int): number of mock realizations if Nmock > 1 (default = 1)

    Returns:
        chi2 (float): reduced chi-squared value
    """
    chi2 = -2*lnL(par, prior, xit, xi, xiC, xiCI, ell, Nrskip, symLOS, Nmock)*Nmock/float(Ndof)
    return chi2


def lnL(par, prior, xit, xi, xiC, xiCI, ell=[0,], Nrskip=1, symLOS=True, Nmock=1):
    """Log likelihood.

    Args:
        par (ndarray,Npar): model parameter values
        prior (dict): boundary values for uniform parameter priors
        xit (ndarray,*): theory model for void-tracer correlation function (either multipoles or POS vs. LOS)
        xi  (ndarray,*): data for void-tracer correlation function (either multipoles or POS vs. LOS)
        xiC, xiCI (ndarray,*): covariance of void-tracer correlation function and its inverse
        ell (int list): multipole orders to calculate (default = [0,])
        Nrskip (int): Number of radial bins to skip in fit (starting from the first bin, default = 1)
        symLOS (bool): if True, assume symmetry along LOS (default)
        Nmock (int): number of mock realizations if Nmock > 1 (default = 1)

    Returns:
        lnL (float): Logarithm of the likelihood multiplied by the prior
    """
    Delta = xi - xit(*par)
    if len(Delta)==len(ell): Delta[:,:Nrskip] = 0.
    elif symLOS: Delta[:Nrskip,:Nrskip] = 0.
    else: Delta[:Nrskip,len(Delta)-Nrskip:len(Delta)+Nrskip] = 0.
    Delta = Delta.flatten()
    lnL = -0.5*np.dot(Delta,np.dot(xiCI,Delta))/Nmock # -0.5*np.linalg.slogdet(xiC)[1]
    #lnL = np.sum(-0.5*np.dot(Delta,Delta)/xiC.diagonal())/Nmock
    return lnL + lnP(par,prior)


def lnP(par, prior):
    """Logarithm of uniform prior.

    Args:
        par (dict): model parameter values
        prior (dict): boundary values for uniform parameter priors

    Returns:
        lnP (float): Logarithm of the uniform prior
    """
    accept = True
    for i in range(len(par)):
        accept &= True if prior[i][0] < par[i] < prior[i][1] else False
    lnP = 0. if accept else -np.inf
    return lnP


def runMCMC(p1, par, prior, xit, xi, xiC, xiCI, vbin='zv', ell=[0,], datavec='2d', Nrskip=1, symLOS=True, Nmock=1, Nwalk=1, Nchain=100, filename='chains.dat', outPath='results/'):
    """Monte Carlo Markov Chain sampler.

    Args:
        p1 (ndarray,[Nvbin,Npar]): best-fit model parameter values
        par (dict): model parameter values
        prior (dict): boundary values for uniform parameter priors
        xit (ndarray,*): theory model for void-tracer correlation function (either multipoles or POS vs. LOS)
        xi  (ndarray,*): data for void-tracer correlation function (either multipoles or POS vs. LOS)
        xiC, xiCI (ndarray,*): covariance of void-tracer correlation function and its inverse
        vbin (str): binning strategy, 'zv': void-redshift bins (default), 'rv': void-radius bins
        ell (int list): multipole orders to calculate (default = [0,])
        datavec (str): Define data vector, '1d': multipoles, '2d': POS vs. LOS 2d correlation function (default)
        Nrskip (int): Number of radial bins to skip in fit (starting from the first bin, default = 1)
        symLOS (bool): if True, assume symmetry along LOS (default)
        Nmock (int): number of mock realizations if Nmock > 1 (default = 1)
        Nwalk (int): number of MCMC walkers (default = 1)
        Nchain (int): length of each MCMC chain (default = 100)
        filename (str): name of output file for chains (default = 'chain.dat')
        outPath (path): name of output path for chains (default = 'results/')

    Returns:
        sampler (object list,Nvbin): instance of EnsembleSampler class containing the chains for each void bin
    """
    sampler = []
    Nvbin = len(p1)
    Npar = len(par.values())
    pr = list(prior.values()) # prior
    for i in range(Nvbin):
        #backend.reset(Nwalk, Npar)
        #sampler[i].reset()
        backend = emcee.backends.HDFBackend(Path(outPath) / filename, name=vbin+str(i)) # emcee.backends.Backend()

        # Ball around best fit as initial parameter values, uniform-randomly distributed with maximum relative error of 5%
        p1i = p1[i]*(1. + 0.1*(np.random.rand(Nwalk,Npar)-0.5))
        if datavec=='1d':
            pool = mp.Pool()
            sampler.append(emcee.EnsembleSampler(Nwalk, Npar, lnL, pool=pool, args=[pr, xit[i], xi[i], xiC[i], xiCI[i], ell, Nrskip, symLOS, Nmock], backend=backend))
        if datavec=='2d':
            sampler.append(emcee.EnsembleSampler(Nwalk, Npar, lnL, args=[pr, xit[i], xi[i], xiC[i], xiCI[i], ell, Nrskip, symLOS, Nmock], backend=backend))

        pos, prob, state = sampler[i].run_mcmc(p1i, Nchain, progress=True)

        if datavec=='1d': pool.close(); pool.join()

    # Diagnostics:
    #acf, act, iact, pMean1, pMean2, pStd1, pStd2 = [],[],[],[],[],[],[]
    #for i in range(Nvbin):
        #acf.append(sampler[i].acceptance_fraction.mean())
        ##act.append(sampler[i].acor.mean())
        #act.append(sampler[i].get_autocorr_time(tol=0).mean())
        #iact.append(emcee.autocorr.integrated_time(sampler[i].flatchain))
        #pMean1.append(np.mean(sampler[i].chain[:,-1,:],axis=0)) # Accross walkers
        #pMean2.append(np.mean(sampler[i].chain[-1,:,:],axis=0)) # Accross samples
        #pStd1.append(np.std(sampler[i].chain[:,-1,:],axis=0))
        #pStd2.append(np.std(sampler[i].chain[-1,:,:],axis=0))

    return sampler


def loadMCMC(filename, Nburn, Nthin, Nmarg=4., Nvbin=2, vbin='zv', outPath='results/'):
    """Load previous MCMC run from file, remove burn-in and apply thinning.

    Args:
        filename (str): name of input file for emcee chains
        Nburn (float): initial burn-in steps of chain to discard, in units of auto-correlation time
        Nthin (float): thinning factor of chain, in units of auto-correlation time
        Nmarg (float): Margin size for parameter limits in plots, in units of standard deviation (default = 4)
        Nvbin (int): number of void bins (default = 2)
        vbin (str): binning strategy, 'zv': void-redshift bins (default), 'rv': void-radius bins
        outPath (path): name of output path for chains (default = 'results/')

    Returns:
        samples (ndarray list,[Nvbin,Nchain,Npar]): MCMC samples after thinning and burn-in removal \n
        logP (ndarray list,[Nvbin,Nchain]): log likelihood values of chains \n
        pMean (ndarray list,[Nvbin,Npar]): mean parameter values \n
        pStd (ndarray list,[Nvbin,Npar]): standard deviation of parameters \n
        pErr (ndarray list,[Nvbin,Npar]): relative errors of parameters (pStd/pMean) \n
        pLim (ndarray list,[Nvbin,Npar,2]): limits for parameter margins around their mean value in plots (Nmarg*pStd on each side)
    """
    samples, act, logP, pMean, pStd, pErr, pLim = [],[],[],[],[],[],[]
    for i in range(Nvbin):
        reader = emcee.backends.HDFBackend(Path(outPath) / filename, name=vbin+str(i))
        act.append(reader.get_autocorr_time(tol=0).mean())
        samples.append(reader.get_chain(discard=int(Nburn*act[i]), thin=int(Nthin*act[i]), flat=True))
        #samples[i][:,1] /= samples[i][:,2] # AP parameter epsilon
        logP.append(reader.get_log_prob(discard=int(Nburn*act[i]), thin=int(Nthin*act[i]), flat=True))
        #chain = getdist.chains.WeightedSamples(samples=samples[i])
        #pLow.append([chain.confidence(j,0.15865,upper=False) for j in range(Npar)] - pMean[i])
        #pHigh.append([chain.confidence(j,0.15865,upper=True) for j in range(Npar)] - pMean[i])
        pMean.append(np.mean(samples[i],axis=0))
        pStd.append(np.std(samples[i],axis=0))
        #pStd.append(np.diff(np.percentile(samples[i], [15.865,50.,84.135], axis=0),axis=0))
        pErr.append(abs(pStd[i]/pMean[i]))
        pLim.append(np.array(list(zip(pMean[i]-Nmarg*pStd[i],pMean[i]+Nmarg*pStd[i]))))

    return samples, logP, pMean, pStd, pErr, pLim


def lnL_DAH(par_cosmo, prior_cosmo, z, DAH_fit, DAH_err):
    """Log likelihood for D_A(z)*H(z)/c.

    Args:
        par_cosmo (dict): cosmological parameter values
        prior_cosmo (dict): boundary values for uniform cosmological parameter priors
        z (ndarray,len(z)): redshifts
        DAH_fit (ndarray,len(z)): measured values of D_A(z)*H(z)/c
        DAH_err (ndarray,len(z)): measured errors of D_A(z)*H(z)/c

    Returns:
        lnL_DAH (float): Logarithm of the likelihood for D_A(z)*H(z)/c multiplied by the prior
    """
    DAH_model = partial(DAH, z)
    if np.isinf(lnP(par_cosmo,prior_cosmo)):
        return lnP(par_cosmo,prior_cosmo)
    else:
        lnL_DAH = -0.5*np.sum((DAH_fit-DAH_model(*par_cosmo))**2/DAH_err**2) + lnP(par_cosmo,prior_cosmo)
        return lnL_DAH


# def lnL_DA_DH(par_cosmo, prior_cosmo, z, DA_fit, DA_err, DH_fit, DH_err):
#     """Joint log likelihood for D_A(z) and D_H(z).

#     Args:
#         par_cosmo (dict): cosmological parameter values
#         prior_cosmo (dict): boundary values for uniform cosmological parameter priors
#         z (ndarray,len(z)): redshifts
#         DA_fit (ndarray,len(z)): measured values of D_A(z)
#         DA_err (ndarray,len(z)): measured errors of D_A(z)
#         DH_fit (ndarray,len(z)): measured values of D_H(z)
#         DH_err (ndarray,len(z)): measured errors of D_H(z)

#     Returns:
#         lnL_DA_DH (float): Logarithm of the joint likelihood for D_A(z) and D_H(z) multiplied by the prior
#     """
#     DA_model = partial(Da, z)
#     DH_model = partial(Dh, z)
#     if np.isinf(lnP(par_cosmo,prior_cosmo)):
#         return lnP(par_cosmo,prior_cosmo)
#     else:
#         lnL_DA_DH = -0.5*np.sum((DA_fit-DA_model(*par_cosmo))**2/DA_err**2) -0.5*np.sum((DH_fit-DH_model(*par_cosmo))**2/DH_err**2) + lnP(par_cosmo,prior_cosmo)
#         return lnL_DA_DH


def runMCMC_cosmo(z, par_cosmo, prior_cosmo, DAH_fit, DAH_err, Nwalk, Nchain, filename, cosmology='LCDM', outPath='results/'):
    """Monte Carlo Markov Chain sampler for D_A(z)*H(z)/c.

    Args:
        z (ndarray,len(z)): redshifts
        par_cosmo (dict): cosmological parameter values
        prior_cosmo (dict): boundary values for uniform cosmological parameter priors
        DAH_fit (ndarray,len(z)): measured values of D_A(z)*H(z)/c
        DAH_err (ndarray,len(z)): measured errors of D_A(z)*H(z)/c
        Nwalk (int): number of MCMC walkers
        Nchain (int): length of each MCMC chain
        filename (str): name of output file for chains
        cosmology (str): cosmological model to consider [either 'LCDM' (default), 'wCDM', or 'w0waCDM']
        outPath (path): name of output path for chains (default = 'results/')

    Returns:
        sampler (object): instance of EnsembleSampler class containing the chains for cosmological parameters
    """
    backend = emcee.backends.HDFBackend(Path(outPath) / filename, name=cosmology)
    if cosmology=='LCDM':
        p0 = [par_cosmo['Om']] # initial value
        pr = [prior_cosmo['Om']] # prior
    if cosmology=='wCDM':
        p0 = [par_cosmo['Om'],par_cosmo['w0']]
        pr = [prior_cosmo['Om'],prior_cosmo['w0']]
    if cosmology=='w0waCDM':
        p0 = [par_cosmo['Om'],par_cosmo['w0'],par_cosmo['wa']]
        pr = [prior_cosmo['Om'],prior_cosmo['w0'],prior_cosmo['wa']]
    Npar = len(p0)
    # Ball around fiducial cosmology as initial values, uniform-randomly distributed with maximum absolute error of 5%
    p1i = p0 + 0.1*(np.random.rand(Nwalk,Npar)-0.5)
    #pool = mp.Pool()
    sampler = emcee.EnsembleSampler(Nwalk, Npar, lnL_DAH, args=[pr, z, DAH_fit, DAH_err], backend=backend) #, pool=pool)
    pos, prob, state = sampler.run_mcmc(p1i, Nchain, progress=True)
    #pool.close(); pool.join()
    return sampler


# def runMCMC_cosmo2(z, par_cosmo, prior_cosmo, DA_fit, DA_err, DH_fit, DH_err, Nwalk, Nchain, filename, cosmology='LCDM', outPath='results/'):
#     """Monte Carlo Markov Chain sampler for D_A(z) and D_H(z).

#     Args:
#         z (ndarray,len(z)): redshifts
#         par_cosmo (dict): cosmological parameter values
#         prior_cosmo (dict): boundary values for uniform cosmological parameter priors
#         DA_fit (ndarray,len(z)): measured values of D_A(z)
#         DA_err (ndarray,len(z)): measured errors of D_A(z)
#         DH_fit (ndarray,len(z)): measured values of D_H(z)
#         DH_err (ndarray,len(z)): measured errors of D_H(z)
#         Nwalk (int): number of MCMC walkers
#         Nchain (int): length of each MCMC chain
#         filename (str): name of output file for chains
#         cosmology (str): cosmological model to consider [either 'LCDM' (default), 'wCDM', or 'w0waCDM']
#         outPath (path): name of output path for chains (default = 'results/')

#     Returns:
#         sampler (object): instance of EnsembleSampler class containing the chains for cosmological parameters
#     """
#     backend = emcee.backends.HDFBackend(Path(outPath) / filename, name=cosmology)
#     if cosmology=='LCDM':
#         p0 = [par_cosmo['Om']] # initial value
#         pr = [prior_cosmo['Om']] # prior
#     if cosmology=='wCDM':
#         p0 = [par_cosmo['Om'],par_cosmo['w0']]
#         pr = [prior_cosmo['Om'],prior_cosmo['w0']]
#     if cosmology=='w0waCDM':
#         p0 = [par_cosmo['Om'],par_cosmo['w0'],par_cosmo['wa']]
#         pr = [prior_cosmo['Om'],prior_cosmo['w0'],prior_cosmo['wa']]
#     Npar = len(p0)
#     # Ball around fiducial cosmology as initial values, uniform-randomly distributed with maximum absolute error of 5%
#     p1i = p0 + 0.1*(np.random.rand(Nwalk,Npar)-0.5)
#     #pool = mp.Pool()
#     sampler = emcee.EnsembleSampler(Nwalk, Npar, lnL_DA_DH, args=[pr, z, DA_fit, DA_err, DH_fit, DH_err], backend=backend) #, pool=pool)
#     pos, prob, state = sampler.run_mcmc(p1i, Nchain, progress=True)
#     #pool.close(); pool.join()
#     return sampler


def loadMCMC_cosmo(filename, cosmology, Nburn, Nthin, Nmarg=4., blind=True, outPath='results/'):
    """Load previous MCMC run for D_A(z)*H(z)/c from file, remove burn-in and apply thinning.

    Args:
        filename (str): name of input file for emcee chains
        cosmology (str): cosmological model to consider [either 'LCDM' (default), 'wCDM', or 'w0waCDM']
        Nburn (float): initial burn-in steps of chain to discard, in units of auto-correlation time
        Nthin (float): thinning factor of chain, in units of auto-correlation time
        Nmarg (float): Margin size for parameter limits in plots, in units of standard deviation (default = 4)
        blind (bool): If true, subtract mean from chains (default = True)
        outPath (path): name of output path for chains (default = 'results/')

    Returns:
        samples (ndarray,[Nchain,Npar]): MCMC chain after thinning and burn-in removal \n
        logP (ndarray,Nchain): log likelihood values of chain \n
        pMean (ndarray,Npar): mean parameter values \n
        pStd (ndarray,Npar): standard deviation of parameters \n
        pErr (ndarray,Npar): relative errors of parameters (pStd/pMean) \n
        pLim (ndarray,[Npar,2]): limits for parameter margins around their mean value in plots (Nmarg*pStd on each side)
    """
    reader = emcee.backends.HDFBackend(Path(outPath) / filename, name=cosmology)
    act = reader.get_autocorr_time(tol=0).mean()
    samples = reader.get_chain(discard=int(Nburn*act), thin=int(Nthin*act), flat=True)
    logP = reader.get_log_prob(discard=int(Nburn*act), thin=int(Nthin*act), flat=True)
    chi2 = -logP.max()
    pBest = samples[np.argmax(logP)]
    pMean = np.mean(samples,axis=0)
    pStd = np.std(samples,axis=0)
    pErr = abs(pStd/pMean)
    if blind:
        samples -= pMean
        pMean -= pMean
    pLim = np.array(list(zip(pMean-Nmarg*pStd,pMean+Nmarg*pStd)))
    return samples, logP, pBest, pMean, pStd, pErr, pLim



############################
##### Theory functions #####
############################

@np.vectorize
def DH(z, par_cosmo):
    """Hubble distance D_H(z) = c/H(z) in units of Mpc/h in flat LCDM.

    Args:
        z (ndarray,len(z)): redshifts
        par_cosmo (dict): cosmological parameter values

    Returns:
        DH (ndarray,len(z)): Hubble distance D_H(z) = c/H(z)
    """
    DH = c/(100*np.sqrt(par_cosmo['Om']*(1.+z)**3 + 1. - par_cosmo['Om']))
    return DH


@np.vectorize
def DA(z, par_cosmo):
    """Comoving angular diameter distance D_A(z) in units of Mpc/h in flat LCDM.

    Args:
        z (ndarray,len(z)): redshifts
        par_cosmo (dict): cosmological parameter values

    Returns:
        DA (ndarray,len(z)): Comoving angular diameter distance D_A(z)
    """
    DA = integrate.quad(DH, 0., z, args=(par_cosmo))[0]
    return DA


def DA0(z, par_cosmo):
    """Comoving angular diameter distance D_A(z) in units of Mpc/h in flat LCDM (fast from astropy).

    Args:
        z (ndarray,len(z)): redshifts
        par_cosmo (dict): cosmological parameter values

    Returns:
        DA0 (ndarray,len(z)): Comoving angular diameter distance D_A(z)
    """
    DA0 = np.array(FlatLambdaCDM(H0=100., Om0=par_cosmo['Om']).comoving_distance(z))
    return DA0


def DAH(z, Om=0.3, w0=-1., wa=0., Ok=0.):
    """D_A(z)*H(z)/c in flat or curved w0waCDM.

    Args:
        z (ndarray,len(z)): redshifts
        Om (float): matter density parameter (default = 0.3)
        w0 (float): equation-of-state parameter w_0 (default = -1.)
        wa (float): equation-of-state parameter w_a (default = 0.)
        Ok (float): curvature parameter Omega_k (default = 0.)

    Returns:
        DAH (ndarray,len(z)): D_A(z)*H(z)/c
    """
    def Dh(z, Om, Ok, w0, wa): # Hubble distance
        return c/100/abs(Om*(1+z)**3 + Ok*(1+z)**2 + (1-Om-Ok)*(1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z)))**0.5

    def Da(z, Om, Ok, w0, wa): # Comoving angular diameter distance
        Dc = integrate.quad(Dh, 0., z, args=(Om,Ok,w0,wa))[0] # Comoving distance
        if   (Ok==0.): return Dc
        elif (Ok<0.):  return c/100/(-Ok)**0.5*np.sin(100/c*(-Ok)**0.5*Dc)
        elif (Ok>0.):  return c/100/Ok**0.5*np.sinh(100/c*Ok**0.5*Dc)
    
    return Da(z, Om, Ok, w0, wa)/Dh(z, Om, Ok, w0, wa)

DAH = np.vectorize(DAH, excluded=(1,2,3,4))


# def Dh(z, Om=0.3, w0=-1., wa=0., Ok=0.): # Hubble distance
#     return c/100/abs(Om*(1+z)**3 + Ok*(1+z)**2 + (1-Om-Ok)*(1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z)))**0.5

# Dh = np.vectorize(Dh, excluded=(1,2,3,4))

# def Da(z, Om=0.3, w0=-1., wa=0., Ok=0.): # Comoving angular diameter distance
#     Dc = integrate.quad(Dh, 0., z, args=(Om,Ok,w0,wa))[0] # Comoving distance
#     if   (Ok==0.): return Dc
#     elif (Ok<0.):  return c/100/(-Ok)**0.5*np.sin(100/c*(-Ok)**0.5*Dc)
#     elif (Ok>0.):  return c/100/Ok**0.5*np.sinh(100/c*Ok**0.5*Dc)

# Da = np.vectorize(Da, excluded=(1,2,3,4))


def Omz(z, par_cosmo):
    """Omega_m(z) in flat LCDM.

    Args:
        z (ndarray,len(z)): redshifts
        par_cosmo (dict): cosmological parameter values

    Returns:
        Omz (ndarray,len(z)): Omega_m(z)
    """
    Omz = par_cosmo['Om']*(1+z)**3*(DH(z, par_cosmo)*100/c)**2
    return Omz


@np.vectorize
def Dz(z, par_cosmo):
    """Growth factor D(z) in flat LCDM, normalized to 1 at z = 0.

    Args:
        z (ndarray,len(z)): redshifts
        par_cosmo (dict): cosmological parameter values

    Returns:
        Dz (ndarray,len(z)): Growth factor D(z)/D(0)
    """
    def intgrd(a): return (DH(1/a-1., par_cosmo)/a)**3
    def D(z): return 5./2.*Omz(z, par_cosmo)/(1+z)**3/DH(z, par_cosmo)**3 * integrate.quad(intgrd, 0., 1./(1.+z))[0]
    Dz = D(z)/D(0.)
    return Dz


def fz(z, par_cosmo):
    """Linear growth rate f(z) in flat LCDM.

    Args:
        z (ndarray,len(z)): redshifts
        par_cosmo (dict): cosmological parameter values

    Returns:
        fz (ndarray,len(z)): Linear growth rate f(z)
    """
    fz = Omz(z, par_cosmo)**0.55
    return fz


def bz(z, par_cosmo):
    """Linear bias b(z) of tracers, assuming simple inverse growth factor scaling.

    Args:
        z (ndarray,len(z)): redshifts
        par_cosmo (dict): cosmological parameter values

    Returns:
        bz (ndarray,len(z)): linear bias b(z)
    """
    bz = par_cosmo['b0']/Dz(z, par_cosmo)
    return bz


def f_b_z(z, par_cosmo):
    """RSD parameter f(z)/b(z) of tracers.

    Args:
        z (ndarray,len(z)): redshifts
        par_cosmo (dict): cosmological parameter values

    Returns:
        fz(z)/bz(z) (ndarray,len(z)): RSD parameter f(z)/b(z)
    """
    return fz(z, par_cosmo)/bz(z, par_cosmo)


def Hz(z, par_cosmo):
    """Hubble rate H(z) in units of km/s/Mpc.

    Args:
        z (ndarray,len(z)): redshifts
        par_cosmo (dict): cosmological parameter values

    Returns:
        Hz (ndarray,len(z)): Hubble rate H(z)
    """
    Hz = c*par_cosmo['h']/DH(z, par_cosmo)
    return Hz


def rho_c(z, par_cosmo):
    """Critical density rho_c(z) in units of (Msol/h)/(Mpc/h)^3.

    Args:
        z (ndarray,len(z)): redshifts
        par_cosmo (dict): cosmological parameter values

    Returns:
        rho_c (ndarray,len(z)): critical density rho_c(z)
    """
    rho_c = 3*Hz(z, par_cosmo)**2/(8*np.pi*G_Newton) * 1e9/par_cosmo['h']**2*KgMsol/KmMpc
    return rho_c


def HSW(r, r_s=1., d_c=-0.8, a=2., b=8.):
    """HSW void density profile (arXiv:1403.5499).

    Args:
        r (ndarray,len(r)): radial distances from void center in units of void radius
        r_s (float): scale radius in units of void radius (default = 1)
        d_c (float): central underdensity (default = -0.8)
        a (float): power-law index alpha (default = 2)
        b (float): power-law index beta (default = 8)

    Returns:
        delta_HSW (ndarray,len(r)): HSW void density profile
    """
    delta_HSW = d_c*(1. - (r/r_s)**a)/(1. + r**b)
    return delta_HSW


def xi_model(ell, rm, rd, d, D, f=0.5, qper=1., qpar=1., M=1., Q=1.):
    """Model for void-tracer correlation function (either POS vs. LOS or multipoles).

    Args:
        ell (int list): multipole orders to calculate, POS vs. LOS 2d correlation if ell = None
        rm (ndarray,len(rm)): radial distances from void center to calculate
        rd (ndarray,len(rd)): radial distances from void center for model void density profile
        d (ndarray,len(rd)): model void density profile
        D (ndarray,len(rd)): radially averaged model void density profile
        f (float): linear growth rate (default = 0.5)
        qper (float): AP distortion perpendicular to the LOS (default = 1)
        qpar (float): AP distortion parallel to the LOS (default = 1)
        M (float): monopole amplitude parameter (default = 1)
        Q (float): quadrupole amplitude parameter (default = 1)

    Returns:
        xi2d (ndarray,[len(rm),len(rm)]): model for POS vs. LOS 2d void-tracer correlation function if ell is None \n
        xi (ndarray,[len(ell),len(rm)]): model for multipoles of void-tracer correlation function if ell is not None
    """
    # M,Q = 1.,1. # Calibration (optional)

    def model(mus, s, l, Nit=5):
        # Redshift-space coordinates
        sper = s*(1.-mus**2)**0.5 *qper # AP correction along POS
        spar = s*mus *qpar # AP correction along LOS
        s = np.sqrt(sper**2 + spar**2)
        Ds = np.interp(s, rd, D)
        # Real-space coordinates via iteration (arXiv:2007.07895)
        for _ in range(Nit):
            rpar = spar/(1. - f/3.*M*Ds) # RSD correction
            r = np.sqrt(sper**2 + rpar**2)
            Ds = np.interp(r, rd, D)
        mu = rpar/r
        dr = np.interp(r, rd, d)
        Dr = np.interp(r, rd, D)
        xi2d = M*(dr + f*Dr + 2*Q*f*(dr-Dr)*mu**2) # (arXiv:2108.10347)
        return xi2d if l==None else (2*l+1.)/2*legendre(l)(mus)*xi2d

    if ell==None: # POS vs. LOS 2d correlation function
        smper = rm[rm > 0.]
        xi2d = np.zeros((len(smper),len(rm)))
        for (i,smpar) in enumerate(rm):
            sm = np.sqrt(smper**2 + smpar**2)
            musm = smpar/sm
            xi2d[:,i] = model(musm, sm, ell)
    else: # Multipoles
        musm = np.linspace(-1.,1.,len(rd))
        xi = np.zeros((len(ell),len(rd)))
        for (l,ll) in enumerate(ell):
            for i in range(len(rd)):
                xi[l,i] = integrate.trapz(model(musm, rd[i], ll), x=musm)
        xi = interpolate.interp1d(rd, xi) #, fill_value='extrapolate')

    return xi2d if ell==None else xi(rm)
