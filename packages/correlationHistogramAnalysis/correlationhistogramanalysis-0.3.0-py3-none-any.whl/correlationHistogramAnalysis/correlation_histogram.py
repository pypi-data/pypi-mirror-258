# -*- coding: utf-8 -*-
"""
Created on Mon June  19 14:09:39 2023

@author: Katnagallu
"""

import numpy as np
from ifes_apt_tc_data_modeling.epos.epos_reader import ReadEposFileFormat


def get_epos(file_name):
    epos_reader = ReadEposFileFormat(file_name)
    epos = np.zeros([epos_reader.number_of_events,11])
    epos[:,:3] = epos_reader.get_reconstructed_positions().values
    epos[:,3] = epos_reader.get_mass_to_charge_state_ratio().values[:,0]
    epos[:,4] = epos_reader.get_raw_time_of_flight().values[:,0]
    epos[:,5] =  epos_reader.get_standing_voltage().values[:,0]
    epos[:,6] = epos_reader.get_pulse_voltage().values[:,0]
    epos[:,7:9] = epos_reader.get_hit_positions().values
    epos[:,9] = epos_reader.get_number_of_pulses().values[:,0]
    epos[:,10] = epos_reader.get_ions_per_pulse().values[:,0]
    
    return epos


def fill_zeros_with_last(arr):
    """
    required for get_pairs(**args)

    Parameters
    ----------
    arr : array containing zeroes and floats.

    Returns
    -------
    array: fills zeroes in the array with the previous non-zero value.

    """
    prev = np.arange(len(arr))
    prev[arr == 0] = 0
    prev = np.maximum.accumulate(prev)
    return arr[prev]


def get_pairs(epos):
    """
    generates, pairs of mass-to-charge values for ipp>1.

    Parameters
    ----------
    epos : float-array epos.

    Returns
    -------
    m1 : float-array
        first of the mass-to-charge pairs,
        with multiplicity>1.
    m2 : float-array
        second of the mass-to-charge pairs,
        with multiplicity>1.
     dx,dy: x y detector coordinates


    """
    m = epos[:, 3]
    ipp = epos[:, 10]
    ipp_m = fill_zeros_with_last(ipp)
    m1 = np.repeat(m[ipp > 1], np.array(ipp[ipp > 1], dtype=int))
    m2 = m[ipp_m > 1]
    dx = epos[:, -4]
    dy = epos[:, -3]
    dx1 = np.repeat(dx[ipp > 1], np.array(ipp[ipp > 1], dtype=int))
    dx2 = dx[ipp_m > 1]
    new_dx1 = np.where(m1 > m2, dx2, dx1)
    new_dx2 = np.where(m1 > m2, dx1, dx2)
    dy1 = np.repeat(dy[ipp > 1], np.array(ipp[ipp > 1], dtype=int))
    dy2 = dy[ipp_m > 1]
    new_dy1 = np.where(m1 > m2, dy2, dy1)
    new_dy2 = np.where(m1 > m2, dy1, dy2)

    new_m1 = np.where(m1 > m2, m2, m1)
    new_m2 = np.where(m1 > m2, m1, m2)
    return new_m1, new_m2, new_dx1, new_dy1, new_dx2, new_dy2


def corr_his(m1, m2, nbins):
    """
    creates a histogram based on the mass-to-charge values m1 and m2, and number of bins
    Parameters
    ----------
    m1 : float
        mass-to-charge of the first daughter.
    m2 : float
        mass-to-charge value of the second daughter.
    nbins : int
        number of bins for histogram

    Returns
    -------
    histogram and edge values for m1 and m2.
    """
    m1edges = np.linspace(np.min(m1), np.max(m1), num=nbins)
    m2edges = np.linspace(np.min(m2), np.max(m2), num=nbins)
    h, _, _ = np.histogram2d(m1, m2, bins=(m1edges, m2edges))
    # Histogram does not follow Cartesian convention (see Notes),
    # therefore transpose H for visualization purposes.
    h = h.T
    return h, m1edges, m2edges


def diss_track(m1, m2, mp, interp_points=100):
    """
    To generate the dissociation tracks corresponding to
    the reaction mp-->m1+m2.

    Parameters
    ----------
    m1 : float
        mass-to-charge of the first daughter.
    m2 : float
        mass-to-charge value of the second daughter.
    mp : float
        mass-to-charge value of the parent ion.
    interp_points: int
        number of points to interpolate.

    Returns
    -------
    m1_d and m2_d the deficit mass-to-charge
    values of m1 and m2 respectively.

    """
    lamda = np.linspace(0, 1, interp_points)
    m1_d = m1 * (1 - (lamda * (1 - (m1 / mp)))) ** -1
    m2_d = m2 * (1 - (lamda * (1 - (m2 / mp)))) ** -1
    return m1_d, m2_d
