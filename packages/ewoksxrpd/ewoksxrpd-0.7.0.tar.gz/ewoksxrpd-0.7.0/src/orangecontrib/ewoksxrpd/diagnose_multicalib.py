import os
from AnyQt import QtWidgets
from AnyQt import QtGui

from ewoksxrpd.tasks.diagnostics import DiagnoseCalibrateMultiResults
from ewoksxrpd.gui.trigger_widget import OWTriggerWidget
from ewoksxrpd.gui.forms import input_parameters_diagnose_multicalib


__all__ = ["OWDiagnoseCalibrateMultiResults"]


class OWDiagnoseCalibrateMultiResults(
    OWTriggerWidget, ewokstaskclass=DiagnoseCalibrateMultiResults
):
    name = "DiagnoseCalibrateMultiResults"
    description = "Diagnose multi-distance calibration"
    icon = "icons/widget.png"
    want_main_area = True

    def _init_forms(self):
        parameter_info = input_parameters_diagnose_multicalib(
            self.get_default_input_values()
        )
        self._create_input_form(parameter_info)

    def _init_main_area(self):
        layout = self._get_main_layout()
        self._label = QtWidgets.QLabel()
        layout.addWidget(self._label)
        super()._init_main_area()

    def _refresh_non_form_output_widgets(self):
        with self._capture_errors():
            super()._refresh_non_form_output_widgets()
            self._update_output_file()

    def _update_output_file(self):
        inputs = self.get_task_input_values()
        filename = inputs.get("filename")
        if not filename or not os.path.isfile(filename):
            self._label.clear()
            return

        pixmap = QtGui.QPixmap(filename)
        self._label.setPixmap(pixmap)
