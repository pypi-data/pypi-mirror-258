"""
This file is part of tweezepy.py
"""

from autograd import hessian
from autograd.scipy.stats import gamma
from inspect import signature
from scipy.optimize import minimize
from scipy import stats

import autograd.numpy as np

class MCMC:
    """
    Monte Carlo sampler class.

    Parameters
    ----------
    walkers : int, optional
        Number of walkers, by default 32
    steps : int, optional
        Number of steps, by default 1600
    progress : bool, optional
        Print progress bar, by default True
    """
    def __init__(self, walkers = 32, steps = 1600, progress = True,**kwargs):
        try:
            import emcee
        except ImportError:
            RuntimeError("Monte Carlo sampling requires the emcee package.")
        self.walkers = walkers
        self.steps = steps

        scale = np.power(10,np.floor(np.log10(self.params)))
        pos = self.params + 1e-4 * np.random.randn(walkers,self.nparams) * scale
        nwalkers,ndims = pos.shape
        self.sampler = emcee.EnsembleSampler(nwalkers,ndims,self.logL,**kwargs)
        self.sampler.run_mcmc(pos, steps,progress = progress)
        self.samples = self.sampler.get_chain()
        self.autocorr_time = self.sampler.get_autocorr_time()

    def sample_plot(self,
                    fig=None,
                    labels = [],
                    fig_kwgs={},
                    ax_kwgs={}):
        """
        Plot the accepted Monte Carlo samples.

        Parameters
        ----------
        fig : object, optional
            Figure object, by default None
        labels : list, optional
            Plot labels, by default []
        fig_kwgs : dict, optional
            Figure keywords, by default {}
        ax_kwgs : dict, optional
            Axes keywords, by default {}

        Returns
        -------
        fig : Figure
            Figure object.
        axes : Axes
            Axes object.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise RuntimeError("Matplotlib is required for plotting.")
        if not isinstance(fig, plt.Figure):
            fig = plt.figure(figsize = (10,3*self.nparams),**fig_kwgs)
        axes = fig.get_axes()
        gs = plt.GridSpec(nrows=self.nparams,ncols =1)
        if len(labels) == 0:
            labels = self.names
        if len(axes) == 0:
            for i in range(self.nparams):
                axes.append(fig.add_subplot(gs[i]))
        for i,p in enumerate(labels):
            ax = axes[i]
            ax.plot(self.samples[:, :, i], c="k", alpha=0.3,**ax_kwgs)
            ax.axvline(2*self.autocorr_time[i],c="k",lw=2)
            ax.set_xlim(0, len(self.samples))
            ax.set_ylabel(p)
            ax.yaxis.set_label_coords(-0.1, 0.5)
            ax.ticklabel_format(axis='y',style='sci',scilimits=(0,0))
        axes[-1].set_xlabel("step number")
        return fig, axes

    def calc_mc_errors(self, percentiles = [15.87,50,84.13], discard = None, thin = None):
        """
        Computes percentiles from Monte Carlo samples.

        Parameters
        ----------
        percentiles : list, optional
            Percentiles for each parameter, by default [15.87,50,84.13]
        discard : int, optional
            Number of "burn-in" steps to discard, by default 100
        thin : int, optional
            N, by default 10
        
        Return
        ------
        errors : array
            Errors from Monte Carlo sampling.
        """
        tau = max(self.autocorr_time)

        if not discard:
            discard = np.ceil(2*tau)
        if not thin:
            thin = np.ceil(tau/2)
        if discard < 2*tau:
            raise RuntimeError('discard should be greater than twice the autocorrelation time %s.'%self.autocorr_time)
        if thin < tau%2:
            raise RuntimeError('thin should be greater than half the autocorrelation time %s.'%self.autocorr_time)
        self.flat_samples = self.sampler.get_chain(discard=discard,thin = thin,flat = True)
        return np.percentile(self.flat_samples,percentiles,axis=0).T

    def corner_plot(self,
                    quantiles = [0.16,0.84],
                    labels = None,
                    **kwargs):
        """
        Utility function for generating corner plots.

        Parameters
        ----------
        quantiles : list, optional
            Quantiles to annotate, by default (0.16,0.84)
        labels : list, optional
            Parameter labels, by default None

        Returns
        -------
        fig : Figure
            Figure object.
        axes : Axes
            Axes object.
        """
        try:
            import corner
        except ImportError:
            raise RuntimeError("Corner plot requires the corner module.")
        if not labels:
            labels = self.names
        fig = corner.corner(self.flat_samples,  
                            truths=self.params,
                            quantiles=quantiles,
                            #levels=(1-np.exp(-0.5),),
                            #title_fmt = '.2e',
                            #show_titles = True,
                            labels = labels,
                            title_kwargs={'fontdict':{'fontsize':12}},
                            **kwargs)
        ax = fig.get_axes()
        for a in ax:
            if a.get_xlabel():
                a.ticklabel_format(axis='x',style='sci',scilimits=(0,0),useMathText=True)
                t = a.get_xaxis().get_offset_text()
                t.set_position((1.1,.25))
                #t.set_xposition((-.5,0.9))
                #a.ticklabel_format()
            if a.get_ylabel():
                a.ticklabel_format(axis='y',style='sci',scilimits=(0,0),useMathText=True)
                t = a.get_yaxis().get_offset_text()
                t.set_position((-.3,0.9))
        return fig,ax
        
class MLEfit(MCMC):
    """
    Perform maximum likelihood estimation and uncertainty calculations.

    Parameters
    ----------
    pedantic : bool, optional
        Ignore unhelpful warnings,
        by default True
    scale_covar : bool, optional
        Whether to scale standard errors by reduced chi-squared,
        by default False
    fit_kwargs : dict, optional
        Disctionary of keyword arguments passed to scipy.optimize.minimize, 
        by default {}.
    
    Attributes
    ----------
    names : list
        Fit function parameter names.
    params : array
        Parameter values.
    std_errors : array
        Parameter uncertainties.
    chi2 : float
        Chi-squared value.
    redchi2 : float
        Reduced chi-squared value.
    AIC : float 
        Akaike information criterion. 
    AICc : float 
        Corrected Akaike information criterion. 
    """
    def __init__(self, pedantic = True, scale_covar = False, minimizer_kwargs = {}):
        if pedantic == False:
            np.seterr('warn')
        elif pedantic == True:
            np.seterr('ignore')
        # Fancy way of determining fit param names        
        names = signature(self.func).parameters # inspect fit function parameters
        self.names = list(names.keys()) # make list of parameter names
        # Data
        shape = self.data['shape']
        y = self.data['y']
        yerr = self.data['yerr']
        self.ndata = len(y)
        # Log likelihood
        self.gd = Gamma_Distribution(shape,y)
        self.logL = lambda p: self.gd.logpdf(self.func(*p)).sum()
        # Negative log likelihood
        self.negLL =  lambda p: -self.logL(p)
        # Use automatic differentiation to calculate hessian
        hess = hessian(self.negLL)
        # Minimize negative log likelihood
        self.fit = minimize(self.negLL,x0=self.guess,method = 'Nelder-Mead',**minimizer_kwargs)
        # Save minimizer fit results
        self.params = self.fit['x']
        self.nparams = len(self.fit['x'])
        self.success = self.fit['success']
        # Collect results into dictionary
        results = {}
        # Throw warning if fit fails
        if not self.success:
            print('MLE fitting failed to converge. %s'%self.fit['message'])
            #self.params = np.array([float('nan') for i in range(self.nparams)])
            #self.std_errors = np.array([float('nan') for i in range(self.nparams)])
        # Compute standard errors by inverting the Hessian
        inv_hessian = np.linalg.inv(hess(self.params))
        # Covariance matrix
        self.cov = 2. * inv_hessian
        # Calculate errors from diagonals of covariance matrix
        self.std_errors = np.sqrt(np.diag(self.cov))
        # Calculate fit values
        yfit = self.func(*self.params); 
        self.fit_data = self.data.copy()
        self.data['yfit'] = yfit
        # Calculate residuals, chi2, and reduced chi2
        residuals = (y-yfit)/yerr; self.residuals = residuals
        self.data['residuals'] = residuals
        self.chi2 = np.power(residuals,2).sum(); results['chi2'] = self.chi2
        self.nfree = self.ndata-self.nparams
        self.redchi2 = self.chi2/self.nfree; results['redchi2'] = self.redchi2
        # Scale errors by reduched chi-squared value
        if scale_covar:
            self.std_errors *= self.redchi2
        # Collect errors into results
        for i,p in enumerate(self.names):
            results['%s'%p] = self.params[i]
            results['%s_error'%p] = self.std_errors[i]
        # Calculate fit support and p-value
        ks = stats.kstest(residuals,'chi2',args=(self.nfree,))
        self.support,self.p = ks
        results['support'] = self.support
        results['p-value'] = self.p
        
        # Calculate loglikelihood
        self.loglikelihood = self.logL(self.params)
        # Calculate AIC, AICc, and BIC
        self.AIC = 2.*(self.nparams-self.loglikelihood); results['AIC'] = self.AIC
        self.AICc = self.AIC + (2*(pow(self.nparams,2)+self.nparams))/(self.ndata-self.nparams-1) ; results['AICc'] = self.AICc
        # Save results into private attribute
        self._results = results

    def mcmc(self, walkers = 32, steps = 2000, discard = 100, thin = 10):
        """
        Runs Monte Carlo sampler and computes standard errors as 0.5*(std_u - std_l)

        Parameters
        ----------
        walkers : int, optional
            Number of walkers, by default 32
        steps : int, optional
            Number of steps to take, by default 2000
        discard : int, optional
            Number of initial steps to discard, by default 100
        thin : int, optional
            Distance between independent steps, by default 10
        """
        MCMC.__init__(self,walkers=walkers,steps=steps)
        percentiles = self.calc_mc_errors(percentiles = [15.87,50,84.13],discard=discard,thin=thin)
        self.mcmc_params = np.zeros(self.nparams)
        self.mcmc_std_errors = np.zeros(self.nparams)
        for i,name in enumerate(self.names):
            std_l, median, std_u = percentiles[i]
            self.mcmc_params[i] = median
            self._results['%s_mcmc'%name] = median
            std_error = 0.5 * (std_u - std_l)
            self.mcmc_std_errors[i] = std_error
            self._results['%s_mcmc_error'%name] = 0.5 * (std_u - std_l)
    @property
    def results(self):
        """
        Dictionary of MLE fit results.

        Returns
        -------
        dict
            Dictionary of MLE fit results.
        """
        return self._results

class Gamma_Distribution:
    """Gamma probability distribution class.

    Parameters
    ----------
    shape : np.array
        Shape parameter.
    yhat : np.array
        Experimental values. 
    
    Attributes
    ----------
    shape : array-like
        Shape parameters.
    yhat : array-like
        Experimnetal values
    """
    def __init__(self,shape,yhat):
        self.yhat = yhat
        self.shape = shape
    def scale(self,ytrue):
        """ Calculate scale parameters.
        
        Parameters
        ----------
        ytrue : array-like
            True/theoretical values.

        Returns
        -------
        scale : array-like
            Scale parameters.
        """
        return ytrue/self.shape 
    def std(self,ytrue):
        """ Calculate standard deviation.

        Parameters
        ----------
        ytrue : array-like
            True/theoretical values.

        Returns
        -------
        std : array-like
            Standard deviations.
        """
        scale = self.scale(ytrue)
        return stats.gamma.std(self.shape, scale = scale)
    def pdf(self,ytrue):
        """ Calculate probability distribution function.

        Parameters
        ----------
        ytrue : array-like
            True/theoretical values.

        Returns
        -------
        pdf : callable
            Probability distribution function.
        """
        scale = self.scale(ytrue)
        return gamma.pdf(self.yhat/scale,self.shape)/scale
    def logpdf(self,ytrue):
        """ Log of the probability distribution function.

        Parameters
        ----------
        ytrue : array-like
            True/theoretical values.

        Returns
        -------
        logpdf : callable
            Log of the probability distribution function.
        """
        scale = self.scale(ytrue)
        return gamma.logpdf(self.yhat/scale,self.shape) - np.log(scale)
    def cdf(self,ytrue):
        """ Cumulative distribution function.

        Parameters
        ----------
        ytrue : array-like
            True/theoretical values.

        Returns
        -------
        cdf : callable
            Cumulative distribution function.
        """
        scale = self.scale(ytrue)
        return stats.gamma.cdf(self.yhat,self.shape,scale=scale)
    def logcdf(self, ytrue):
        """ Log of cumulative distribution function.

        Parameters
        ----------
        ytrue : array-like
            True/theoretical values.

        Returns
        -------
        logcdf : callable
            Log of cumulative distribution function.
        """
        scale = self.scale(ytrue)
        return gamma.logcdf(self.yhat,self.shape,scale = scale)
    def interval(self,ytrue,alpha = 0.95):
        """

        Parameters
        ----------
        ytrue : array-like
            True/theoretical values.
        alpha : float, optional
            Probability that a random variable will be drawn from the returned range. Each value should be in the range [0, 1]., by default 0.95

        Returns
        -------
        Interval : callable
            Endpoints of the range that contains fraction alpha [0, 1] of the distribution.
        """
        scale = self.scale(ytrue)
        return stats.gamma.interval(alpha,self.shape,scale = scale)