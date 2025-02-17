
__all__ = ("WCamTranslator", )

from astro_metadata_translator import cache_translation, FitsTranslator
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, Angle

class WCamTranslator(FitsTranslator):
    """Metadata translator for WCam FITS headers.

    Under normal circumstances, translators are found in the astro_metadata_translator repository. However, it is possible to also put them in an obs_package, provided that they are imported in both the _instrument.py and rawFormatter.py files.

    This one is in obs_wcam to keep everything togeter in one place.
    """

    """Name of this translation class"""
    name = "WCam"

    """Supports the Wcam instrument."""
    supported_instrument = "WCam"

    """
    _const_map includes properties that you may not know, nor can calculate.

    Bear in mind that some examples listed here as "None" may require units or be a specific class should you want to upgrade them to _trivial_map or to_<<example>>. For example, "altaz_begin" needs to be an astropy.coordinates.AltAz class.
    """
    _const_map = {"boresight_rotation_coord": "sky",
                  "detector_group": None,
                  "boresight_airmass": None, #This could be calculated.
                  "boresight_rotation_angle": Angle(90 * u.deg),
                  "science_program": None,
                  "temperature": 300. * u.K,
                  "pressure": 985. * u.hPa,
                  "relative_humidity": None,
                  "altaz_begin": None, #This could be calculated.
                  "location": None,
        }

    """
    _trivial_map includes properties that can be taken directly from header
    """
    _trivial_map = {
        "exposure_id": "RUN",
        "visit_id": "RUN",
        "observation_id": "RUN",
        "detector_exposure_id": "RUN",
        "detector_num": "DETECTOR",
        "detector_serial": "DETECTOR",
        "physical_filter": "FILTER",
        "exposure_time": ("EXPTIME", dict(unit=u.s)),
        "dark_time": ("EXPTIME", dict(unit=u.s)),
        "object": "OBJECT",
        "observation_type": "OBSTYPE",
        }

    @classmethod
    def can_translate(cls, header, filename=None):
        """
        butler ingest-raws cycles through the known translators, using this method to determine whether each one can translate supplied header.

        This example just checks the INSTRUME header keyword and returns True if it contains "WCAM". However, you can make this as stringent as you like (e.g., perhaps you can currently handle a limited range of filters)

        Parameters
        ----------
        header : `dict`-like
            Header to convert to standardized form.
        filename : `str`, optional
            Name of file being translated.
        Returns
        -------
        can : `bool`
            `True` if the header is recognized by this class. `False`
            otherwise.
        """

        # Use INSTRUME. Because of defaulting behavior only do this
        # if we really have an INSTRUME header
        if "INSTRUME" in header:
            if header["INSTRUME"] == "WCAM":
                return True
        return False

    """
    The to_<<example>> methods are used when properties can't be trivially taken from the header.

    For example, the date in the header needs to be converted into an astropy.Time class.
    """
    @cache_translation
    def to_datetime_begin(self):
        date = self._header["DATE-OBS"]
        date = [date[0:4], date[4:6], date[6:]]
        date = '-'.join(date)
        t = Time(date, format="iso", scale="utc")
        return t

    @cache_translation
    def to_datetime_end(self):
        datetime_end = self.to_datetime_begin() + self.to_exposure_time()
        return datetime_end

    @cache_translation
    def to_tracking_radec(self):
        radec = SkyCoord(self._header["RA2000"], self._header["DEC2000"],
                         frame="icrs", unit=(u.hourangle, u.deg))
        return radec

    @cache_translation
    def to_instrument(self):
        if self._header["INSTRUME"] == "WCAM":
            return "WCam"
        else:
            #It should never get here, given can_translate().
            return "Unknown"

    def to_telescope(self):
        return self.to_instrument()

    @cache_translation
    def to_detector_name(self):
        return '{:02d}'.format(self._header["DETECTOR"])
