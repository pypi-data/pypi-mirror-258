# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/feature_store/jobs/v1/job_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from _qwak_proto.qwak.feature_store.jobs.v1 import job_pb2 as qwak_dot_feature__store_dot_jobs_dot_v1_dot_job__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,qwak/feature_store/jobs/v1/job_service.proto\x12\x1aqwak.feature.store.jobs.v1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a$qwak/feature_store/jobs/v1/job.proto\"b\n!DeleteFeaturesetJobByJobIdRequest\x12\x15\n\rfeatureset_id\x18\x01 \x01(\t\x12\x16\n\x0e\x65nvironment_id\x18\x02 \x01(\t\x12\x0e\n\x06job_id\x18\x03 \x01(\t\"F\n\"DeleteFeaturesetJobByJobIdResponse\x12 \n\x18\x64\x65leted_job_record_count\x18\x01 \x01(\x05\"L\n\x0f\x41pplyJobRequest\x12\x39\n\njob_record\x18\x01 \x01(\x0b\x32%.qwak.feature.store.jobs.v1.JobRecord\":\n\x10\x41pplyJobResponse\x12\x16\n\x0ejob_running_id\x18\x01 \x01(\x03\x12\x0e\n\x06job_id\x18\x02 \x01(\t\"F\n\x15InitPaginationRequest\x12\x15\n\rfeatureset_id\x18\x01 \x01(\t\x12\x16\n\x0e\x65nvironment_id\x18\x02 \x01(\t\"Q\n\x16InitPaginationResponse\x12\x14\n\x0crecord_count\x18\x01 \x01(\x03\x12!\n\x19pagination_session_max_id\x18\x02 \x01(\x03\"\x8b\x01\n\x0fListJobsRequest\x12\x15\n\rfeatureset_id\x18\x01 \x01(\t\x12\x16\n\x0e\x65nvironment_id\x18\x02 \x01(\t\x12\x11\n\tpage_size\x18\x03 \x01(\x05\x12\x13\n\x0bpage_number\x18\x04 \x01(\x05\x12!\n\x19pagination_session_max_id\x18\x05 \x01(\x03\"G\n\x10ListJobsResponse\x12\x33\n\x04jobs\x18\x01 \x03(\x0b\x32%.qwak.feature.store.jobs.v1.JobRecord\"N\n\x1dGetLatestSuccessfulJobRequest\x12\x15\n\rfeatureset_id\x18\x01 \x01(\t\x12\x16\n\x0e\x65nvironment_id\x18\x02 \x01(\t\"D\n\x13GetLatestJobRequest\x12\x15\n\rfeatureset_id\x18\x01 \x01(\t\x12\x16\n\x0e\x65nvironment_id\x18\x02 \x01(\t\"J\n\x14GetLatestJobResponse\x12\x32\n\x03job\x18\x01 \x01(\x0b\x32%.qwak.feature.store.jobs.v1.JobRecord\"c\n\x1eGetLatestSuccessfulJobResponse\x12\x32\n\x03job\x18\x01 \x01(\x0b\x32%.qwak.feature.store.jobs.v1.JobRecord\x12\r\n\x05\x66ound\x18\x02 \x01(\x08\"#\n!GetAllLatestSuccessfulJobsRequest\"Y\n\"GetAllLatestSuccessfulJobsResponse\x12\x33\n\x04jobs\x18\x01 \x03(\x0b\x32%.qwak.feature.store.jobs.v1.JobRecord\"L\n\x1b\x44\x65leteFeaturesetJobsRequest\x12\x15\n\rfeatureset_id\x18\x01 \x01(\t\x12\x16\n\x0e\x65nvironment_id\x18\x02 \x01(\t\"A\n\x1c\x44\x65leteFeaturesetJobsResponse\x12!\n\x19\x64\x65leted_job_records_count\x18\x01 \x01(\x05\"\x96\x01\n\x17GetJobsSummariesRequest\x12\x34\n\x10lower_time_bound\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x36\n\x10upper_time_bound\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x42\r\n\x0bupper_bound\"j\n\x18GetJobsSummariesResponse\x12N\n\x0ejobs_summaries\x18\x01 \x03(\x0b\x32\x36.qwak.feature.store.jobs.v1.FeaturesetLevelJobsSummary2\x9f\t\n\nJobService\x12\x65\n\x08\x41pplyJob\x12+.qwak.feature.store.jobs.v1.ApplyJobRequest\x1a,.qwak.feature.store.jobs.v1.ApplyJobResponse\x12w\n\x0eInitPagination\x12\x31.qwak.feature.store.jobs.v1.InitPaginationRequest\x1a\x32.qwak.feature.store.jobs.v1.InitPaginationResponse\x12\x65\n\x08ListJobs\x12+.qwak.feature.store.jobs.v1.ListJobsRequest\x1a,.qwak.feature.store.jobs.v1.ListJobsResponse\x12\x8f\x01\n\x16GetLatestSuccessfulJob\x12\x39.qwak.feature.store.jobs.v1.GetLatestSuccessfulJobRequest\x1a:.qwak.feature.store.jobs.v1.GetLatestSuccessfulJobResponse\x12\x9b\x01\n\x1aGetAllLatestSuccessfulJobs\x12=.qwak.feature.store.jobs.v1.GetAllLatestSuccessfulJobsRequest\x1a>.qwak.feature.store.jobs.v1.GetAllLatestSuccessfulJobsResponse\x12q\n\x0cGetLatestJob\x12/.qwak.feature.store.jobs.v1.GetLatestJobRequest\x1a\x30.qwak.feature.store.jobs.v1.GetLatestJobResponse\x12\x89\x01\n\x14\x44\x65leteFeaturesetJobs\x12\x37.qwak.feature.store.jobs.v1.DeleteFeaturesetJobsRequest\x1a\x38.qwak.feature.store.jobs.v1.DeleteFeaturesetJobsResponse\x12\x9b\x01\n\x1a\x44\x65leteFeaturesetJobByJobId\x12=.qwak.feature.store.jobs.v1.DeleteFeaturesetJobByJobIdRequest\x1a>.qwak.feature.store.jobs.v1.DeleteFeaturesetJobByJobIdResponse\x12}\n\x10GetJobsSummaries\x12\x33.qwak.feature.store.jobs.v1.GetJobsSummariesRequest\x1a\x34.qwak.feature.store.jobs.v1.GetJobsSummariesResponseB=\n%com.qwak.ai.feature.store.jobs.v1.apiP\x01Z\x12qwak/fsjobs;fsjobsb\x06proto3')



_DELETEFEATURESETJOBBYJOBIDREQUEST = DESCRIPTOR.message_types_by_name['DeleteFeaturesetJobByJobIdRequest']
_DELETEFEATURESETJOBBYJOBIDRESPONSE = DESCRIPTOR.message_types_by_name['DeleteFeaturesetJobByJobIdResponse']
_APPLYJOBREQUEST = DESCRIPTOR.message_types_by_name['ApplyJobRequest']
_APPLYJOBRESPONSE = DESCRIPTOR.message_types_by_name['ApplyJobResponse']
_INITPAGINATIONREQUEST = DESCRIPTOR.message_types_by_name['InitPaginationRequest']
_INITPAGINATIONRESPONSE = DESCRIPTOR.message_types_by_name['InitPaginationResponse']
_LISTJOBSREQUEST = DESCRIPTOR.message_types_by_name['ListJobsRequest']
_LISTJOBSRESPONSE = DESCRIPTOR.message_types_by_name['ListJobsResponse']
_GETLATESTSUCCESSFULJOBREQUEST = DESCRIPTOR.message_types_by_name['GetLatestSuccessfulJobRequest']
_GETLATESTJOBREQUEST = DESCRIPTOR.message_types_by_name['GetLatestJobRequest']
_GETLATESTJOBRESPONSE = DESCRIPTOR.message_types_by_name['GetLatestJobResponse']
_GETLATESTSUCCESSFULJOBRESPONSE = DESCRIPTOR.message_types_by_name['GetLatestSuccessfulJobResponse']
_GETALLLATESTSUCCESSFULJOBSREQUEST = DESCRIPTOR.message_types_by_name['GetAllLatestSuccessfulJobsRequest']
_GETALLLATESTSUCCESSFULJOBSRESPONSE = DESCRIPTOR.message_types_by_name['GetAllLatestSuccessfulJobsResponse']
_DELETEFEATURESETJOBSREQUEST = DESCRIPTOR.message_types_by_name['DeleteFeaturesetJobsRequest']
_DELETEFEATURESETJOBSRESPONSE = DESCRIPTOR.message_types_by_name['DeleteFeaturesetJobsResponse']
_GETJOBSSUMMARIESREQUEST = DESCRIPTOR.message_types_by_name['GetJobsSummariesRequest']
_GETJOBSSUMMARIESRESPONSE = DESCRIPTOR.message_types_by_name['GetJobsSummariesResponse']
DeleteFeaturesetJobByJobIdRequest = _reflection.GeneratedProtocolMessageType('DeleteFeaturesetJobByJobIdRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEFEATURESETJOBBYJOBIDREQUEST,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.DeleteFeaturesetJobByJobIdRequest)
  })
_sym_db.RegisterMessage(DeleteFeaturesetJobByJobIdRequest)

DeleteFeaturesetJobByJobIdResponse = _reflection.GeneratedProtocolMessageType('DeleteFeaturesetJobByJobIdResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEFEATURESETJOBBYJOBIDRESPONSE,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.DeleteFeaturesetJobByJobIdResponse)
  })
_sym_db.RegisterMessage(DeleteFeaturesetJobByJobIdResponse)

ApplyJobRequest = _reflection.GeneratedProtocolMessageType('ApplyJobRequest', (_message.Message,), {
  'DESCRIPTOR' : _APPLYJOBREQUEST,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.ApplyJobRequest)
  })
_sym_db.RegisterMessage(ApplyJobRequest)

ApplyJobResponse = _reflection.GeneratedProtocolMessageType('ApplyJobResponse', (_message.Message,), {
  'DESCRIPTOR' : _APPLYJOBRESPONSE,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.ApplyJobResponse)
  })
_sym_db.RegisterMessage(ApplyJobResponse)

InitPaginationRequest = _reflection.GeneratedProtocolMessageType('InitPaginationRequest', (_message.Message,), {
  'DESCRIPTOR' : _INITPAGINATIONREQUEST,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.InitPaginationRequest)
  })
_sym_db.RegisterMessage(InitPaginationRequest)

InitPaginationResponse = _reflection.GeneratedProtocolMessageType('InitPaginationResponse', (_message.Message,), {
  'DESCRIPTOR' : _INITPAGINATIONRESPONSE,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.InitPaginationResponse)
  })
_sym_db.RegisterMessage(InitPaginationResponse)

ListJobsRequest = _reflection.GeneratedProtocolMessageType('ListJobsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTJOBSREQUEST,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.ListJobsRequest)
  })
_sym_db.RegisterMessage(ListJobsRequest)

ListJobsResponse = _reflection.GeneratedProtocolMessageType('ListJobsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTJOBSRESPONSE,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.ListJobsResponse)
  })
_sym_db.RegisterMessage(ListJobsResponse)

GetLatestSuccessfulJobRequest = _reflection.GeneratedProtocolMessageType('GetLatestSuccessfulJobRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETLATESTSUCCESSFULJOBREQUEST,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.GetLatestSuccessfulJobRequest)
  })
_sym_db.RegisterMessage(GetLatestSuccessfulJobRequest)

GetLatestJobRequest = _reflection.GeneratedProtocolMessageType('GetLatestJobRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETLATESTJOBREQUEST,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.GetLatestJobRequest)
  })
_sym_db.RegisterMessage(GetLatestJobRequest)

GetLatestJobResponse = _reflection.GeneratedProtocolMessageType('GetLatestJobResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETLATESTJOBRESPONSE,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.GetLatestJobResponse)
  })
_sym_db.RegisterMessage(GetLatestJobResponse)

GetLatestSuccessfulJobResponse = _reflection.GeneratedProtocolMessageType('GetLatestSuccessfulJobResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETLATESTSUCCESSFULJOBRESPONSE,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.GetLatestSuccessfulJobResponse)
  })
_sym_db.RegisterMessage(GetLatestSuccessfulJobResponse)

GetAllLatestSuccessfulJobsRequest = _reflection.GeneratedProtocolMessageType('GetAllLatestSuccessfulJobsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETALLLATESTSUCCESSFULJOBSREQUEST,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.GetAllLatestSuccessfulJobsRequest)
  })
_sym_db.RegisterMessage(GetAllLatestSuccessfulJobsRequest)

GetAllLatestSuccessfulJobsResponse = _reflection.GeneratedProtocolMessageType('GetAllLatestSuccessfulJobsResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETALLLATESTSUCCESSFULJOBSRESPONSE,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.GetAllLatestSuccessfulJobsResponse)
  })
_sym_db.RegisterMessage(GetAllLatestSuccessfulJobsResponse)

DeleteFeaturesetJobsRequest = _reflection.GeneratedProtocolMessageType('DeleteFeaturesetJobsRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEFEATURESETJOBSREQUEST,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.DeleteFeaturesetJobsRequest)
  })
_sym_db.RegisterMessage(DeleteFeaturesetJobsRequest)

DeleteFeaturesetJobsResponse = _reflection.GeneratedProtocolMessageType('DeleteFeaturesetJobsResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEFEATURESETJOBSRESPONSE,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.DeleteFeaturesetJobsResponse)
  })
_sym_db.RegisterMessage(DeleteFeaturesetJobsResponse)

GetJobsSummariesRequest = _reflection.GeneratedProtocolMessageType('GetJobsSummariesRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETJOBSSUMMARIESREQUEST,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.GetJobsSummariesRequest)
  })
_sym_db.RegisterMessage(GetJobsSummariesRequest)

GetJobsSummariesResponse = _reflection.GeneratedProtocolMessageType('GetJobsSummariesResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETJOBSSUMMARIESRESPONSE,
  '__module__' : 'qwak.feature_store.jobs.v1.job_service_pb2'
  # @@protoc_insertion_point(class_scope:qwak.feature.store.jobs.v1.GetJobsSummariesResponse)
  })
_sym_db.RegisterMessage(GetJobsSummariesResponse)

_JOBSERVICE = DESCRIPTOR.services_by_name['JobService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%com.qwak.ai.feature.store.jobs.v1.apiP\001Z\022qwak/fsjobs;fsjobs'
  _DELETEFEATURESETJOBBYJOBIDREQUEST._serialized_start=147
  _DELETEFEATURESETJOBBYJOBIDREQUEST._serialized_end=245
  _DELETEFEATURESETJOBBYJOBIDRESPONSE._serialized_start=247
  _DELETEFEATURESETJOBBYJOBIDRESPONSE._serialized_end=317
  _APPLYJOBREQUEST._serialized_start=319
  _APPLYJOBREQUEST._serialized_end=395
  _APPLYJOBRESPONSE._serialized_start=397
  _APPLYJOBRESPONSE._serialized_end=455
  _INITPAGINATIONREQUEST._serialized_start=457
  _INITPAGINATIONREQUEST._serialized_end=527
  _INITPAGINATIONRESPONSE._serialized_start=529
  _INITPAGINATIONRESPONSE._serialized_end=610
  _LISTJOBSREQUEST._serialized_start=613
  _LISTJOBSREQUEST._serialized_end=752
  _LISTJOBSRESPONSE._serialized_start=754
  _LISTJOBSRESPONSE._serialized_end=825
  _GETLATESTSUCCESSFULJOBREQUEST._serialized_start=827
  _GETLATESTSUCCESSFULJOBREQUEST._serialized_end=905
  _GETLATESTJOBREQUEST._serialized_start=907
  _GETLATESTJOBREQUEST._serialized_end=975
  _GETLATESTJOBRESPONSE._serialized_start=977
  _GETLATESTJOBRESPONSE._serialized_end=1051
  _GETLATESTSUCCESSFULJOBRESPONSE._serialized_start=1053
  _GETLATESTSUCCESSFULJOBRESPONSE._serialized_end=1152
  _GETALLLATESTSUCCESSFULJOBSREQUEST._serialized_start=1154
  _GETALLLATESTSUCCESSFULJOBSREQUEST._serialized_end=1189
  _GETALLLATESTSUCCESSFULJOBSRESPONSE._serialized_start=1191
  _GETALLLATESTSUCCESSFULJOBSRESPONSE._serialized_end=1280
  _DELETEFEATURESETJOBSREQUEST._serialized_start=1282
  _DELETEFEATURESETJOBSREQUEST._serialized_end=1358
  _DELETEFEATURESETJOBSRESPONSE._serialized_start=1360
  _DELETEFEATURESETJOBSRESPONSE._serialized_end=1425
  _GETJOBSSUMMARIESREQUEST._serialized_start=1428
  _GETJOBSSUMMARIESREQUEST._serialized_end=1578
  _GETJOBSSUMMARIESRESPONSE._serialized_start=1580
  _GETJOBSSUMMARIESRESPONSE._serialized_end=1686
  _JOBSERVICE._serialized_start=1689
  _JOBSERVICE._serialized_end=2872
# @@protoc_insertion_point(module_scope)
