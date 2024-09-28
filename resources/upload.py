import json
import os.path
import traceback
from logging import exception

#
from flask import make_response, request
from flask_restful import Resource
from http import HTTPStatus
import pandas as pd
#
from constants.api_status import APIStatus
from constants.document import DocumentExtension, FileUpload
from global_utilities import llm_utilities
from resources.base_resource import BaseResource
from resources.exceptions import Exceptions



class Upload(Resource, BaseResource):
    def __init__(self):
        super().__init__()

    def do_processing(self, statements):
        result = []
        for statement in statements:
            data = {
                "statement": statement
            }
            score = llm_utilities.get_analysis(statement)
            data.update(score)
            result.append(data)

        return result

    def post(self):
        self.logger.info("Post the sheet(xlsx/csv) here ")

        try:
            data = self.__validate_request_post()
            df = pd.read_excel(data.get("file_path"))

            result = self.do_processing(df["Review"])

            response_payload = {
                "status": APIStatus.SUCCESS,
                "message": result
            }
            response = make_response(json.dumps(response_payload))
            response.status_code = HTTPStatus.OK

        except Exceptions as e:
            response_payload = {
                "status": e.status_code,
                "message": e.message
            }
            response = make_response(json.dumps(response_payload))
            response.status_code = e.status_code

        except Exception as e:
            error = f"Runtime error raised in POST Message Document API.\nException: {e}.\nTraceback:\n{traceback.format_exc()}"
            self.logger.error(error)
            response_payload = {
                "status": APIStatus.FAILURE,
                "message": "Internal Server Error. Please try again in some time."
            }
            response = make_response(json.dumps(response_payload))
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        response.mimetype = 'application/json'
        return response

    def __validate_request_post(self):
        self.logger.info("Attempting to validate request payload for POST API")

        try:
            request_payload = {
                "files": request.files
            }

            if not any(request_payload.values()):
                raise
        except Exception as e:
            error = "File is missing"
            self.logger.error(f"{error}\nException: {e}\nTraceback: {traceback.format_exc()}")
            raise Exceptions(
                status_code=HTTPStatus.BAD_REQUEST,
                message=error
            ) from e

        file = request.files.get("file")
        file_name = file.filename

        if '.' not in file_name:
            self.logger.error(f"Document format is invalid")
            raise Exceptions(
                status_code=HTTPStatus.BAD_REQUEST,
                message="Document must be either in xlsx or csv format"
            )

        extension = file_name.rsplit('.', 1)[1].lower()
        if extension not in DocumentExtension.VALID_DOCUMENT_EXTENSIONS:
            self.logger.error(f"Document format is invalid")
            raise Exceptions(
                status_code=HTTPStatus.BAD_REQUEST,
                message="Document must be either in xlsx or csv format"
            )

        file_path = os.path.join(FileUpload.FILE_UPLOAD_PATH, file_name)
        file.save(file_path)

        return {
            "file": file,
            "file_name": file_name,
            "extension": extension,
            "file_path": file_path
        }

    def get(self):

        response_payload = {
            "status": APIStatus.SUCCESS,
            "message": "/update API"
        }
        response = make_response(response_payload)
        response.status_code = HTTPStatus.OK
        response.mimetype = 'application/json'
        return response
