# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Extend numpy's decorators to use nipy's gui and data labels.
"""

from numpy.testing.decorators import *

from nipy.utils import templates, example_data, DataError


def make_label_dec(label, ds=None):
    """Factory function to create a decorator that applies one or more labels.

    Parameters
    ----------
    label : str or sequence
        One or more labels that will be applied by the decorator to the
        functions it decorates.  Labels are attributes of the decorated function
        with their value set to True.
    ds : str
        An optional docstring for the resulting decorator.  If not given, a
        default docstring is auto-generated.

    Returns
    -------
    ldec : function
        A decorator.

    Examples
    --------
    >>> slow = make_label_dec('slow')
    >>> print slow.__doc__
    Labels a test as 'slow'

    >>> rare = make_label_dec(['slow','hard'],
    ... "Mix labels 'slow' and 'hard' for rare tests")
    >>> @rare
    ... def f(): pass
    ...
    >>>
    >>> f.slow
    True
    >>> f.hard
    True
    """
    if isinstance(label,basestring):
        labels = [label]
    else:
        labels = label
    # Validate that the given label(s) are OK for use in setattr() by doing a
    # dry run on a dummy function.
    tmp = lambda : None
    for label in labels:
        setattr(tmp,label,True)
    # This is the actual decorator we'll return
    def decor(f):
        for label in labels:
            setattr(f,label,True)
        return f
    # Apply the user's docstring
    if ds is None:
        ds = "Labels a test as %r" % label
        decor.__doc__ = ds
    return decor


# Nipy specific labels
gui = make_label_dec('gui')
data = make_label_dec('data')


# For tests that need further review
def needs_review(msg):
    """ Skip a test that needs further review.

    Parameters
    ----------
    msg : string
        msg regarding the review that needs to be done
    """
    def skip_func(func):
        return skipif(True, msg)(func)
    return skip_func


# Easier version of the numpy knownfailure
def knownfailure(f):
    return knownfailureif(True)(f)


def if_datasource(ds, msg):
    try:
        ds.get_filename()
    except DataError:
        return skipif(True, msg)
    return lambda f : f


def if_templates(f):
    return if_datasource(templates, 'Cannot find template data')(f)


def if_example_data(f):
    return if_datasource(example_data, 'Cannot find example data')(f)
