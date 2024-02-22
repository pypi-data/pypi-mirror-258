"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import qwak.instance_template.instance_template_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class ListInstanceTemplatesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OPTIONAL_INSTANCE_FILTER_FIELD_NUMBER: builtins.int
    @property
    def optional_instance_filter(self) -> qwak.instance_template.instance_template_pb2.InstanceFilter: ...
    def __init__(
        self,
        *,
        optional_instance_filter: qwak.instance_template.instance_template_pb2.InstanceFilter | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["optional_instance_filter", b"optional_instance_filter"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["optional_instance_filter", b"optional_instance_filter"]) -> None: ...

global___ListInstanceTemplatesRequest = ListInstanceTemplatesRequest

class ListInstanceTemplatesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INSTANCE_TEMPLATE_LIST_FIELD_NUMBER: builtins.int
    @property
    def instance_template_list(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[qwak.instance_template.instance_template_pb2.InstanceTemplateSpec]: ...
    def __init__(
        self,
        *,
        instance_template_list: collections.abc.Iterable[qwak.instance_template.instance_template_pb2.InstanceTemplateSpec] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["instance_template_list", b"instance_template_list"]) -> None: ...

global___ListInstanceTemplatesResponse = ListInstanceTemplatesResponse

class GetInstanceTemplateRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    id: builtins.str
    def __init__(
        self,
        *,
        id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["id", b"id"]) -> None: ...

global___GetInstanceTemplateRequest = GetInstanceTemplateRequest

class GetInstanceTemplateResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INSTANCE_TEMPLATE_FIELD_NUMBER: builtins.int
    @property
    def instance_template(self) -> qwak.instance_template.instance_template_pb2.InstanceTemplateSpec: ...
    def __init__(
        self,
        *,
        instance_template: qwak.instance_template.instance_template_pb2.InstanceTemplateSpec | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["instance_template", b"instance_template"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["instance_template", b"instance_template"]) -> None: ...

global___GetInstanceTemplateResponse = GetInstanceTemplateResponse
