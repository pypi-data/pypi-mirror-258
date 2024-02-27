import argparse
from pathlib import Path
from collections import OrderedDict

class Voiager():
    """
    VOId dynAmics and Geometry ExploreR main class.
    
    Args:
        params (dict): dictionary of parameters from input file
    """
    
    @staticmethod
    def parseParamsFile():
        """
        Find and read parameter file from default or specified location

        Returns:
            parser (object): instance of ArgumentParser from argparse
        """
        path = Path.cwd() # top level code directory
        parser = argparse.ArgumentParser(prog='voiager', description='VOId dynAmics and Geometry ExploreR provides a framework to perform cosmological analyses using voids identified in large-scale structure survey data.')
        parser.add_argument('parameters',
                            nargs = '?',
                            type = argparse.FileType('r'),
                            default = str(path / 'voiager' / 'params.yaml'),
                            help = 'Path to location of parameter yaml file')
        parser.add_argument('--version', action='version', version=Voiager.__version__)
        return parser


    def __init__(self, params):

        path = Path.cwd()

        # Survey information
        self.survey = params['Info']['survey'] # Name of survey
        self.sample = params['Info']['sample'] # Name of tracer sample
        self.random = params['Info']['random'] # Name of random sample
        self.version = params['Info']['version'] # Version (suffix) of void catalog
        self.zmin,self.zmax = params['Info']['redshift'] # Redshift range
        self.sky = params['Info']['sky'] # Sky area in square degrees (full sky ~ 41253)
        self.cosmology = params['Info']['cosmology'] # Cosmological model to constrain (current options: "LCDM", "wCDM", "w0waCDM")

        # Input / output
        self.runExec = params['IO']['runExec'] # If True, run executable when called
        self.basePath = path / params['IO']['basePath'] # Location of the top level code directory
        self.tracerPath = self.basePath / params['IO']['tracerPath'] # Location of tracer catalogs
        self.voidPath = self.basePath / params['IO']['voidPath'] # Location of void catalogs
        self.outPath = self.basePath / params['IO']['outPath'] / self.survey / (self.sample + self.version) # Location to store output files
        self.plotPath = self.outPath / params['IO']['plotPath'] # Location to store plots
        self.inputFormat = params['IO']['inputFormat'] # Filetype for input tracer and random catalogs (supported types: https://docs.astropy.org/en/stable/io/unified.html)
        self.inputExtension = params['IO']['inputExtension'] # Filename extension for input tracer and random catalogs
        self.figFormat = params['IO']['figFormat'] # Format to save figures (e.g., pdf, png, jpg)
        self.columnNames = params['IO']['columnNames'] # Tracer and random catalog column headers for right ascension, declination, redshift (angles in degrees)
        self.stackFile = params['IO']['stackFile']+'.dat' # Filename for data of stacks
        self.chainFile = params['IO']['chainFile']+'.dat' # Filename for data of chains
        self.cosmoFile = params['IO']['chainFile']+'_'+self.cosmology+'.dat' # Filename for data of cosmology chains
        self.continueStack = params['IO']['continueStack'] # If True, continue using previous stacks. If False, delete old stacks.
        self.continueChain = params['IO']['continueChain'] # If True, continue sampling of previous chains. If False, delete old chains.

        # Void selection
        self.zvmin,self.zvmax = params['Selection']['zv'] # Void redshift range
        self.rvmin,self.rvmax = params['Selection']['rv'] # Void radius range
        self.mvmin,self.mvmax = params['Selection']['mv'] # Void mass range (number of tracers per void)
        self.dvmin,self.dvmax = params['Selection']['dv'] # Void core (minimum) density range
        self.Cvmin,self.Cvmax = params['Selection']['Cv'] # Void compensation range
        self.evmin,self.evmax = params['Selection']['ev'] # Void ellipticity range
        self.mgsmin,self.mgsmax = params['Selection']['mgs'] # Void radius range in units of mean galaxy separation (mgs)

        # Binning parameters
        self.vbin = params['Bins']['vbin'] # 'zv': void-redshift bins, 'rv': void-radius bins
        self.binning = params['Bins']['binning'] # 'eqn': equal number of voids, 'lin': linearly spaced, 'log': logarithmicly spaced. Alternatively, provide a list for custom bin edges
        self.Nvbin = params['Bins']['Nvbin'] # Number of void bins
        self.Nrbin = params['Bins']['Nrbin'] # Number of radial bins in correlation function
        self.Nrskip = params['Bins']['Nrskip'] # Number of radial bins to skip in fit (starting from the first bin)
        self.rmax = params['Bins']['rmax'] # Maximum radial distance in units of void radius
        self.ell = params['Bins']['ell'] # Multipole orders to consider
        self.Nside = params['Bins']['Nside'] # Mask resolution for generating random voids
        self.symLOS = params['Bins']['symLOS'] # If True, assume void-centric symmetry along LOS (no odd multipoles).
        self.project2d = params['Bins']['project2d'] # If True, the projected correlation function is calculated from the POS vs. LOS 2d correlation function
        self.rescov = params['Bins']['rescov'] # If True, calculate covariance matrix for residuals between data and model (experimental!)
        self.datavec = params['Bins']['datavec'] # Define data vector, '1d': multipoles, '2d': POS vs. LOS 2d correlation function

        # Computing parameters
        self.Ncpu = params['Computing']['Ncpu'] # Number of CPUs to use
        self.Nmock = params['Computing']['Nmock'] # Number of mock realizations (for observation = 1)
        self.Nbin_nz = params['Computing']['Nbin_nz'] # Number of bins for redshift distributions
        self.Nbin_nv = params['Computing']['Nbin_nv'] # Number of bins for void abundance function
        self.Nspline = params['Computing']['Nspline'] # Number of nodes for splines (only for visualization in plots, does not affect fit)
        self.Nsmooth = params['Computing']['Nsmooth'] # Smoothing factor for splines (for no smoothing = 0)
        self.Nwalk = params['Computing']['Nwalk'] # Number of MCMC walkers (ideally equal to Ncpu)
        self.Nchain = params['Computing']['Nchain'] # Length of each MCMC chain
        self.Nburn = params['Computing']['Nburn'] # Initial burn-in steps of chain to discard, in units of auto-correlation time
        self.Nthin = params['Computing']['Nthin'] # Thinning factor of chain, in units of auto-correlation time
        self.Nmarg = params['Computing']['Nmarg'] # Margin size for parameter limits in plots, in units of standard deviation

        # Model parameters with fiducial values and priors
        self.par = OrderedDict(params['Model']['par'])
        self.prior = OrderedDict(params['Model']['prior'])

        # Cosmological parameters with fiducial values and priors
        self.par_cosmo = params['Cosmo']['par_cosmo']
        self.prior_cosmo = params['Cosmo']['prior_cosmo']
        self.blind = params['Cosmo']['blind'] # If True, subtract mean of cosmology posterior