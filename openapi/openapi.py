from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import List
from typing import Mapping
from typing import Optional
from typing import Set
from typing import Union


Expression = str


@dataclass
class Contact:
    name: Optional[str]
    url: Optional[str]
    email: Optional[str]


@dataclass
class License:
    name: str
    identifier: Optional[str]
    url: Optional[str]


@dataclass
class Info:
    title: str
    summary: Optional[str]
    description: Optional[str]
    terms_of_service: Optional[str]
    contact: Optional[Contact]
    license: Optional[License]
    version: str


@dataclass
class ServerVariable:
    enum: Optional[Set[str]]
    default: str
    description: Optional[str]


@dataclass
class Server:
    url: str
    description: Optional[str]
    variables: Optional[Mapping[str, ServerVariable]]


@dataclass
class ExternalDocumentation:
    description: Optional[str]
    url: str


@dataclass
class Discriminator:
    property_name: str
    mapping: Optional[Mapping[str, str]]


@dataclass
class XML:
    name: Optional[str]
    namespace: Optional[str]
    prefix: Optional[str]
    attribute: Optional[bool] = False
    wrapped: Optional[bool] = False


@dataclass
class Schema:
    discriminator: Optional[Discriminator]
    xml: Optional[XML]
    external_docs: Optional[ExternalDocumentation]
    example: Optional[Any]


class Style(Enum):
    MATRIX = "matrix"
    LABEL = "label"
    FORM = "form"
    SIMPLE = "simple"
    SPACE_DELIMITED = "space_delimited"
    PIPE_DELIMITED = "pipe_delimited"
    DEEP_OBJECT = "deep_object"


class DataType(Enum):
    PRIMITIVE = "primitive"
    ARRAY = "array"
    OBJECT = "object"


class DataIn(Enum):
    PATH = "path"
    QUERY = "query"
    COOKIE = "cookie"
    HEADER = "header"


@dataclass
class StyleValue:
    style: Style
    type: List[DataType]  # TODO: check single value or list
    in_: List[DataIn]  # TODO: check single value or list


# https://spec.openapis.org/oas/v3.1.0#style-values
style_value_map = {
    Style.MATRIX: StyleValue(
        style=Style.MATRIX, type=[DataType.PRIMITIVE, DataType.ARRAY, DataType.OBJECT], in_=[DataIn.PATH]
    ),
    Style.LABEL: "",
    Style.FORM: "",
    Style.SIMPLE: "",
    Style.SPACE_DELIMITED: "",
    Style.PIPE_DELIMITED: "",
    Style.DEEP_OBJECT: "",
}


@dataclass
class Reference:
    ref: str
    summary: Optional[str]
    description: Optional[str]


@dataclass
class Example:
    summary: Optional[str]
    description: Optional[str]
    value: Optional[Any]
    external_value: Optional[str]


@dataclass
class Header:
    name: str
    description: Optional[str]
    external_docs: ExternalDocumentation


@dataclass
class Encoding:
    content_type: Optional[str]
    headers: Optional[Mapping[str, Union[Header, Reference]]]
    style: Optional[str]
    explode: Optional[str]
    allow_reserved: Optional[bool]


@dataclass
class MediaType:
    schema: Optional[Schema]
    example: Optional[Any]
    examples: Optional[Mapping[str, Union[Example, Reference]]]
    encoding: Optional[Mapping[str, Encoding]]


@dataclass
class Parameter:
    name: str
    in_: str
    description: Optional[str]
    required: Optional[bool]  # If Parameter.in_ == 'path' -> MUST be True. Otherwise, default is False
    style: Optional[StyleValue]
    schema: Optional[Schema]
    example: Optional[Any]
    examples: Optional[Mapping[str, Union[Example, Reference]]]
    content: Optional[Mapping[str, MediaType]]
    deprecated: Optional[bool] = False
    allow_empty_value: Optional[bool] = False
    explode: Optional[bool] = False
    allow_reserved: Optional[bool] = False


@dataclass
class RequestBody:
    description: Optional[str]
    content: Mapping[str, MediaType]
    required: Optional[bool] = False


@dataclass
class Link:
    operation_ref: Optional[str]
    operation_id: Optional[str]
    parameters: Optional[Mapping[str, Union[Any, Expression]]]
    request_body: Optional[Union[Any, Expression]]
    description: Optional[str]
    server: Optional[Server]


@dataclass
class Response:
    description: str
    headers: Optional[Mapping[str, Union[Header, Reference]]]
    content: Optional[Mapping[str, MediaType]]
    links: Optional[Mapping[str, Union[Link, Reference]]]


@dataclass
class ResponsesContainer:
    default: Optional[Union[Response, Reference]]
    http_status_code_map: Optional[Mapping[str, Union[Response, Reference]]]  # codes may contain the wildcard X char


@dataclass
class SecurityRequirement:
    name: str
    values: List[str]


@dataclass
class Operation:
    tags: Optional[List[str]]
    summary: Optional[str]
    description: Optional[str]
    external_docs: Optional[ExternalDocumentation]
    operation_id: Optional[str]
    parameters: Optional[List[Union[Parameter, Reference]]]
    request_body: Optional[Union[RequestBody, Reference]]
    responses: Optional[List[Response]]
    callbacks: Optional[Mapping[str, Union["Callback", Reference]]]
    deprecated: Optional[bool]
    security: Optional[List[SecurityRequirement]]
    servers: Optional[List[Server]]


@dataclass
class PathItem:
    path: str
    ref: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    get: Optional[Operation]
    put: Optional[Operation]
    post: Optional[Operation]
    delete: Optional[Operation]
    options: Optional[Operation]
    head: Optional[Operation]
    patch: Optional[Operation]
    trace: Optional[Operation]
    servers: Optional[List[Server]]
    parameters: Optional[List[Union[Parameter, Reference]]]


@dataclass
class Callback:
    expression_key: str
    expression_value: Union[PathItem, Reference]


@dataclass
class OAuthFlow:
    authorization_url: str
    token_url: Optional[str]
    refresh_url: Optional[str]
    scopes: Optional[Mapping[str, str]]


@dataclass
class OAuthFlows:
    implicit: Optional[OAuthFlow]
    password: Optional[OAuthFlow]
    client_credentials: Optional[OAuthFlow]
    authorization_code: Optional[OAuthFlow]


@dataclass
class SecurityScheme:
    type: str
    description: Optional[str]
    name: str
    in_: str
    scheme: str
    bearer_format: Optional[str]
    flows: OAuthFlows
    open_id_connect_url: str


@dataclass
class Components:
    schemas: Optional[Mapping[str, Schema]]
    responses: Optional[Mapping[str, Union[Response, Reference]]]
    parameters: Optional[Mapping[str, Union[Parameter, Reference]]]
    examples: Optional[Mapping[str, Union[Example, Reference]]]
    request_bodies: Optional[Mapping[str, Union[RequestBody, Reference]]]
    headers: Optional[Mapping[str, Union[Header, Reference]]]
    security_schemes: Optional[Mapping[str, Union[SecurityScheme, Reference]]]
    links: Optional[Mapping[str, Union[Link, Reference]]]
    callbacks: Optional[Mapping[str, Union[Callback, Reference]]]
    path_items: Optional[Mapping[str, Union[PathItem, Reference]]]


@dataclass
class Tag:
    name: str
    description: Optional[str]
    external_docs: ExternalDocumentation


@dataclass
class Document:
    openapi: str
    info: Info
    json_schema_dialect: Optional[str]
    servers: Optional[List[Server]]
    paths: Optional[List[PathItem]]
    webhooks: Optional[Mapping[str, Union[PathItem, Reference]]]
    components: Optional[Components]
    security: Optional[List[SecurityRequirement]]
    tags: Optional[List[Tag]]
    external_docs: Optional[ExternalDocumentation]
