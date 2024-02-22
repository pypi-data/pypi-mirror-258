"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _MemoryUnitApi:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _MemoryUnitApiEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_MemoryUnitApi.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    UNKNOWN_MEMORY_UNIT: _MemoryUnitApi.ValueType  # 0
    MIB: _MemoryUnitApi.ValueType  # 1
    GIB: _MemoryUnitApi.ValueType  # 2

class MemoryUnitApi(_MemoryUnitApi, metaclass=_MemoryUnitApiEnumTypeWrapper): ...

UNKNOWN_MEMORY_UNIT: MemoryUnitApi.ValueType  # 0
MIB: MemoryUnitApi.ValueType  # 1
GIB: MemoryUnitApi.ValueType  # 2
global___MemoryUnitApi = MemoryUnitApi

class _InputFileType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _InputFileTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_InputFileType.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    UNDEFINED_INPUT_FILE_TYPE: _InputFileType.ValueType  # 0
    CSV_INPUT_FILE_TYPE: _InputFileType.ValueType  # 1
    FEATHER_INPUT_FILE_TYPE: _InputFileType.ValueType  # 2
    PARQUET_INPUT_FILE_TYPE: _InputFileType.ValueType  # 3

class InputFileType(_InputFileType, metaclass=_InputFileTypeEnumTypeWrapper): ...

UNDEFINED_INPUT_FILE_TYPE: InputFileType.ValueType  # 0
CSV_INPUT_FILE_TYPE: InputFileType.ValueType  # 1
FEATHER_INPUT_FILE_TYPE: InputFileType.ValueType  # 2
PARQUET_INPUT_FILE_TYPE: InputFileType.ValueType  # 3
global___InputFileType = InputFileType

class _OutputFileType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _OutputFileTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_OutputFileType.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    UNDEFINED_OUTPUT_FILE_TYPE: _OutputFileType.ValueType  # 0
    CSV_OUTPUT_FILE_TYPE: _OutputFileType.ValueType  # 1
    FEATHER_OUTPUT_FILE_TYPE: _OutputFileType.ValueType  # 2
    PARQUET_OUTPUT_FILE_TYPE: _OutputFileType.ValueType  # 3

class OutputFileType(_OutputFileType, metaclass=_OutputFileTypeEnumTypeWrapper): ...

UNDEFINED_OUTPUT_FILE_TYPE: OutputFileType.ValueType  # 0
CSV_OUTPUT_FILE_TYPE: OutputFileType.ValueType  # 1
FEATHER_OUTPUT_FILE_TYPE: OutputFileType.ValueType  # 2
PARQUET_OUTPUT_FILE_TYPE: OutputFileType.ValueType  # 3
global___OutputFileType = OutputFileType

class _GpuType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _GpuTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_GpuType.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    INVALID_GPU: _GpuType.ValueType  # 0
    NVIDIA_K80: _GpuType.ValueType  # 1
    NVIDIA_V100: _GpuType.ValueType  # 2
    NVIDIA_A100: _GpuType.ValueType  # 3
    NVIDIA_T4: _GpuType.ValueType  # 4
    NVIDIA_A10G: _GpuType.ValueType  # 5
    NVIDIA_L4: _GpuType.ValueType  # 6

class GpuType(_GpuType, metaclass=_GpuTypeEnumTypeWrapper): ...

INVALID_GPU: GpuType.ValueType  # 0
NVIDIA_K80: GpuType.ValueType  # 1
NVIDIA_V100: GpuType.ValueType  # 2
NVIDIA_A100: GpuType.ValueType  # 3
NVIDIA_T4: GpuType.ValueType  # 4
NVIDIA_A10G: GpuType.ValueType  # 5
NVIDIA_L4: GpuType.ValueType  # 6
global___GpuType = GpuType

class _CloudProvider:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _CloudProviderEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_CloudProvider.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    UNKNOWN_CLOUD_PROVIDER: _CloudProvider.ValueType  # 0
    AWS: _CloudProvider.ValueType  # 1
    GCP: _CloudProvider.ValueType  # 2

class CloudProvider(_CloudProvider, metaclass=_CloudProviderEnumTypeWrapper): ...

UNKNOWN_CLOUD_PROVIDER: CloudProvider.ValueType  # 0
AWS: CloudProvider.ValueType  # 1
GCP: CloudProvider.ValueType  # 2
global___CloudProvider = CloudProvider

class ListInferenceJobFilesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BUCKET_FIELD_NUMBER: builtins.int
    DIRECTORY_PATH_FIELD_NUMBER: builtins.int
    TOKEN_SECRET_FIELD_NUMBER: builtins.int
    SECRET_SECRET_FIELD_NUMBER: builtins.int
    SECRET_SERVICE_URL_FIELD_NUMBER: builtins.int
    ROLE_ARN_FIELD_NUMBER: builtins.int
    AWS_CREDENTIALS_FIELD_NUMBER: builtins.int
    GCP_CREDENTIALS_FIELD_NUMBER: builtins.int
    bucket: builtins.str
    """The bucket in cloud storage"""
    directory_path: builtins.str
    """The path in the bucket to read the files from"""
    token_secret: builtins.str
    """The qwak secret the bucket's token is stored in"""
    secret_secret: builtins.str
    """The qwak secret the bucket's secret is stored in"""
    secret_service_url: builtins.str
    """The qwak secret service url for that environment"""
    role_arn: builtins.str
    """The role arn to assume"""
    @property
    def aws_credentials(self) -> global___AwsCredentials: ...
    @property
    def gcp_credentials(self) -> global___GcpCredentials: ...
    def __init__(
        self,
        *,
        bucket: builtins.str = ...,
        directory_path: builtins.str = ...,
        token_secret: builtins.str = ...,
        secret_secret: builtins.str = ...,
        secret_service_url: builtins.str = ...,
        role_arn: builtins.str = ...,
        aws_credentials: global___AwsCredentials | None = ...,
        gcp_credentials: global___GcpCredentials | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["aws_credentials", b"aws_credentials", "cloud_client_credentials", b"cloud_client_credentials", "gcp_credentials", b"gcp_credentials"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["aws_credentials", b"aws_credentials", "bucket", b"bucket", "cloud_client_credentials", b"cloud_client_credentials", "directory_path", b"directory_path", "gcp_credentials", b"gcp_credentials", "role_arn", b"role_arn", "secret_secret", b"secret_secret", "secret_service_url", b"secret_service_url", "token_secret", b"token_secret"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["cloud_client_credentials", b"cloud_client_credentials"]) -> typing_extensions.Literal["aws_credentials", "gcp_credentials"] | None: ...

global___ListInferenceJobFilesRequest = ListInferenceJobFilesRequest

class AwsCredentials(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ROLE_ARN_FIELD_NUMBER: builtins.int
    TOKEN_SECRET_FIELD_NUMBER: builtins.int
    SECRET_SECRET_FIELD_NUMBER: builtins.int
    role_arn: builtins.str
    """The role arn to assume"""
    token_secret: builtins.str
    """The qwak secret the bucket's token is stored in"""
    secret_secret: builtins.str
    """The qwak secret the bucket's secret is stored in"""
    def __init__(
        self,
        *,
        role_arn: builtins.str = ...,
        token_secret: builtins.str = ...,
        secret_secret: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["role_arn", b"role_arn", "secret_secret", b"secret_secret", "token_secret", b"token_secret"]) -> None: ...

global___AwsCredentials = AwsCredentials

class GcpCredentials(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SERVICE_ACCOUNT_JSON_KEY_SECRET_FIELD_NUMBER: builtins.int
    service_account_json_key_secret: builtins.str
    def __init__(
        self,
        *,
        service_account_json_key_secret: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["service_account_json_key_secret", b"service_account_json_key_secret"]) -> None: ...

global___GcpCredentials = GcpCredentials

class ListInferenceJobFilesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FILE_NAMES_FIELD_NUMBER: builtins.int
    SUCCESS_FIELD_NUMBER: builtins.int
    FAILURE_REASON_FIELD_NUMBER: builtins.int
    @property
    def file_names(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """The list of files in the folder"""
    success: builtins.bool
    """Whether the request was successful or not"""
    failure_reason: builtins.str
    """The failure description"""
    def __init__(
        self,
        *,
        file_names: collections.abc.Iterable[builtins.str] | None = ...,
        success: builtins.bool = ...,
        failure_reason: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["failure_reason", b"failure_reason", "file_names", b"file_names", "success", b"success"]) -> None: ...

global___ListInferenceJobFilesResponse = ListInferenceJobFilesResponse

class CreateInferenceTaskExecutorRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TASK_EXECUTOR_CONFIGURATION_FIELD_NUMBER: builtins.int
    INFERENCE_TASK_CONFIGURATION_FIELD_NUMBER: builtins.int
    @property
    def task_executor_configuration(self) -> global___TaskExecutorConfigurationMessage: ...
    @property
    def inference_task_configuration(self) -> global___InferenceTaskConfigurationMessage: ...
    def __init__(
        self,
        *,
        task_executor_configuration: global___TaskExecutorConfigurationMessage | None = ...,
        inference_task_configuration: global___InferenceTaskConfigurationMessage | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["inference_task_configuration", b"inference_task_configuration", "task_executor_configuration", b"task_executor_configuration"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["inference_task_configuration", b"inference_task_configuration", "task_executor_configuration", b"task_executor_configuration"]) -> None: ...

global___CreateInferenceTaskExecutorRequest = CreateInferenceTaskExecutorRequest

class PrepareInferenceJobRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INFERENCE_JOB_CONFIGURATION_MESSAGE_FIELD_NUMBER: builtins.int
    @property
    def inference_job_configuration_message(self) -> global___InferenceJobConfigurationMessage: ...
    def __init__(
        self,
        *,
        inference_job_configuration_message: global___InferenceJobConfigurationMessage | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["inference_job_configuration_message", b"inference_job_configuration_message"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["inference_job_configuration_message", b"inference_job_configuration_message"]) -> None: ...

global___PrepareInferenceJobRequest = PrepareInferenceJobRequest

class PrepareInferenceJobResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SUCCESS_FIELD_NUMBER: builtins.int
    FAILURE_REASON_FIELD_NUMBER: builtins.int
    success: builtins.bool
    """Whether the request was successful or not"""
    failure_reason: builtins.str
    """The failure description"""
    def __init__(
        self,
        *,
        success: builtins.bool = ...,
        failure_reason: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["failure_reason", b"failure_reason", "success", b"success"]) -> None: ...

global___PrepareInferenceJobResponse = PrepareInferenceJobResponse

class TaskExecutorConfigurationMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INFERENCE_JOB_ID_FIELD_NUMBER: builtins.int
    INFERENCE_TASK_ID_FIELD_NUMBER: builtins.int
    MODEL_IDENTIFIER_FIELD_NUMBER: builtins.int
    IMAGE_URL_FIELD_NUMBER: builtins.int
    BACKOFF_LIMIT_FIELD_NUMBER: builtins.int
    CPU_FIELD_NUMBER: builtins.int
    MEMORY_AMOUNT_FIELD_NUMBER: builtins.int
    MEMORY_UNITS_FIELD_NUMBER: builtins.int
    ENVIRONMENT_ID_FIELD_NUMBER: builtins.int
    CUSTOM_IAM_ROLE_ARN_FIELD_NUMBER: builtins.int
    JOB_SIZE_FIELD_NUMBER: builtins.int
    PURCHASE_OPTION_FIELD_NUMBER: builtins.int
    IMAGE_PULL_SECRET_FIELD_NUMBER: builtins.int
    inference_job_id: builtins.str
    """The id of the inference job"""
    inference_task_id: builtins.str
    """The id of the current inference task"""
    @property
    def model_identifier(self) -> global___ModelIdentifier:
        """Model details"""
    image_url: builtins.str
    """The image url to use"""
    backoff_limit: builtins.int
    """How many times the current task can fail"""
    cpu: builtins.float
    """Cpu usage"""
    memory_amount: builtins.int
    """Memory usage"""
    memory_units: global___MemoryUnitApi.ValueType
    """Units type of memory"""
    environment_id: builtins.str
    custom_iam_role_arn: builtins.str
    @property
    def job_size(self) -> global___BatchJobResources: ...
    purchase_option: builtins.str
    """Whether it is spot/ondemand (default - spot)"""
    image_pull_secret: builtins.str
    """If the image saved in out source repository (jfrog e.g.)  and image pull secret is needed"""
    def __init__(
        self,
        *,
        inference_job_id: builtins.str = ...,
        inference_task_id: builtins.str = ...,
        model_identifier: global___ModelIdentifier | None = ...,
        image_url: builtins.str = ...,
        backoff_limit: builtins.int = ...,
        cpu: builtins.float = ...,
        memory_amount: builtins.int = ...,
        memory_units: global___MemoryUnitApi.ValueType = ...,
        environment_id: builtins.str = ...,
        custom_iam_role_arn: builtins.str = ...,
        job_size: global___BatchJobResources | None = ...,
        purchase_option: builtins.str = ...,
        image_pull_secret: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["job_size", b"job_size", "model_identifier", b"model_identifier"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["backoff_limit", b"backoff_limit", "cpu", b"cpu", "custom_iam_role_arn", b"custom_iam_role_arn", "environment_id", b"environment_id", "image_pull_secret", b"image_pull_secret", "image_url", b"image_url", "inference_job_id", b"inference_job_id", "inference_task_id", b"inference_task_id", "job_size", b"job_size", "memory_amount", b"memory_amount", "memory_units", b"memory_units", "model_identifier", b"model_identifier", "purchase_option", b"purchase_option"]) -> None: ...

global___TaskExecutorConfigurationMessage = TaskExecutorConfigurationMessage

class InferenceJobConfigurationMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INFERENCE_JOB_ID_FIELD_NUMBER: builtins.int
    ENVIRONMENT_ID_FIELD_NUMBER: builtins.int
    CUSTOM_IAM_ROLE_ARN_FIELD_NUMBER: builtins.int
    inference_job_id: builtins.str
    """The id of the inference job"""
    environment_id: builtins.str
    """Environment id"""
    custom_iam_role_arn: builtins.str
    """Custom IAm role"""
    def __init__(
        self,
        *,
        inference_job_id: builtins.str = ...,
        environment_id: builtins.str = ...,
        custom_iam_role_arn: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["custom_iam_role_arn", b"custom_iam_role_arn", "environment_id", b"environment_id", "inference_job_id", b"inference_job_id"]) -> None: ...

global___InferenceJobConfigurationMessage = InferenceJobConfigurationMessage

class ModelIdentifier(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MODEL_ID_FIELD_NUMBER: builtins.int
    BUILD_ID_FIELD_NUMBER: builtins.int
    BRANCH_ID_FIELD_NUMBER: builtins.int
    MODEL_UUID_FIELD_NUMBER: builtins.int
    model_id: builtins.str
    build_id: builtins.str
    branch_id: builtins.str
    model_uuid: builtins.str
    def __init__(
        self,
        *,
        model_id: builtins.str = ...,
        build_id: builtins.str = ...,
        branch_id: builtins.str = ...,
        model_uuid: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["branch_id", b"branch_id", "build_id", b"build_id", "model_id", b"model_id", "model_uuid", b"model_uuid"]) -> None: ...

global___ModelIdentifier = ModelIdentifier

class InferenceTaskConfigurationMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SOURCE_BUCKET_FIELD_NUMBER: builtins.int
    DESTINATION_BUCKET_FIELD_NUMBER: builtins.int
    FILEPATH_FIELD_NUMBER: builtins.int
    DESTINATION_PATH_FIELD_NUMBER: builtins.int
    INPUT_FILE_TYPE_FIELD_NUMBER: builtins.int
    OUTPUT_FILE_TYPE_FIELD_NUMBER: builtins.int
    TOKEN_SECRET_FIELD_NUMBER: builtins.int
    SECRET_SECRET_FIELD_NUMBER: builtins.int
    PARAMETERS_FIELD_NUMBER: builtins.int
    CLOUD_PROVIDER_FIELD_NUMBER: builtins.int
    source_bucket: builtins.str
    """The source bucket in cloud storage"""
    destination_bucket: builtins.str
    """The destination bucket in cloud storage"""
    filepath: builtins.str
    """The full file path to process"""
    destination_path: builtins.str
    """The destination path to save results to"""
    input_file_type: global___InputFileType.ValueType
    """The input file type"""
    output_file_type: global___OutputFileType.ValueType
    """The output file type"""
    token_secret: builtins.str
    """The qwak secret the bucket's token is stored in"""
    secret_secret: builtins.str
    """The qwak secret the bucket's secret is stored in"""
    @property
    def parameters(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___BatchJobParameter]:
        """User provided parameters which will be passed to the batch execution job as environment variables"""
    cloud_provider: global___CloudProvider.ValueType
    """The cloud provider"""
    def __init__(
        self,
        *,
        source_bucket: builtins.str = ...,
        destination_bucket: builtins.str = ...,
        filepath: builtins.str = ...,
        destination_path: builtins.str = ...,
        input_file_type: global___InputFileType.ValueType = ...,
        output_file_type: global___OutputFileType.ValueType = ...,
        token_secret: builtins.str = ...,
        secret_secret: builtins.str = ...,
        parameters: collections.abc.Iterable[global___BatchJobParameter] | None = ...,
        cloud_provider: global___CloudProvider.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["cloud_provider", b"cloud_provider", "destination_bucket", b"destination_bucket", "destination_path", b"destination_path", "filepath", b"filepath", "input_file_type", b"input_file_type", "output_file_type", b"output_file_type", "parameters", b"parameters", "secret_secret", b"secret_secret", "source_bucket", b"source_bucket", "token_secret", b"token_secret"]) -> None: ...

global___InferenceTaskConfigurationMessage = InferenceTaskConfigurationMessage

class BatchJobParameter(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEY_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    key: builtins.str
    value: builtins.str
    def __init__(
        self,
        *,
        key: builtins.str = ...,
        value: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

global___BatchJobParameter = BatchJobParameter

class CleanInferenceTasksExecutorsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INFERENCE_JOB_ID_FIELD_NUMBER: builtins.int
    inference_job_id: builtins.str
    """The id of the inference job"""
    def __init__(
        self,
        *,
        inference_job_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["inference_job_id", b"inference_job_id"]) -> None: ...

global___CleanInferenceTasksExecutorsRequest = CleanInferenceTasksExecutorsRequest

class CleanInferenceTasksExecutorsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SUCCESS_FIELD_NUMBER: builtins.int
    FAILURE_REASON_FIELD_NUMBER: builtins.int
    success: builtins.bool
    """Whether the request was successful or not"""
    failure_reason: builtins.str
    """The failure description"""
    def __init__(
        self,
        *,
        success: builtins.bool = ...,
        failure_reason: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["failure_reason", b"failure_reason", "success", b"success"]) -> None: ...

global___CleanInferenceTasksExecutorsResponse = CleanInferenceTasksExecutorsResponse

class CleanInferenceTaskExecutorRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INFERENCE_JOB_ID_FIELD_NUMBER: builtins.int
    INFERENCE_TASK_ID_FIELD_NUMBER: builtins.int
    inference_job_id: builtins.str
    """The id of the inference job"""
    inference_task_id: builtins.str
    """The id of the inference task"""
    def __init__(
        self,
        *,
        inference_job_id: builtins.str = ...,
        inference_task_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["inference_job_id", b"inference_job_id", "inference_task_id", b"inference_task_id"]) -> None: ...

global___CleanInferenceTaskExecutorRequest = CleanInferenceTaskExecutorRequest

class CleanInferenceTaskExecutorResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SUCCESS_FIELD_NUMBER: builtins.int
    FAILURE_REASON_FIELD_NUMBER: builtins.int
    success: builtins.bool
    """Whether the request was successful or not"""
    failure_reason: builtins.str
    """The failure description"""
    def __init__(
        self,
        *,
        success: builtins.bool = ...,
        failure_reason: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["failure_reason", b"failure_reason", "success", b"success"]) -> None: ...

global___CleanInferenceTaskExecutorResponse = CleanInferenceTaskExecutorResponse

class CreateInferenceTaskExecutorResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SUCCESS_FIELD_NUMBER: builtins.int
    FAILURE_REASON_FIELD_NUMBER: builtins.int
    success: builtins.bool
    """Whether the request was successful or not"""
    failure_reason: builtins.str
    """The failure description"""
    def __init__(
        self,
        *,
        success: builtins.bool = ...,
        failure_reason: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["failure_reason", b"failure_reason", "success", b"success"]) -> None: ...

global___CreateInferenceTaskExecutorResponse = CreateInferenceTaskExecutorResponse

class StartInferenceJobWarmupRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MODEL_ID_FIELD_NUMBER: builtins.int
    BRANCH_ID_FIELD_NUMBER: builtins.int
    BUILD_ID_FIELD_NUMBER: builtins.int
    IMAGE_URL_FIELD_NUMBER: builtins.int
    CPU_FIELD_NUMBER: builtins.int
    MEMORY_AMOUNT_FIELD_NUMBER: builtins.int
    MEMORY_UNITS_FIELD_NUMBER: builtins.int
    EXECUTORS_FIELD_NUMBER: builtins.int
    TIMEOUT_FIELD_NUMBER: builtins.int
    JOB_SIZE_FIELD_NUMBER: builtins.int
    MODEL_UUID_FIELD_NUMBER: builtins.int
    IMAGE_PULL_SECRET_FIELD_NUMBER: builtins.int
    model_id: builtins.str
    """Model details"""
    branch_id: builtins.str
    """branch id"""
    build_id: builtins.str
    """Build Id"""
    image_url: builtins.str
    """The image url to use"""
    cpu: builtins.float
    """Cpu usage"""
    memory_amount: builtins.int
    """Memory usage"""
    memory_units: global___MemoryUnitApi.ValueType
    """Units type of memory"""
    executors: builtins.int
    """Number of executors"""
    timeout: builtins.int
    """Warmup timeout in seconds"""
    @property
    def job_size(self) -> global___BatchJobResources: ...
    model_uuid: builtins.str
    image_pull_secret: builtins.str
    """Image pull secret"""
    def __init__(
        self,
        *,
        model_id: builtins.str = ...,
        branch_id: builtins.str = ...,
        build_id: builtins.str = ...,
        image_url: builtins.str = ...,
        cpu: builtins.float = ...,
        memory_amount: builtins.int = ...,
        memory_units: global___MemoryUnitApi.ValueType = ...,
        executors: builtins.int = ...,
        timeout: builtins.int = ...,
        job_size: global___BatchJobResources | None = ...,
        model_uuid: builtins.str = ...,
        image_pull_secret: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["job_size", b"job_size"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["branch_id", b"branch_id", "build_id", b"build_id", "cpu", b"cpu", "executors", b"executors", "image_pull_secret", b"image_pull_secret", "image_url", b"image_url", "job_size", b"job_size", "memory_amount", b"memory_amount", "memory_units", b"memory_units", "model_id", b"model_id", "model_uuid", b"model_uuid", "timeout", b"timeout"]) -> None: ...

global___StartInferenceJobWarmupRequest = StartInferenceJobWarmupRequest

class StartInferenceJobWarmupResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___StartInferenceJobWarmupResponse = StartInferenceJobWarmupResponse

class CancelInferenceJobWarmupRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MODEL_ID_FIELD_NUMBER: builtins.int
    BRANCH_ID_FIELD_NUMBER: builtins.int
    BUILD_ID_FIELD_NUMBER: builtins.int
    MODEL_UUID_FIELD_NUMBER: builtins.int
    model_id: builtins.str
    branch_id: builtins.str
    build_id: builtins.str
    model_uuid: builtins.str
    def __init__(
        self,
        *,
        model_id: builtins.str = ...,
        branch_id: builtins.str = ...,
        build_id: builtins.str = ...,
        model_uuid: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["branch_id", b"branch_id", "build_id", b"build_id", "model_id", b"model_id", "model_uuid", b"model_uuid"]) -> None: ...

global___CancelInferenceJobWarmupRequest = CancelInferenceJobWarmupRequest

class CancelInferenceJobWarmupResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___CancelInferenceJobWarmupResponse = CancelInferenceJobWarmupResponse

class BatchJobResources(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NUMBER_OF_PODS_FIELD_NUMBER: builtins.int
    CPU_FIELD_NUMBER: builtins.int
    MEMORY_AMOUNT_FIELD_NUMBER: builtins.int
    MEMORY_UNITS_FIELD_NUMBER: builtins.int
    GPU_RESOURCES_FIELD_NUMBER: builtins.int
    number_of_pods: builtins.int
    """Number of pods to deploy"""
    cpu: builtins.float
    """Cpu"""
    memory_amount: builtins.int
    """Amount of memory"""
    memory_units: global___MemoryUnitApi.ValueType
    """Units type of memory"""
    @property
    def gpu_resources(self) -> global___GpuResources:
        """Optional GPU resources for batch"""
    def __init__(
        self,
        *,
        number_of_pods: builtins.int = ...,
        cpu: builtins.float = ...,
        memory_amount: builtins.int = ...,
        memory_units: global___MemoryUnitApi.ValueType = ...,
        gpu_resources: global___GpuResources | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["gpu_resources", b"gpu_resources"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["cpu", b"cpu", "gpu_resources", b"gpu_resources", "memory_amount", b"memory_amount", "memory_units", b"memory_units", "number_of_pods", b"number_of_pods"]) -> None: ...

global___BatchJobResources = BatchJobResources

class GpuResources(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    GPU_TYPE_FIELD_NUMBER: builtins.int
    GPU_AMOUNT_FIELD_NUMBER: builtins.int
    gpu_type: global___GpuType.ValueType
    """The type of the GPU"""
    gpu_amount: builtins.int
    """Amount of GPUs"""
    def __init__(
        self,
        *,
        gpu_type: global___GpuType.ValueType = ...,
        gpu_amount: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["gpu_amount", b"gpu_amount", "gpu_type", b"gpu_type"]) -> None: ...

global___GpuResources = GpuResources
