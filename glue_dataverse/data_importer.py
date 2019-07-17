from glue.config import menubar_plugin
from glue.core.data_factories.helpers import load_data

from PyQt5.QtWidgets import QVBoxLayout, QMessageBox, QDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore


SUPPORTED_TYPES = ['application/fits']


class FileDownload:

    def __init__(self, obj, parent):
        self.obj = obj
        self.parent = parent

    def finished(self):
        self.parent.finished_download(self.obj.path())


class DataVerseImportDialog(QDialog):

    def __init__(self, data_collection=None):

        super(DataVerseImportDialog, self).__init__()

        self.downloads = []
        self.data_collection = data_collection

        self.web = QWebEngineView()
        self.web.setUrl(QtCore.QUrl('https://dataverse.harvard.edu'))
        self.web.page().profile().downloadRequested.connect(self.handle_download)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.web)
        self.layout.setContentsMargins(3, 3, 3, 3)

        self.setLayout(self.layout)

    def handle_download(self, event):

        mime_type = event.mimeType()

        if mime_type not in SUPPORTED_TYPES:
            QMessageBox.error('Glue does not support files of type {0}'.format(mime_type))
            return

        event.accept()

        dl = FileDownload(event, self)
        self.downloads.append(dl)

        event.finished.connect(dl.finished)

    def finished_download(self, path):
        self.data_collection.append(load_data(path))


@menubar_plugin("Import from Dataverse")
def menubar_plugin(session, data_collection):
    dv = DataVerseImportDialog(data_collection)
    dv.exec_()
