__all__ = ("WCAM_FILTER_DEFINITIONS",)

from lsst.obs.base import FilterDefinition, FilterDefinitionCollection

WCAM_FILTER_DEFINITIONS = FilterDefinitionCollection(
        FilterDefinition(
            physical_filter="Clear",
            band="Clear",
            alias={'Clear'}
            )
    )
