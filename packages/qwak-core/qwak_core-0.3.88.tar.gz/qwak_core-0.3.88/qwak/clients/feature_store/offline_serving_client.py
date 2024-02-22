import logging
from typing import List, Optional

from _qwak_proto.qwak.offline.serving.v1.feature_values_pb2 import (
    FeaturesetFeatures as ProtoFeaturesetFeatures,
)
from _qwak_proto.qwak.offline.serving.v1.offline_serving_async_service_pb2 import (
    FeatureValuesRequestStatus as ProtoFeatureValuesRequestStatus,
    FileFormat as ProtoFileFormat,
    GetFeatureValuesInRangeRequest as ProtoGetFeatureValuesInRangeRequest,
    GetFeatureValuesInRangeResponse as ProtoGetFeatureValuesInRangeResponse,
    GetFeatureValuesRequest as ProtoGetFeatureValuesRequest,
    GetFeatureValuesResponse as ProtoGetFeatureValuesResponse,
    GetFeatureValuesResultRequest as ProtoGetFeatureValuesResultRequest,
    GetFeatureValuesResultResponse as ProtoGetFeatureValuesResultResponse,
    GetFileUploadUrlRequest as ProtoGetFileUploadUrlRequest,
    GetFileUploadUrlResponse as ProtoGetFileUploadUrlResponse,
)
from _qwak_proto.qwak.offline.serving.v1.offline_serving_async_service_pb2_grpc import (
    FeatureStoreOfflineServingAsyncServiceStub,
)
from _qwak_proto.qwak.offline.serving.v1.population_pb2 import (
    Population as ProtoPopulation,
    PopulationFileUploadUrlType as ProtoPopulationFileUploadUrlType,
    TimedPopulation as ProtoTimedPopulation,
)
from dependency_injector.wiring import Provide
from google.protobuf.timestamp_pb2 import Timestamp as ProtoTimestamp
from qwak.inner.di_configuration import QwakContainer
from qwak.inner.tool.retry_utils import retry


class FeatureValuesResultNotReadyException(Exception):
    pass


class FeatureValuesTimeoutException(Exception):
    pass


class FsOfflineServingClient:
    """
    Querying offline features store
    """

    def __init__(self, grpc_channel=Provide[QwakContainer.core_grpc_channel]):
        self._client = FeatureStoreOfflineServingAsyncServiceStub(grpc_channel)

    def get_population_file_upload_url(
        self,
    ) -> str:
        """
        Generating population file upload url
        :return: pre-signed url to upload population data
        """

        request: ProtoGetFileUploadUrlRequest = ProtoGetFileUploadUrlRequest(
            population=ProtoPopulationFileUploadUrlType()
        )

        response: ProtoGetFileUploadUrlResponse = self._client.GetFileUploadUrl(request)
        return response.file_upload_url

    def get_feature_values(
        self,
        features: List[ProtoFeaturesetFeatures],
        population: ProtoTimedPopulation,
        result_file_format: ProtoFileFormat,
    ) -> str:
        """
        Getting offline feature values
        :return: Request handle id to poll for result with
        """
        request: ProtoGetFeatureValuesRequest = ProtoGetFeatureValuesRequest(
            features=features,
            population=population,
            result_file_format=result_file_format,
        )

        response: ProtoGetFeatureValuesResponse = self._client.GetFeatureValues(request)
        return response.request_id

    def get_feature_values_in_range(
        self,
        features: ProtoFeaturesetFeatures,
        lower_time_bound: ProtoTimestamp,
        upper_time_bound: ProtoTimestamp,
        result_file_format: ProtoFileFormat,
        population: Optional[ProtoPopulation],
    ) -> str:
        """
        Getting offline feature values
        :return: Request handle id to poll for result with
        """
        request: ProtoGetFeatureValuesInRangeRequest = (
            ProtoGetFeatureValuesInRangeRequest(
                features=features,
                lower_time_bound=lower_time_bound,
                upper_time_bound=upper_time_bound,
                result_file_format=result_file_format,
                population=population,
            )
        )

        response: ProtoGetFeatureValuesInRangeResponse = (
            self._client.GetFeatureValuesInRange(request)
        )
        return response.request_id

    def get_result(self, request_handle: str) -> ProtoGetFeatureValuesResultResponse:
        request: ProtoGetFeatureValuesResultRequest = (
            ProtoGetFeatureValuesResultRequest(request_id=request_handle)
        )

        return self._client.GetFeatureValuesResult(request)

    def _inner_poll(self, request_handle: str) -> ProtoGetFeatureValuesResultResponse:
        """
        This function receives request_handle amd polls for results.

        Args:
            request_handle: request_id for polling

        Returns: if the request status is PENDING it throws FeatureValuesResultNotReadyException.
                 else returns the Feature Values Result
        """
        response: ProtoGetFeatureValuesResultResponse = self.get_result(
            request_handle=request_handle
        )

        if (
            response.status
            == ProtoFeatureValuesRequestStatus.FEATURE_VALUES_REQUEST_STATUS_PENDING
        ):
            logging.info("Feature Values query is still in progress...")
            raise FeatureValuesResultNotReadyException()

        return response

    def poll_for_result(
        self,
        request_handle: str,
        timeout_seconds: int = 60 * 60,
        poll_interval_seconds: int = 10,
    ) -> ProtoGetFeatureValuesResultResponse:
        """
        This function receives request_handle and polls for Feature Values Result.
        it relies on _inner_poll() to raise FeatureValuesResultNotReadyException in case the result is not ready.
        only once the desired amount of attempts completed it raises FeatureValuesTimeoutException
        Args:
            request_handle: request_id
            timeout_seconds: total number of seconds for all attempts before timeout
            poll_interval_seconds: sleep time between attempts

        Returns: Feature Values Result or raises FeatureValuesTimeoutException if attempts exceeded timeout_seconds.

        """
        try:
            result = retry(
                f=self._inner_poll,
                kwargs={"request_handle": request_handle},
                exceptions=FeatureValuesResultNotReadyException,
                attempts=int(timeout_seconds / poll_interval_seconds) + 1,
                delay=poll_interval_seconds,
            )
        except FeatureValuesResultNotReadyException:
            raise FeatureValuesTimeoutException(
                f"Feature values query timed out. Qwak limits query execution time to {int(timeout_seconds / 60)} minutes"
            )

        return result

    def get_feature_values_blocking(
        self,
        features: List[ProtoFeaturesetFeatures],
        population: ProtoTimedPopulation,
        result_file_format: ProtoFileFormat,
        timeout_seconds: int = 60 * 60,
        poll_interval_seconds: int = 10,
    ) -> ProtoGetFeatureValuesResultResponse:
        request_handle: str = self.get_feature_values(
            features=features,
            population=population,
            result_file_format=result_file_format,
        )

        return self.poll_for_result(
            request_handle=request_handle,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
        )

    def get_feature_values_in_range_blocking(
        self,
        features: ProtoFeaturesetFeatures,
        lower_time_bound: ProtoTimestamp,
        upper_time_bound: ProtoTimestamp,
        result_file_format: ProtoFileFormat,
        population: Optional[ProtoPopulation] = None,
        timeout_seconds: int = 60 * 60,
        poll_interval_seconds: int = 10,
    ) -> ProtoGetFeatureValuesResultResponse:
        request_handle: str = self.get_feature_values_in_range(
            features=features,
            lower_time_bound=lower_time_bound,
            upper_time_bound=upper_time_bound,
            population=population,
            result_file_format=result_file_format,
        )

        return self.poll_for_result(
            request_handle=request_handle,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
        )
