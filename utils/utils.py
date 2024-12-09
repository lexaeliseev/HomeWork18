import logging
import json
import allure
from requests import Response
from allure_commons.types import AttachmentType


def response_logging(response: Response):
    logging.info("Request: " + response.request.url)
    if response.request.body:
        logging.info("INFO Request body: " + response.request.body)  # логирование тела запроса если оно есть
    logging.info("Request headers: " + str(response.request.headers))
    logging.info("Response code " + str(response.status_code))
    logging.info("Response: " + response.text)


def response_attaching(response: Response):
    allure.attach(
        body=response.request.url,
        name="Request url",
        attachment_type=AttachmentType.TEXT,
    )

    if response.request.body:  # логирование тела запроса если оно есть
        try:
            request_body_json = json.loads(response.request.body)
            allure.attach(
                body=json.dumps(request_body_json, indent=4, ensure_ascii=True),
                name="Request body",
                attachment_type=AttachmentType.JSON,
                extension="json",
            )
        except json.JSONDecodeError:
            allure.attach(
                body=response.request.body,
                name="Request body",
                attachment_type=AttachmentType.TEXT,
                extension="txt",
            )

    try:
        response_json = response.json()
        allure.attach(
            body=json.dumps(response_json, indent=4, ensure_ascii=True),
            name="Response",
            attachment_type=AttachmentType.JSON,
            extension="json",
        )
    except json.JSONDecodeError:
        allure.attach(
            body=response.text,
            name="Response",
            attachment_type=AttachmentType.TEXT,
            extension="txt",
        )
