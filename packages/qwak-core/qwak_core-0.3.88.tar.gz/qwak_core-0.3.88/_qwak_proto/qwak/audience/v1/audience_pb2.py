# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/audience/v1/audience.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fqwak/audience/v1/audience.proto\x12\x10qwak.audience.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"I\n\rAudienceEntry\x12\n\n\x02id\x18\x01 \x01(\t\x12,\n\x08\x61udience\x18\x02 \x01(\x0b\x32\x1a.qwak.audience.v1.Audience\"\xc1\x03\n\x08\x41udience\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12/\n\nconditions\x18\x03 \x03(\x0b\x32\x1b.qwak.audience.v1.Condition\x12\'\n\x06routes\x18\x04 \x03(\x0b\x32\x17.qwak.audience.v1.Route\x12+\n\x07\x63reated\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x12\n\ncreated_by\x18\x06 \x01(\t\x12,\n\x08modified\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0bmodified_by\x18\x08 \x01(\t\x12M\n\x12\x65nvironment_routes\x18\t \x03(\x0b\x32\x31.qwak.audience.v1.Audience.EnvironmentRoutesEntry\x1a\x65\n\x16\x45nvironmentRoutesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12:\n\x05value\x18\x02 \x01(\x0b\x32+.qwak.audience.v1.EnvironmentAudienceRoutes:\x02\x38\x01\"D\n\x19\x45nvironmentAudienceRoutes\x12\'\n\x06routes\x18\x01 \x03(\x0b\x32\x17.qwak.audience.v1.Route\"y\n\x13\x41udienceRoutesEntry\x12\x13\n\x0b\x61udience_id\x18\x01 \x01(\t\x12\x15\n\raudience_name\x18\x02 \x01(\t\x12\'\n\x06routes\x18\x04 \x03(\x0b\x32\x17.qwak.audience.v1.Route\x12\r\n\x05order\x18\x05 \x01(\x05\"\xb1\x01\n\tCondition\x12\x0b\n\x03key\x18\x01 \x01(\t\x12=\n\x10\x62inary_condition\x18\x02 \x01(\x0b\x32!.qwak.audience.v1.BinaryConditionH\x00\x12;\n\x0funary_condition\x18\x03 \x01(\x0b\x32 .qwak.audience.v1.UnaryConditionH\x00\x12\x0e\n\x06invert\x18\x04 \x01(\x08\x42\x0b\n\tcondition\"X\n\x0eUnaryCondition\x12\x35\n\x08operator\x18\x01 \x01(\x0e\x32#.qwak.audience.v1.UnaryOperatorType\x12\x0f\n\x07operand\x18\x02 \x01(\t\"x\n\x0f\x42inaryCondition\x12\x36\n\x08operator\x18\x01 \x01(\x0e\x32$.qwak.audience.v1.BinaryOperatorType\x12\x15\n\rfirst_operand\x18\x02 \x01(\t\x12\x16\n\x0esecond_operand\x18\x03 \x01(\t\"\x9a\x01\n\x05Route\x12\x16\n\x0evariation_name\x18\x01 \x01(\t\x12\x0e\n\x06weight\x18\x02 \x01(\r\x12\x0e\n\x06shadow\x18\x03 \x01(\x08\x12\x10\n\x08model_id\x18\x04 \x01(\t\x12\x16\n\x0e\x65nvironment_id\x18\x05 \x01(\t\x12\x13\n\x0b\x61udience_id\x18\x06 \x01(\t\x12\x1a\n\x12request_timeout_ms\x18\x07 \x01(\x05*\x9e\x02\n\x11UnaryOperatorType\x12\x1f\n\x1bUNARY_OPERATOR_TYPE_INVALID\x10\x00\x12#\n\x1fUNARY_OPERATOR_TYPE_EXACT_MATCH\x10\x01\x12(\n$UNARY_OPERATOR_TYPE_SAFE_REGEX_MATCH\x10\x02\x12%\n!UNARY_OPERATOR_TYPE_PRESENT_MATCH\x10\x03\x12$\n UNARY_OPERATOR_TYPE_PREFIX_MATCH\x10\x04\x12$\n UNARY_OPERATOR_TYPE_SUFFIX_MATCH\x10\x05\x12&\n\"UNARY_OPERATOR_TYPE_CONTAINS_MATCH\x10\x06*\\\n\x12\x42inaryOperatorType\x12 \n\x1c\x42INARY_OPERATOR_TYPE_INVALID\x10\x00\x12$\n BINARY_OPERATOR_TYPE_RANGE_MATCH\x10\x01\x42\x42\n\x14\x63om.qwak.audience.v1B\rAudienceProtoP\x01Z\x19qwak/audience/v1;audienceb\x06proto3')

_UNARYOPERATORTYPE = DESCRIPTOR.enum_types_by_name['UnaryOperatorType']
UnaryOperatorType = enum_type_wrapper.EnumTypeWrapper(_UNARYOPERATORTYPE)
_BINARYOPERATORTYPE = DESCRIPTOR.enum_types_by_name['BinaryOperatorType']
BinaryOperatorType = enum_type_wrapper.EnumTypeWrapper(_BINARYOPERATORTYPE)
UNARY_OPERATOR_TYPE_INVALID = 0
UNARY_OPERATOR_TYPE_EXACT_MATCH = 1
UNARY_OPERATOR_TYPE_SAFE_REGEX_MATCH = 2
UNARY_OPERATOR_TYPE_PRESENT_MATCH = 3
UNARY_OPERATOR_TYPE_PREFIX_MATCH = 4
UNARY_OPERATOR_TYPE_SUFFIX_MATCH = 5
UNARY_OPERATOR_TYPE_CONTAINS_MATCH = 6
BINARY_OPERATOR_TYPE_INVALID = 0
BINARY_OPERATOR_TYPE_RANGE_MATCH = 1


_AUDIENCEENTRY = DESCRIPTOR.message_types_by_name['AudienceEntry']
_AUDIENCE = DESCRIPTOR.message_types_by_name['Audience']
_AUDIENCE_ENVIRONMENTROUTESENTRY = _AUDIENCE.nested_types_by_name['EnvironmentRoutesEntry']
_ENVIRONMENTAUDIENCEROUTES = DESCRIPTOR.message_types_by_name['EnvironmentAudienceRoutes']
_AUDIENCEROUTESENTRY = DESCRIPTOR.message_types_by_name['AudienceRoutesEntry']
_CONDITION = DESCRIPTOR.message_types_by_name['Condition']
_UNARYCONDITION = DESCRIPTOR.message_types_by_name['UnaryCondition']
_BINARYCONDITION = DESCRIPTOR.message_types_by_name['BinaryCondition']
_ROUTE = DESCRIPTOR.message_types_by_name['Route']
AudienceEntry = _reflection.GeneratedProtocolMessageType('AudienceEntry', (_message.Message,), {
  'DESCRIPTOR' : _AUDIENCEENTRY,
  '__module__' : 'qwak.audience.v1.audience_pb2'
  # @@protoc_insertion_point(class_scope:qwak.audience.v1.AudienceEntry)
  })
_sym_db.RegisterMessage(AudienceEntry)

Audience = _reflection.GeneratedProtocolMessageType('Audience', (_message.Message,), {

  'EnvironmentRoutesEntry' : _reflection.GeneratedProtocolMessageType('EnvironmentRoutesEntry', (_message.Message,), {
    'DESCRIPTOR' : _AUDIENCE_ENVIRONMENTROUTESENTRY,
    '__module__' : 'qwak.audience.v1.audience_pb2'
    # @@protoc_insertion_point(class_scope:qwak.audience.v1.Audience.EnvironmentRoutesEntry)
    })
  ,
  'DESCRIPTOR' : _AUDIENCE,
  '__module__' : 'qwak.audience.v1.audience_pb2'
  # @@protoc_insertion_point(class_scope:qwak.audience.v1.Audience)
  })
_sym_db.RegisterMessage(Audience)
_sym_db.RegisterMessage(Audience.EnvironmentRoutesEntry)

EnvironmentAudienceRoutes = _reflection.GeneratedProtocolMessageType('EnvironmentAudienceRoutes', (_message.Message,), {
  'DESCRIPTOR' : _ENVIRONMENTAUDIENCEROUTES,
  '__module__' : 'qwak.audience.v1.audience_pb2'
  # @@protoc_insertion_point(class_scope:qwak.audience.v1.EnvironmentAudienceRoutes)
  })
_sym_db.RegisterMessage(EnvironmentAudienceRoutes)

AudienceRoutesEntry = _reflection.GeneratedProtocolMessageType('AudienceRoutesEntry', (_message.Message,), {
  'DESCRIPTOR' : _AUDIENCEROUTESENTRY,
  '__module__' : 'qwak.audience.v1.audience_pb2'
  # @@protoc_insertion_point(class_scope:qwak.audience.v1.AudienceRoutesEntry)
  })
_sym_db.RegisterMessage(AudienceRoutesEntry)

Condition = _reflection.GeneratedProtocolMessageType('Condition', (_message.Message,), {
  'DESCRIPTOR' : _CONDITION,
  '__module__' : 'qwak.audience.v1.audience_pb2'
  # @@protoc_insertion_point(class_scope:qwak.audience.v1.Condition)
  })
_sym_db.RegisterMessage(Condition)

UnaryCondition = _reflection.GeneratedProtocolMessageType('UnaryCondition', (_message.Message,), {
  'DESCRIPTOR' : _UNARYCONDITION,
  '__module__' : 'qwak.audience.v1.audience_pb2'
  # @@protoc_insertion_point(class_scope:qwak.audience.v1.UnaryCondition)
  })
_sym_db.RegisterMessage(UnaryCondition)

BinaryCondition = _reflection.GeneratedProtocolMessageType('BinaryCondition', (_message.Message,), {
  'DESCRIPTOR' : _BINARYCONDITION,
  '__module__' : 'qwak.audience.v1.audience_pb2'
  # @@protoc_insertion_point(class_scope:qwak.audience.v1.BinaryCondition)
  })
_sym_db.RegisterMessage(BinaryCondition)

Route = _reflection.GeneratedProtocolMessageType('Route', (_message.Message,), {
  'DESCRIPTOR' : _ROUTE,
  '__module__' : 'qwak.audience.v1.audience_pb2'
  # @@protoc_insertion_point(class_scope:qwak.audience.v1.Route)
  })
_sym_db.RegisterMessage(Route)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024com.qwak.audience.v1B\rAudienceProtoP\001Z\031qwak/audience/v1;audience'
  _AUDIENCE_ENVIRONMENTROUTESENTRY._options = None
  _AUDIENCE_ENVIRONMENTROUTESENTRY._serialized_options = b'8\001'
  _UNARYOPERATORTYPE._serialized_start=1356
  _UNARYOPERATORTYPE._serialized_end=1642
  _BINARYOPERATORTYPE._serialized_start=1644
  _BINARYOPERATORTYPE._serialized_end=1736
  _AUDIENCEENTRY._serialized_start=86
  _AUDIENCEENTRY._serialized_end=159
  _AUDIENCE._serialized_start=162
  _AUDIENCE._serialized_end=611
  _AUDIENCE_ENVIRONMENTROUTESENTRY._serialized_start=510
  _AUDIENCE_ENVIRONMENTROUTESENTRY._serialized_end=611
  _ENVIRONMENTAUDIENCEROUTES._serialized_start=613
  _ENVIRONMENTAUDIENCEROUTES._serialized_end=681
  _AUDIENCEROUTESENTRY._serialized_start=683
  _AUDIENCEROUTESENTRY._serialized_end=804
  _CONDITION._serialized_start=807
  _CONDITION._serialized_end=984
  _UNARYCONDITION._serialized_start=986
  _UNARYCONDITION._serialized_end=1074
  _BINARYCONDITION._serialized_start=1076
  _BINARYCONDITION._serialized_end=1196
  _ROUTE._serialized_start=1199
  _ROUTE._serialized_end=1353
# @@protoc_insertion_point(module_scope)
