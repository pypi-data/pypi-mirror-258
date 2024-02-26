# coding: utf-8

# flake8: noqa

"""
    Harmony Endpoint Management API

    <h2>Today more than ever, endpoint security plays a critical role in enabling your remote workforce.</h2> <h4>Harmony Endpoint provides comprehensive endpoint protection at the highest security level that is crucial to avoid  security breaches and data compromise.</h4> <p>The following documentation provides the operations supported by the Harmony Endpoint's External API.</p> <p>To use the Harmony Endpoint External API service:</p> <ol>  <li>   <p>In the <em>Infinity Portal</em>, create a suitable API Key. In the <em>Service</em> field, enter <em>Endpoint</em>.</br>    For more information, refer to the <a     href=\"https://sc1.checkpoint.com/documents/Infinity_Portal/WebAdminGuides/EN/Infinity-Portal-Admin-Guide/Content/Topics-Infinity-Portal/API-Keys.htm?tocpath=Global%20Settings%7C_____7#API_Keys\">Infinity     Portal Administration Guide</a>.     </br>Once a key has been created, it may be used indefinitely (unless an    expiration date was explicitly set for it).</p>   During the key's creation, note the presented <em>Authentication URL</em>. This URL is used to obtain <em>Bearer    tokens</em> for the next step  </li>  <li>   <p>Authenticate using the <em>Infinity Portal's</em> External Authentication Service.<br />The authentication    request should be made to the <em>Authentication URL</em> obtained during the previous step.</p>   <p>Example (<em>Your tenant's authentication URL may differ</em>):</p>   <p><img     src=\"data:image/png;base64,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\" />   </p>  </li>  <li>   <p>Include the resulting <em>token</em> in the <em>Authorization</em> header in the form of a <em>Bearer</em>    (For example, 'Authorization': 'Bearer {TOKEN}') in every request made to the API service</p>  </li>  <li>   <p>Call the <a href=\"#/Session/LoginCloud\">Cloud Login API</a></p>  </li>  <li>   <p>Include the resulting <em>x-mgmt-api-token</em> in Header <em>x-mgmt-api-token</em> of all subsequent    requests</p>  </li> </ol>  # noqa: E501

    The version of the OpenAPI document: 1.9.179
    Contact: harmony-endpoint-external-api@checkpoint.com
    Generated by: https://openapi-generator.tech
"""

__version__ = "1.0.0"

# import ApiClient
from chkp_harmony_endpoint_management_sdk.generated.cloud.api_client import ApiClient

# import Configuration
from chkp_harmony_endpoint_management_sdk.generated.cloud.configuration import Configuration

# import exceptions
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import OpenApiException
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiAttributeError
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiTypeError
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiValueError
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiKeyError
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiException

from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiException

# Code generation part of HarmonyEndpoint

import json
from chkp_harmony_endpoint_management_sdk.core.logger import logger
from chkp_harmony_endpoint_management_sdk.classes.sdk_connection_state import SDKConnectionState
from chkp_harmony_endpoint_management_sdk.classes.harmony_endpoint_sdk_info import HarmonyEndpointSDKInfo
from chkp_harmony_endpoint_management_sdk.generated.cloud.sdk_build import sdk_build_info

from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_asset_management_computers_filtered.post import ComputersByFilter
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_ioc_create.post import CreateIoc
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_ioc_delete_all.delete import DeleteAllIoc
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_ioc_delete.delete import DeleteIocByIds
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_ioc_edit.put import EditIoc
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_ioc_get.post import GetIocPaged
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_jobs_job_id.get import GetJobById
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_organization_virtual_group_virtual_group_id_members_add.put import AddMembersToVirtualGroup
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_organization_virtual_group_create.post import Create
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_organization_virtual_group_virtual_group_id_members_remove.put import RemoveMembersFromVirtualGroup
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_organization_tree_search.post import SearchInOrganization
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_rule_id_assignments_add.put import AddRuleAssignments
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_metadata.get import GetAllRulesMetadata
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_rule_id_modifications.get import GetModificationsPendingInstallationByRuleId
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_rule_id_assignments.get import GetRuleAssignments
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_rule_id_metadata.get import GetRuleMetadataById
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_install.post import InstallAllPolicies
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_rule_id_install.post import InstallPoliciesForRule
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_policy_rule_id_assignments_remove.put import RemoveRuleAssignments
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_registry_key_add.post import AgentAddRegistryKey
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_vpn_site_add.post import AgentAddVpnSite
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_process_information.post import AgentCollectProcessInformation
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_file_copy.post import AgentCopyFile
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_file_delete.post import AgentDeleteFile
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_file_move.post import AgentMoveFile
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_registry_key_delete.post import AgentRemoveRegistryKey
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_vpn_site_remove.post import AgentRemoveVpnSite
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_process_terminate.post import AgentTerminateProcess
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_collect_logs.post import CollectLogs
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_repair_computer.post import RepairComputer
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_reset_computer.post import ResetComputer
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_agent_shutdown_computer.post import ShutdownComputer
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_id_abort.post import AbortRemediationOperationById
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_status.get import GetAllRemediationOperationStatuses
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_id_results_slim.post import GetRemediationOperationSlimResultsById
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_id_status.get import GetRemediationOperationStatusById
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_analyze_by_indicator_file_name.post import AnalyzeByFileName
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_analyze_by_indicator_ip.post import AnalyzeByIp
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_analyze_by_indicator_md5.post import AnalyzeByMd5
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_analyze_by_indicator_path.post import AnalyzeByPath
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_analyze_by_indicator_url.post import AnalyzeByUrl
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_anti_malware_restore.post import AntiMalwareRestore
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_anti_malware_scan.post import AntiMalwareScan
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_anti_malware_update.post import AntiMalwareUpdate
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_de_isolate.post import DeIsolateComputer
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_isolate.post import IsolateComputer
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_file_quarantine.post import QuarantineFile
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_remediation_forensics_file_restore.post import RestoreQuarantinedFile
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_session_keepalive.post import KeepAlive
from chkp_harmony_endpoint_management_sdk.generated.cloud.paths.v1_session_login_cloud.post import LoginCloud

client = ApiClient()

class AssetManagementApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def computers_by_filter(self):
        return ComputersByFilter(self.__session_manager.client).computers_by_filter

class IndicatorsOfCompromiseApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def create_ioc(self):
        return CreateIoc(self.__session_manager.client).create_ioc

    @property
    def delete_all_ioc(self):
        return DeleteAllIoc(self.__session_manager.client).delete_all_ioc

    @property
    def delete_ioc_by_ids(self):
        return DeleteIocByIds(self.__session_manager.client).delete_ioc_by_ids

    @property
    def edit_ioc(self):
        return EditIoc(self.__session_manager.client).edit_ioc

    @property
    def get_ioc_paged(self):
        return GetIocPaged(self.__session_manager.client).get_ioc_paged

class JobsApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def get_job_by_id(self):
        return GetJobById(self.__session_manager.client).get_job_by_id

class OrganizationalStructureApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def add_members_to_virtual_group(self):
        return AddMembersToVirtualGroup(self.__session_manager.client).add_members_to_virtual_group

    @property
    def create(self):
        return Create(self.__session_manager.client).create

    @property
    def remove_members_from_virtual_group(self):
        return RemoveMembersFromVirtualGroup(self.__session_manager.client).remove_members_from_virtual_group

    @property
    def search_in_organization(self):
        return SearchInOrganization(self.__session_manager.client).search_in_organization

class PolicyGeneralApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def add_rule_assignments(self):
        return AddRuleAssignments(self.__session_manager.client).add_rule_assignments

    @property
    def get_all_rules_metadata(self):
        return GetAllRulesMetadata(self.__session_manager.client).get_all_rules_metadata

    @property
    def get_modifications_pending_installation_by_rule_id(self):
        return GetModificationsPendingInstallationByRuleId(self.__session_manager.client).get_modifications_pending_installation_by_rule_id

    @property
    def get_rule_assignments(self):
        return GetRuleAssignments(self.__session_manager.client).get_rule_assignments

    @property
    def get_rule_metadata_by_id(self):
        return GetRuleMetadataById(self.__session_manager.client).get_rule_metadata_by_id

    @property
    def install_all_policies(self):
        return InstallAllPolicies(self.__session_manager.client).install_all_policies

    @property
    def install_policies_for_rule(self):
        return InstallPoliciesForRule(self.__session_manager.client).install_policies_for_rule

    @property
    def remove_rule_assignments(self):
        return RemoveRuleAssignments(self.__session_manager.client).remove_rule_assignments

class RemediationResponseAgentApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def agent_add_registry_key(self):
        return AgentAddRegistryKey(self.__session_manager.client).agent_add_registry_key

    @property
    def agent_add_vpn_site(self):
        return AgentAddVpnSite(self.__session_manager.client).agent_add_vpn_site

    @property
    def agent_collect_process_information(self):
        return AgentCollectProcessInformation(self.__session_manager.client).agent_collect_process_information

    @property
    def agent_copy_file(self):
        return AgentCopyFile(self.__session_manager.client).agent_copy_file

    @property
    def agent_delete_file(self):
        return AgentDeleteFile(self.__session_manager.client).agent_delete_file

    @property
    def agent_move_file(self):
        return AgentMoveFile(self.__session_manager.client).agent_move_file

    @property
    def agent_remove_registry_key(self):
        return AgentRemoveRegistryKey(self.__session_manager.client).agent_remove_registry_key

    @property
    def agent_remove_vpn_site(self):
        return AgentRemoveVpnSite(self.__session_manager.client).agent_remove_vpn_site

    @property
    def agent_terminate_process(self):
        return AgentTerminateProcess(self.__session_manager.client).agent_terminate_process

    @property
    def collect_logs(self):
        return CollectLogs(self.__session_manager.client).collect_logs

    @property
    def repair_computer(self):
        return RepairComputer(self.__session_manager.client).repair_computer

    @property
    def reset_computer(self):
        return ResetComputer(self.__session_manager.client).reset_computer

    @property
    def shutdown_computer(self):
        return ShutdownComputer(self.__session_manager.client).shutdown_computer

class RemediationResponseGeneralApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def abort_remediation_operation_by_id(self):
        return AbortRemediationOperationById(self.__session_manager.client).abort_remediation_operation_by_id

    @property
    def get_all_remediation_operation_statuses(self):
        return GetAllRemediationOperationStatuses(self.__session_manager.client).get_all_remediation_operation_statuses

    @property
    def get_remediation_operation_slim_results_by_id(self):
        return GetRemediationOperationSlimResultsById(self.__session_manager.client).get_remediation_operation_slim_results_by_id

    @property
    def get_remediation_operation_status_by_id(self):
        return GetRemediationOperationStatusById(self.__session_manager.client).get_remediation_operation_status_by_id

class RemediationResponseThreatPreventionApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def analyze_by_file_name(self):
        return AnalyzeByFileName(self.__session_manager.client).analyze_by_file_name

    @property
    def analyze_by_ip(self):
        return AnalyzeByIp(self.__session_manager.client).analyze_by_ip

    @property
    def analyze_by_md5(self):
        return AnalyzeByMd5(self.__session_manager.client).analyze_by_md5

    @property
    def analyze_by_path(self):
        return AnalyzeByPath(self.__session_manager.client).analyze_by_path

    @property
    def analyze_by_url(self):
        return AnalyzeByUrl(self.__session_manager.client).analyze_by_url

    @property
    def anti_malware_restore(self):
        return AntiMalwareRestore(self.__session_manager.client).anti_malware_restore

    @property
    def anti_malware_scan(self):
        return AntiMalwareScan(self.__session_manager.client).anti_malware_scan

    @property
    def anti_malware_update(self):
        return AntiMalwareUpdate(self.__session_manager.client).anti_malware_update

    @property
    def de_isolate_computer(self):
        return DeIsolateComputer(self.__session_manager.client).de_isolate_computer

    @property
    def isolate_computer(self):
        return IsolateComputer(self.__session_manager.client).isolate_computer

    @property
    def quarantine_file(self):
        return QuarantineFile(self.__session_manager.client).quarantine_file

    @property
    def restore_quarantined_file(self):
        return RestoreQuarantinedFile(self.__session_manager.client).restore_quarantined_file

class SessionApi():
    def __init__(self, session_manager):
        self.__session_manager = session_manager

    @property
    def keep_alive(self):
        return KeepAlive(self.__session_manager.client).keep_alive

    @property
    def login_cloud(self):
        return LoginCloud(self.__session_manager.client).login_cloud



class HarmonyEndpointBase:
    
    @staticmethod
    def info() -> HarmonyEndpointSDKInfo:
        return sdk_build_info()

    def __init__(self, instance_schema: str, session_manager):
        logger(f'A new instance "{instance_schema}" of sdk created, full version info: {HarmonyEndpointBase.info()}')
        self._session_manager = session_manager


    def disconnect(self):
        self._session_manager.disconnect()

    def reconnect(self):
        self._session_manager.reconnect()

    def connection_state(self) -> SDKConnectionState:
        self._session_manager.connection_state()


    @property
    def asset_management_api(self):
        return AssetManagementApi(self._session_manager)

    @property
    def indicators_of_compromise_api(self):
        return IndicatorsOfCompromiseApi(self._session_manager)

    @property
    def jobs_api(self):
        return JobsApi(self._session_manager)

    @property
    def organizational_structure_api(self):
        return OrganizationalStructureApi(self._session_manager)

    @property
    def policy_general_api(self):
        return PolicyGeneralApi(self._session_manager)

    @property
    def remediation_response_agent_api(self):
        return RemediationResponseAgentApi(self._session_manager)

    @property
    def remediation_response_general_api(self):
        return RemediationResponseGeneralApi(self._session_manager)

    @property
    def remediation_response_threat_prevention_api(self):
        return RemediationResponseThreatPreventionApi(self._session_manager)

    @property
    def _session_api(self):
        return SessionApi(self._session_manager)

