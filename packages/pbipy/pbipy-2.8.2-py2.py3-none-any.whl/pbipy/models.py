"""
Module contains Python representations of Power BI objects.

The powerbi.PowerBI() client will attempt to translate API responses into instances 
of these objects.
"""

from dataclasses import dataclass, field
from typing import Optional

from dateutil.parser import parse

from .utils import camel_case_dict_keys


@dataclass(kw_only=True)
class PBIObject:
    raw: dict = field(repr=False, default=None)

    @classmethod
    def from_raw(cls, raw):
        """
        Create an instance of a `PBIObject` from the raw json response
        of an API Endpoint.

        Parameters
        ----------
        `raw` : `dict`
            Raw json response from the API call.

        Returns
        -------
        `PBIObject`
            Instance of a `PBIObject` type. The type returned depends on
            where it was called from.
        """

        kwargs = camel_case_dict_keys(raw)
        return cls(**kwargs, raw=raw)


@dataclass
class Group(PBIObject):
    """A Power BI group. Commonly called a Workspace."""

    id: str

    name: str = None
    type: str = None
    is_read_only: bool = None
    is_on_dedicated_capacity: bool = None
    capacity_id: str = None
    dataflow_storage_id: str = None


@dataclass
class Dataset(PBIObject):
    """A Power BI Dataset."""

    id: str

    name: str = None
    web_url: str = None
    add_rows_api_enabled: bool = None
    is_refreshable: bool = None
    is_effective_identity_required: bool = None
    is_effective_identity_roles_required: bool = None
    is_in_place_sharing_enabled: bool = None
    is_on_prem_gateway_required: bool = None
    target_storage_mode: str = None
    created_date: str = None
    create_report_embed_url: str = None
    qna_embed_url: str = None
    upstream_datasets: list = field(default=None)
    users: list = field(default=None)
    configured_by: str = None

    def __post_init__(self):
        if self.created_date:
            self.created_date = parse(self.created_date)


@dataclass
class Refresh(PBIObject):
    """A Power BI refresh history entry."""

    id: int = None

    request_id: str = None
    refresh_type: str = None
    start_time: str = None
    end_time: str = None
    status: str = None
    service_exception_json: str = None

    def __post_init__(self):
        if self.start_time:
            self.start_time = parse(self.start_time)
        if self.end_time:
            self.end_time = parse(self.end_time)


# TODO: Consider creating subclassess for each subtype.
@dataclass
class ActivityEvent(PBIObject):
    """Power BI Auditing Events.

    Activity Events are audit and tracked activity on the Power BI
    instance. Examples of Activity Events can include: viewing reports,
    refreshing datasets, updating apps, etc.

    While there are many types of Activity Events, pbipy consolidates these
    into an `ActivityEvent` object. Attributes not related to an activity
    type will be set to `None`.
    """

    id: str

    activity: str = None
    activity_id: str = None
    app_dashboard_id: str = None
    app_id: str = None
    app_name: str = None
    app_report_id: str = None
    artifact_id: str = None
    artifact_kind: str = None
    artifact_name: str = None
    client_ip: str = None
    consumption_method: str = None
    creation_time: str = None
    dashboard_id: str = None
    dashboard_name: str = None
    data_connectivity_mode: str = None
    dataflow_access_token_request_parameters: str = None
    dataflow_id: str = None
    dataflow_name: str = None
    dataflow_type: str = None
    dataset_id: str = None
    dataset_name: str = None
    datasets: str = None
    datasource_object_ids: str = None
    distribution_method: str = None
    exported_artifact_info: str = None
    folder_access_requests: str = None
    folder_display_name: str = None
    folder_object_id: str = None
    gateway_id: str = None
    has_full_report_attachment: bool = None
    import_display_name: str = None
    import_id: str = None
    import_source: str = None
    import_type: str = None
    is_success: bool = None
    item_name: str = None
    last_refresh_time: str = None
    model_id: str = None
    models_snapshots: str = None
    monikers: str = None
    object_id: str = None
    operation: str = None
    org_app_permission: str = None
    organization_id: str = None
    record_type: str = None
    refresh_type: str = None
    report_id: str = None
    report_name: str = None
    report_type: int = None
    request_id: str = None
    schedules: str = None
    share_link_id: str = None
    sharing_action: str = None
    sharing_information: str = None
    user_agent: str = None
    user_id: str = None
    user_key: str = None
    user_type: int = None
    work_space_name: str = None
    workload: str = None
    workspace_id: str = None

    def __post_init__(self):
        if self.creation_time:
            self.creation_time = parse(self.creation_time)
        if self.last_refresh_time:
            self.last_refresh_time = parse(self.last_refresh_time)


@dataclass
class DatasetToDataflowLink(PBIObject):
    """A Power BI dataset to dataflow link"""

    dataset_object_id: str
    dataflow_object_id: str
    workspace_object_id: str


@dataclass
class DatasetUserAccess(PBIObject):
    """A Power BI principal access right entry for a dataset."""

    dataset_user_access_right: str
    identifier: str
    principal_type: str


@dataclass
class Datasource(PBIObject):
    """A Power BI data source"""

    datasource_id: str
    datasource_type: str = None
    connection_details: dict = None
    gateway_id: dict = None


@dataclass
class DirectQueryRefreshSchedule(PBIObject):
    """A Power BI refresh schedule for DirectQuery or LiveConnection."""

    days: list = field(default=None)
    frequency: int = None
    local_time_zone_id: str = None
    times: list = field(default=None)


@dataclass
class MashupParameter(PBIObject):
    """A Power BI dataset parameter."""

    current_value: str = None
    is_required: bool = None
    name: str = None
    suggested_values: list = field(default=None)
    type: str = None


@dataclass
class Report(PBIObject):
    """A Power BI report."""

    id: str
    report_type: str = None
    name: str = None
    web_url: str = None
    embed_url: str = None
    is_owned_by_me: bool = None
    dataset_id: str = None
    users: list = field(default=None)
    subscriptions: list = field(default=None)
    app_id: str = None
    description: str = None
    original_report_object_id: str = None


@dataclass
class App(PBIObject):
    """A Power BI App"""

    id: str
    name: str = None
    last_update: str = None
    description: str = None
    published_by: str = None
    workspace_id: str = None
    users: list = field(default=None)

    def __post_init__(self):
        if self.last_update:
            self.last_update = parse(self.last_update)


@dataclass
class Dashboard(PBIObject):
    """A Power BI dashboard."""

    id: str
    app_id: str = None
    display_name: str = None
    embed_url: str = None
    is_read_only: bool = None
    subscriptions: list = field(default=None)
    users: list = field(default=None)
    web_url: str = None


@dataclass
class Tile(PBIObject):
    """A Power BI tile."""

    id: str
    col_span: int = None
    dataset_id: str = None
    embed_data: str = None
    embed_url: str = None
    report_id: str = None
    row_span: int = None
    title: str = None
    sub_title: str = None
