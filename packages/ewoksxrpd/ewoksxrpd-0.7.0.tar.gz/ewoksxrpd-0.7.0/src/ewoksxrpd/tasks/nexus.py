from contextlib import contextmanager

from ewokscore.missing_data import is_missing_data
import h5py
from silx.io.dictdump import dicttonx

from .utils import data_utils, pyfai_utils
from .data_access import TaskWithDataAccess

__all__ = ["SaveNexusPattern1D", "SaveNexusIntegrated"]


class _BaseSaveNexusIntegrated(
    TaskWithDataAccess,
    input_names=["url"],
    optional_input_names=[
        "bliss_scan_url",
        "metadata",
        "nxprocess_name",
        "nxmeasurement_name",
        "nxprocess_as_default",
        "external_url",
    ],
    output_names=["saved"],
    register=False,
):
    @property
    def _process_info(self):
        raise NotImplementedError

    @property
    def _nxprocess_name(self):
        if self.inputs.nxprocess_name:
            return self.inputs.nxprocess_name
        return "integrate"

    @property
    def _nxmeasurement_name(self):
        if self.inputs.nxmeasurement_name:
            return self.inputs.nxmeasurement_name
        return "integrated"

    @contextmanager
    def _save_context(self):
        master_url = self.inputs.url
        data_url = self.get_input_value("external_url", master_url)

        with self.open_h5item(data_url, mode="a", create=True) as data_parent:
            assert isinstance(data_parent, h5py.Group)
            with self.open_h5item(master_url, mode="a", create=True) as master_parent:
                assert isinstance(master_parent, h5py.Group)
                nxprocess = pyfai_utils.create_nxprocess(
                    master_parent, data_parent, self._nxprocess_name, self._process_info
                )

            yield nxprocess

            with self.open_h5item(master_url, mode="a", create=True) as master_parent:
                url = data_utils.data_from_storage(
                    self.inputs.bliss_scan_url, remove_numpy=True
                )
                if url:
                    self.link_bliss_scan(master_parent, url)
                mark_as_default = self.get_input_value("nxprocess_as_default", True)
                measurement = master_parent.require_group("measurement")
                measurement.attrs["NX_class"] = "NXcollection"
                pyfai_utils.create_nxprocess_links(
                    nxprocess,
                    measurement,
                    self._nxmeasurement_name,
                    mark_as_default=mark_as_default,
                )
                if self.inputs.metadata:
                    dicttonx(
                        self.inputs.metadata,
                        master_parent,
                        update_mode="add",
                        add_nx_class=True,
                    )
        self.outputs.saved = True


class SaveNexusPattern1D(
    _BaseSaveNexusIntegrated,
    input_names=["x", "y", "xunits"],
    optional_input_names=["header", "yerror"],
):
    """Save single diffractogram in HDF5/NeXus format"""

    def run(self):
        with self._save_context() as nxprocess:
            nxdata = pyfai_utils.create_nxdata(
                nxprocess,
                self.inputs.y.ndim,
                self.inputs.x,
                self.inputs.xunits,
                None,
                None,
            )
            nxdata.attrs["signal"] = "intensity"
            nxdata["intensity"] = self.inputs.y
            if not self.missing_inputs.yerror:
                nxdata["intensity_errors"] = self.inputs.yerror

    @property
    def _process_info(self):
        return self.inputs.header


class SaveNexusIntegrated(
    _BaseSaveNexusIntegrated,
    input_names=["radial", "intensity", "radial_units"],
    optional_input_names=["info", "azimuthal", "intensity_error", "azimuthal_units"],
):
    """Save 1D or 2D integration diffraction patterns in HDF5/NeXus format"""

    def run(self):
        with self._save_context() as nxprocess:
            # Fallback for old workflows that do not specify azimuthal_units but do have azimuthal data
            if is_missing_data(self.inputs.azimuthal_units) and not is_missing_data(
                self.inputs.azimuthal
            ):
                azimuthal_units = "chi_deg"
            else:
                azimuthal_units = self.inputs.azimuthal_units
            nxdata = pyfai_utils.create_nxdata(
                nxprocess,
                self.inputs.intensity.ndim,
                self.inputs.radial,
                self.inputs.radial_units,
                self.inputs.azimuthal,
                azimuthal_units,
            )
            nxdata.attrs["signal"] = "intensity"
            nxdata["intensity"] = self.inputs.intensity
            if not self.missing_inputs.intensity_error:
                nxdata["intensity_errors"] = self.inputs.intensity_error

    @property
    def _process_info(self):
        return self.inputs.info
