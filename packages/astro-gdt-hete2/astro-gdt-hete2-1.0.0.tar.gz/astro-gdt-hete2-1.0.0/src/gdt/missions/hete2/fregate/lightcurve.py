#  CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT
#  WITH UNLIMITED RIGHTS
#
#  Grant No.: 80NSSC21K0651
#  Grantee Name: Universities Space Research Association
#  Grantee Address: 425 3rd Street SW, Suite 950, Washington DC 20024
#
#  Copyright (c) 2024 by Universities Space Research Association (USRA). All rights reserved.
#
#  Developed by:
#       William Cleveland
#       Universities Space Research Association
#       Science and Technology Institute
#       https://sti.usra.edu
#
#  This work is a derivative of the Gamma-ray Data Tools (GDT), including the Core and Fermi packages, originally
#  developed by the following:
#
#       William Cleveland and Adam Goldstein
#       Universities Space Research Association
#       Science and Technology Institute
#       https://sti.usra.edu
#
#       Daniel Kocevski
#       National Aeronautics and Space Administration (NASA)
#       Marshall Space Flight Center
#       Astrophysics Branch (ST-12)
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
#   with the License. You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations under the License.
#  CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT
#  WITH UNLIMITED RIGHTS
#
#  Grant No.: 80NSSC21K0651
#  Grantee Name: Universities Space Research Association
#  Grantee Address: 425 3rd Street SW, Suite 950, Washington DC 20024
#
#  Copyright (c) 2024 by Universities Space Research Association (USRA). All rights reserved.
#
#  Developed by:
#       William Cleveland
#       Universities Space Research Association
#       Science and Technology Institute
#       https://sti.usra.edu
#
#  This work is a derivative of the Gamma-ray Data Tools (GDT), including the Core and Fermi packages, originally
#  developed by the following:
#
#       William Cleveland and Adam Goldstein
#       Universities Space Research Association
#       Science and Technology Institute
#       https://sti.usra.edu
#
#       Daniel Kocevski
#       National Aeronautics and Space Administration (NASA)
#       Marshall Space Flight Center
#       Astrophysics Branch (ST-12)
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
#   with the License. You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations under the License.
import warnings
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

import astropy.io.fits as fits
import numpy as np
from astropy.time import Time

from gdt.core.file import FitsFileContextManager
from gdt.core.phaii import Phaii
from gdt.core.data_primitives import Gti, TimeEnergyBins, TimeBins

from .detectors import FregateDetectors

__all__ = ['FregateLightCurve', 'FregatePhaii']


@dataclass
class FregateLightCurveData:
    tstart: np.ndarray
    counts: np.ndarray
    energy_bands: np.ndarray
    time_delta: float


class FregatePhaii(Phaii):
    """Subclass Phaii to provide default header definitions for the Phaii extracted
    from the light curve files."""

    def _build_hdulist(self):
        """create FITS and primary header"""
        hdulist = fits.HDUList()
        primary_hdu = fits.PrimaryHDU()
        hdulist.append(primary_hdu)

        """ create the ebounds extension"""
        ebounds_hdu = self._ebounds_table()
        hdulist.append(ebounds_hdu)

        """create the spectrum extension"""
        spectrum_hdu = self._spectrum_table()
        hdulist.append(spectrum_hdu)

        """ create the GTI extension"""
        gti_hdu = self._gti_table()
        hdulist.append(gti_hdu)

        return hdulist

    def _ebounds_table(self):
        chan_col = fits.Column(name='CHANNEL', format='1I',
                               array=np.arange(self.num_chans, dtype=int))
        emin_col = fits.Column(name='E_MIN', format='1E', unit='keV',
                               array=self.ebounds.low_edges())
        emax_col = fits.Column(name='E_MAX', format='1E', unit='keV',
                               array=self.ebounds.high_edges())

        hdu = fits.BinTableHDU.from_columns([chan_col, emin_col, emax_col])

        return hdu

    def _spectrum_table(self):
        tstart = np.copy(self.data.tstart)
        tstop = np.copy(self.data.tstop)
        if self.trigtime is not None:
            tstart += self.trigtime
            tstop += self.trigtime

        counts_col = fits.Column(name='COUNTS',
                                 format='{}I'.format(self.num_chans),
                                 bzero=32768, bscale=1, unit='count',
                                 array=self.data.counts)
        expos_col = fits.Column(name='EXPOSURE', format='1E', unit='s',
                                array=self.data.exposure)
        time_col = fits.Column(name='TIME', format='1D', unit='s',
                               bzero=self.trigtime, array=tstart)
        endtime_col = fits.Column(name='ENDTIME', format='1D', unit='s',
                                  bzero=self.trigtime, array=tstop)
        hdu = fits.BinTableHDU.from_columns([counts_col, expos_col,
                                             time_col, endtime_col])

        return hdu

    def _gti_table(self):
        tstart = np.array(self.gti.low_edges())
        tstop = np.array(self.gti.high_edges())

        start_col = fits.Column(name='START', format='1D', unit='s',
                                bzero=self.trigtime, array=tstart)
        stop_col = fits.Column(name='STOP', format='1D', unit='s',
                               bzero=self.trigtime, array=tstop)
        hdu = fits.BinTableHDU.from_columns([start_col, stop_col])

        return hdu


class FregateLightCurve(FitsFileContextManager):
    """FREGATE lightcurve file containing PHAII from multiple detectors.
    """

    def __init__(self):
        super().__init__()
        self._data: Dict[FregateDetectors, FregateLightCurveData] = {}
        self.time_zero: Optional[float] = None
        self._gti: Optional[Gti] = None

    def _data_from_hdu(self, hdu: fits.BinTableHDU):

        detector = FregateDetectors.from_full_name(hdu.header['INSTRUME'])

        # Retrieve the data from the HDU
        self._data[detector] = FregateLightCurveData(
            tstart=hdu.data['TIME'],  # Start time of each bin
            counts=hdu.data['RATE'],  # 2D array containing counts by energy band
            energy_bands=np.array(  # The energy bands defined in the light curve file
                [[hdu.header['E_MIN1'] if 'E_MIN1' in hdu.header else 8.0,
                  hdu.header['E_MIN2'] if 'E_MIN2' in hdu.header else 8.0,
                  hdu.header['E_MIN3'] if 'E_MIN3' in hdu.header else 32.0,
                  hdu.header['E_MIN4'] if 'E_MIN4' in hdu.header else 400.0],
                 [hdu.header['E_MAX1'] if 'E_MAX1' in hdu.header else 40.0,
                  hdu.header['E_MAX2'] if 'E_MAX2' in hdu.header else 70.0,
                  hdu.header['E_MAX3'] if 'E_MAX3' in hdu.header else 400.0,
                  hdu.header['E_MAX4'] if 'E_MAX4' in hdu.header else 1000.0]]).T,
            time_delta=hdu.header['TIMEDEL']  # The size of each bin in seconds
        )
        t0 = Time(hdu.header['TIMEZERO'], format='decimalyear').gps  # Time of the detection
        if self.time_zero is None:
            self.time_zero = t0
        elif self.time_zero != t0:
            warnings.warn(f'Time zero value for detector {detector} is different from previous read time zero')

    @property
    def detectors(self) -> List[FregateDetectors]:
        """(list): The detectors in the file"""
        return list(self._data.keys())

    @property
    def num_dets(self) -> int:
        """(int): Number of detectors in the file"""
        return len(self.detectors)

    @staticmethod
    def _detector_from_value(value: Union[str, int, FregateDetectors]) -> FregateDetectors:
        if isinstance(value, FregateDetectors):
            index = value
        elif isinstance(value, str):
            try:
                index = FregateDetectors.from_str(value)
            except ValueError:
                index = FregateDetectors.from_full_name(value)
        elif isinstance(value, int):
            index = FregateDetectors.from_num(value)
        else:
            raise TypeError('value must be a str, int, or FregateDetectors object')
        return index

    def energy_bands(self, detector: Union[FregateDetectors, str, int]):
        data = self._data[self._detector_from_value(detector)]
        return data.energy_bands

    def num_energy_bands(self, detector: Union[FregateDetectors, str, int]):
        return self.energy_bands(detector).shape[1]

    def time_bins(self, detector: Union[FregateDetectors, str, int], energy_band: int) -> TimeBins:
        data = self._data[self._detector_from_value(detector)]
        return TimeBins(counts=data.counts[:, energy_band], lo_edges=data.tstart,
                        hi_edges=data.tstart + data.time_delta, exposure=[data.time_delta] * data.counts.shape[0])

    def time_energy_bins(self, detector: Union[str, int, FregateDetectors], energy_band: int) -> TimeEnergyBins:
        """Retrieve the TimeEnergyBins object for the given detector.

        Args:
            detector (str, int, or :class:`FregateDetectors`)
            energy_band (int)

        Returns:
            (:class:`TimeEnergyBins`)
        """
        data = self._data[self._detector_from_value(detector)]
        return TimeEnergyBins(counts=data.counts[:, energy_band].reshape(-1, 1),
                              tstart=data.tstart, tstop=data.tstart + data.time_delta,
                              exposure=[data.time_delta] * data.counts.shape[0],
                              emin=data.energy_bands[energy_band, 0].reshape(-1, 1),
                              emax=data.energy_bands[energy_band, 1].reshape(-1, 1))

    def phaii(self, detector: Union[str, int, FregateDetectors], energy_band: int) -> Phaii:
        """Retrieve the Phaii object for the given detector.

        Args:
            detector (str, int, or :class:`FregateDetectors`)
            energy_band (int)

        Returns:
            (:class:`Phaii`)
        """
        data = self._data[self._detector_from_value(detector)]
        return FregatePhaii.from_data(self.time_energy_bins(detector, energy_band),
                                      gti=self._gti, trigger_time=self.time_zero)

    @property
    def gti(self) -> Gti:
        """Retrieve the GTI extension data.

        Returns:
            (:class:`Gti`)
        """
        return self._gti

    @classmethod
    def open(cls, file_path, **kwargs):
        """Open a FREGATE file containing PHA time series from multiple detectors.

        Args:
            file_path (str): The file path

        Returns:
            (:class:`FregateLightCurve`)
        """
        obj = super().open(file_path, **kwargs)

        # Populate the EnergyTimeBins
        for i in range(1, len(obj.hdulist) - 1):
            hdu = obj.hdulist[i]
            obj._data_from_hdu(hdu)

        # Retrieve the GTI
        data = obj.hdulist[-1].data
        obj._gti = Gti.from_bounds(data['START'], data['STOP'])
        obj.close()
        return obj

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.num_dets} detectors>'
