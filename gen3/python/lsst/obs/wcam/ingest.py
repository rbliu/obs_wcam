from lsst.obs.base.ingest import RawFileData
import lsst.obs.base
from ._instrument import WCam

class WCamRawIngestTask(lsst.obs.base.RawIngestTask):

    def extractMetadata(self, filename: str) -> RawFileData:

        datasets = []
        fitsData = lsst.afw.fits.Fits(filename.ospath, 'r')
        header = fitsData.readMetadata()
        datasets.append(self._calculate_dataset_info(header, filename))
        instrument = WCam()
        FormatterClass = instrument.getRawFormatter(datasets[0].dataId)

        return RawFileData(datasets=datasets, filename=filename,
                           FormatterClass=FormatterClass,
                           instrument=instrument)
