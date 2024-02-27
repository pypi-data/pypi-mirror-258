
"""
VOId dynAmics and Geometry ExploreR provides a framework to perform cosmological analyses using voids identified in large-scale structure survey data. The code measures dynamic and geometric shape distortions in void stacks and propagates those to constraints on cosmological parameters using Bayesian inference.
"""
from voiager.voiager import Voiager
from voiager.launch import launch
from voiager import datalib
from voiager import plotlib

__all__ = ['Voiager', 'launch', 'datalib', 'plotlib']
__version__ = "1.0.0"
__author__ = 'Nico Hamaus'

Voiager.__version__ = __version__
