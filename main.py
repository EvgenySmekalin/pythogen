# This is a sample Python script.
import json
from pprint import PrettyPrinter
from pprint import pprint
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Union

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# import httpx

from openapi.openapi import Document
from openapi.openapi import Example
from openapi.openapi import Info
from openapi.openapi import MediaType
from openapi.openapi import Operation
from openapi.openapi import PathItem
from openapi.openapi import Reference
from openapi.openapi import Response
from openapi.openapi import ResponsesContainer


def get_info(document: Dict) -> Info:
    info = document.get('info')

    return Info(
        title=info.get('title'),
        summary=None,
        description=None,
        terms_of_service=None,
        contact=None,
        license=None,
        version=info.get('version'),
    )


def get_examples(media_type_value: Dict) -> Optional[Mapping[str, Union[Example, Reference]]]:
    examples = media_type_value.get('examples')

    if not examples:
        return None

    return {
        name: Example(
            summary=None,
            description=None,
            value=example.get('value'),
            external_value=None,
        )
        for name, example in examples.items()
    }


def get_content(response: Dict) -> Optional[Mapping[str, MediaType]]:
    content = response.get('content')

    if not content:
        return None

    return {
        media_type: MediaType(
            schema=None,
            example=None,
            examples=get_examples(media_type_value),
            encoding=None,
        )
        for media_type, media_type_value in content.items()
    }


def get_responses(operation: Dict) -> Optional[ResponsesContainer]:
    responses_container: Optional[Dict] = operation.get('responses')

    if not responses_container:
        return None

    default = responses_container.get('default')
    default_response = None

    if default:
        default_response = Response(
            description=default.get('description'),
            headers=None,
            content=None,
            links=None
        )

    http_responses = {}

    for http_status_code, response in responses_container.items():
        http_responses[http_status_code] = Response(
            description=response.get('description'),
            headers=None,
            content=get_content(response),
            links=None
        )

    return ResponsesContainer(
        default=default,
        http_status_code_map=http_responses,
    )


def get_operation(operation_type: str, path_item: Dict) -> Optional[Operation]:
    operation = path_item.get(operation_type)

    if not operation:
        return None

    return Operation(
        tags=None,
        summary=operation.get('summary'),
        description=None,
        external_docs=None,
        operation_id=operation.get('operationId'),
        parameters=None,
        request_body=None,
        responses=get_responses(operation),
        callbacks=None,
        deprecated=None,
        security=None,
        servers=None,
    )


def get_paths(document: Dict) -> Optional[List[PathItem]]:
    document_paths = document.get('paths')

    if not document_paths:
        return None

    paths = []

    for path, path_item in document_paths.items():
        paths.append(
            PathItem(
                path=path,
                ref=None,
                summary=None,
                description=None,
                get=get_operation(operation_type='get', path_item=path_item),
                put=None,
                post=None,
                delete=None,
                options=None,
                head=None,
                patch=None,
                trace=None,
                servers=None,
                parameters=None,
            )
        )

    return paths


def parse_document(document: Dict) -> Document:
    return Document(
        openapi=document.get('openapi'),
        info=get_info(document),
        json_schema_dialect=None,
        servers=None,
        paths=get_paths(document),
        webhooks=None,
        components=None,
        security=None,
        tags=None,
        external_docs=None,
    )


if __name__ == '__main__':
    with open('api-with-examples.json', 'r') as open_api_file:
        data = open_api_file.read()

    open_api_document = parse_document(json.loads(data))

    pp = PrettyPrinter(indent=1)
    pp.pprint(open_api_document)


