# Copyright (C) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.
import logging
from pprint import pformat
from typing import Any, Dict, List, Optional

import attr

from geti_sdk.data_models.enums import JobState, JobType
from geti_sdk.data_models.project import Dataset
from geti_sdk.data_models.status import StatusSummary
from geti_sdk.data_models.user import User
from geti_sdk.data_models.utils import (
    attr_value_serializer,
    str_to_datetime,
    str_to_enum_converter,
    str_to_optional_enum_converter,
)
from geti_sdk.http_session import GetiRequestException, GetiSession


@attr.define(slots=False)
class JobStatus(StatusSummary):
    """
    Current status of a job on the Intel® Geti™ server.

    :var state: Current state of the job
    """

    state: str = attr.field(converter=str_to_enum_converter(JobState), kw_only=True)

    @classmethod
    def from_dict(cls, status_dict: Dict[str, Any]) -> "JobStatus":
        """
        Create a JobStatus object from a dictionary.

        :param status_dict: Dictionary representing a status, as returned by the
            Intel® Geti™ /status and /jobs endpoints
        :return: JobStatus object holding the status data contained in `status_dict`
        """
        return cls(**status_dict)


@attr.define
class TaskMetadata:
    """
    Metadata related to a task on the Intel® Geti™ cluster.

    :var name: Name of the task
    :var model_template_id: Identifier of the model template used by the task
    :var model_architecture: Name of the neural network architecture used for the model
    :var model_version: Version of the model currently used by the job
    :var dataset_storage_id: Unique database ID of the dataset storage used by the job
    :var task_id: ID of the task to which the TaskStatus object applies. Only used in
        Geti v1.1 and up
    """

    model_architecture: Optional[str] = None
    model_template_id: Optional[str] = None
    model_version: Optional[int] = None
    name: Optional[str] = None
    dataset_storage_id: Optional[str] = None
    task_id: Optional[str] = None  # Added in Geti v1.1


@attr.define
class TestMetadata:
    """
    Metadata related to a model test job on the GETi cluster.

    :var model_template_id: Identifier of the model template used in the test
    :var model_architecture: Name of the neural network architecture used for the model
    :var datasets: List of dictionaries, each dictionary holding the id and name of a
        dataset used in the test
    """

    model_architecture: str
    model_template_id: str
    datasets: List[Dataset]
    model: Optional[dict] = None  # Added in Geti v1.7


@attr.define
class ProjectMetadata:
    """
    Metadata related to a project on the GETi cluster.

    :var name: Name of the project
    :var id: ID of the project
    """

    name: Optional[str] = None
    id: Optional[str] = None


@attr.define
class ModelMetadata:
    """
    Metadata for a Job related to a model on the GETi cluster.

    :var model_storage_id: ID of the model storage in which the model lives
    :var model_id: ID of the model
    """

    model_storage_id: str
    model_id: str


@attr.define
class ScoreMetadata:
    """
    Metadata element containing scores for the tasks in the project

    :var task_id: ID of the task for which the score was achieved
    :var score: Performance score for the model for the task
    """

    task_id: str
    score: float


@attr.define
class JobMetadata:
    """
    Metadata for a particular job on the GETi cluster.

    :var task: TaskMetadata object holding information regarding the task from which
        the job originates
    :var base_model_id: Optional unique database ID of the base model. Only used for
        optimization jobs
    :var model_storage_id: Optional unique database ID of the model storage used by
        the job.
    :var optimization_type: Optional type of the optimization method used in the job.
        Only used for optimization jobs
    :var optimized_model_id: Optional unique database ID of the optimized model
        produced by the job. Only used for optimization jobs.
    :var scores: List of scores for the job. Added in Geti v1.1
    """

    task: Optional[TaskMetadata] = None
    project: Optional[ProjectMetadata] = None
    test: Optional[TestMetadata] = None
    base_model_id: Optional[str] = None
    model_storage_id: Optional[str] = None
    optimization_type: Optional[str] = None
    optimized_model_id: Optional[str] = None
    scores: Optional[List[ScoreMetadata]] = None
    trained_model: Optional[ModelMetadata] = None  # Added in Geti v1.7


@attr.define
class JobCancellationInfo:
    """
    Information relating to the cancellation of a Job in Intel Geti

    :var is_cancelled: True if the job is cancelled, False otherwise
    :var user_uid: Unique ID of the User who cancelled the Job
    :var cancel_time: Time at which the Job was cancelled
    """

    is_cancelled: bool = False
    user_uid: Optional[str] = None
    cancel_time: Optional[str] = attr.field(converter=str_to_datetime, default=None)


@attr.define(slots=False)
class Job:
    """
    Representation of a job running on the GETi cluster.

    :var name: Name of the job
    :var description: Description of the job
    :var id: Unique database ID of the job
    :var project_id: Unique database ID of the project from which the job originates
    :var status: JobStatus object holding the current status of the job
    :var type: Type of the job
    :var metadata: JobMetadata object holding metadata for the job
    """

    name: str
    description: str
    id: str
    status: JobStatus
    type: str = attr.field(converter=str_to_enum_converter(JobType))
    metadata: JobMetadata
    project_id: Optional[str] = None
    creation_time: Optional[str] = attr.field(converter=str_to_datetime, default=None)
    start_time: Optional[str] = attr.field(
        converter=str_to_datetime, default=None
    )  # Added in Geti v1.7
    end_time: Optional[str] = attr.field(
        converter=str_to_datetime, default=None
    )  # Added in Geti v1.7
    author: Optional[User] = None  # Added in Geti v1.7
    cancellation_info: Optional[JobCancellationInfo] = None  # Added in Geti v1.7
    state: Optional[str] = attr.field(
        converter=str_to_optional_enum_converter(JobState), default=None
    )  # Added in Geti v1.7
    steps: Optional[List[dict]] = None  # Added in Geti v1.7

    def __attrs_post_init__(self):
        """
        Initialize private attributes.
        """
        self._workspace_id: Optional[str] = None

    @property
    def workspace_id(self) -> str:
        """
        Return the unique database ID of the workspace to which the job belongs.

        :return: Unique database ID of the workspace to which the job belongs
        """
        if self._workspace_id is None:
            raise ValueError(
                f"Workspace ID for job {self} is unknown, it was never set."
            )
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id: str):
        """
        Set the workspace id for the job.

        :param workspace_id: Unique database ID of the workspace to which the job
            belongs
        """
        self._workspace_id = workspace_id

    @property
    def relative_url(self) -> str:
        """
        Return the url at which the Job can be addressed on the GETi cluster, relative
        to the url of the cluster itself.

        :return: Relative url for the Job instance
        """
        return f"workspaces/{self.workspace_id}/jobs/{self.id}"

    def update(self, session: GetiSession) -> "Job":
        """
        Update the job status to its current value, by making a request to the GETi
        cluster addressed by `session`.

        :param session: GetiSession to the cluster from which the Job originates
        :raises ValueError: If no workspace_id has been set for the job prior to
            calling this method
        :return: Job with its status updated
        """
        response = session.get_rest_response(url=self.relative_url, method="GET")
        updated_status = JobStatus.from_dict(response["status"])
        self.status = updated_status
        self.state = updated_status.state
        return self

    def cancel(self, session: GetiSession) -> "Job":
        """
        Cancel and delete the job, by making a request to the GETi cluster addressed
        by `session`.

        :param session: GetiSession to the cluster on which the Job is running
        :return: Job with updated status
        """
        try:
            session.get_rest_response(url=self.relative_url, method="DELETE")
            self.status.state = JobState.CANCELLED
        except GetiRequestException as error:
            if error.status_code == 404:
                logging.info(
                    f"Job '{self.name}' is not active anymore, unable to delete."
                )
                self.status.state = JobState.INACTIVE
            else:
                raise error
        return self

    @property
    def overview(self) -> str:
        """
        Return a string that shows an overview of the job.

        :return: String holding an overview of the job
        """
        return pformat(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        """
        Return the dictionary representation of the job.

        :return:
        """
        return attr.asdict(self, recurse=True, value_serializer=attr_value_serializer)

    @property
    def is_finished(self) -> bool:
        """
        Return True if the job finished successfully, False otherwise
        """
        return self.status.state == JobState.FINISHED
