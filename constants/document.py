from typing import Final, List
#
from global_utilities import app

class DocumentExtension:
    XLSX: Final = "xlsx"
    CSV: Final = "csv"

    VALID_DOCUMENT_EXTENSIONS: List = [
        XLSX,
        CSV
    ]

class FileUpload:
    FILE_UPLOAD_PATH: Final = app.config["FILE_UPLOAD"]