"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.struct_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _Type:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _TypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_Type.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    INVALID_USER_APPLICATION_TYPE: _Type.ValueType  # 0
    REMOTE_BUILD: _Type.ValueType  # 1
    BATCH_FEATURE_PROCESSOR: _Type.ValueType  # 2
    STREAMING_FEATURE_PROCESSOR: _Type.ValueType  # 3
    BATCH_INFERENCE_TASK: _Type.ValueType  # 4
    MODEL_DEPLOYMENT: _Type.ValueType  # 5
    MODEL_MONITOR: _Type.ValueType  # 6
    DEPLOYMENT_MICROSERVICE: _Type.ValueType  # 7
    APPLICATION: _Type.ValueType  # 8
    BATCH_FEATURESET: _Type.ValueType  # 9

class Type(_Type, metaclass=_TypeEnumTypeWrapper): ...

INVALID_USER_APPLICATION_TYPE: Type.ValueType  # 0
REMOTE_BUILD: Type.ValueType  # 1
BATCH_FEATURE_PROCESSOR: Type.ValueType  # 2
STREAMING_FEATURE_PROCESSOR: Type.ValueType  # 3
BATCH_INFERENCE_TASK: Type.ValueType  # 4
MODEL_DEPLOYMENT: Type.ValueType  # 5
MODEL_MONITOR: Type.ValueType  # 6
DEPLOYMENT_MICROSERVICE: Type.ValueType  # 7
APPLICATION: Type.ValueType  # 8
BATCH_FEATURESET: Type.ValueType  # 9
global___Type = Type

class Spec(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUE_FIELD_NUMBER: builtins.int
    @property
    def value(self) -> google.protobuf.struct_pb2.Struct: ...
    def __init__(
        self,
        *,
        value: google.protobuf.struct_pb2.Struct | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["value", b"value"]) -> None: ...

global___Spec = Spec

class Status(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUE_FIELD_NUMBER: builtins.int
    @property
    def value(self) -> google.protobuf.struct_pb2.Struct: ...
    def __init__(
        self,
        *,
        value: google.protobuf.struct_pb2.Struct | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["value", b"value"]) -> None: ...

global___Status = Status
