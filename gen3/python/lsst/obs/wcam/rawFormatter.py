from lsst.obs.base import FitsRawFormatterBase
from ._instrument import WCam
from .wcamFilters import WCAM_FILTER_DEFINITIONS
# Comment-out the following line if you put .translators/necam.py in the 
# astro_metadata_translator repository: 
from .translators import WCamTranslator
# ...and uncomment the following:
# from astro_metadata_translator import NeCamTranslator

class WCamRawFormatter(FitsRawFormatterBase):
    """
    Gen3 Butler formatter for WCam raw data.
    """
    translatorClass = WCamTranslator
    filterDefinitions = WCAM_FILTER_DEFINITIONS

    def getDetector(self, id):
        return WCam().getCamera()[id]
