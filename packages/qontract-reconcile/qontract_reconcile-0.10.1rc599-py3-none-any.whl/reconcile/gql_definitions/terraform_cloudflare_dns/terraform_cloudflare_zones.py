"""
Generated by qenerate plugin=pydantic_v1. DO NOT MODIFY MANUALLY!
"""
from collections.abc import Callable  # noqa: F401 # pylint: disable=W0611
from datetime import datetime  # noqa: F401 # pylint: disable=W0611
from enum import Enum  # noqa: F401 # pylint: disable=W0611
from typing import (  # noqa: F401 # pylint: disable=W0611
    Any,
    Optional,
    Union,
)

from pydantic import (  # noqa: F401 # pylint: disable=W0611
    BaseModel,
    Extra,
    Field,
    Json,
)

from reconcile.gql_definitions.fragments.vault_secret import VaultSecret


DEFINITION = """
fragment VaultSecret on VaultSecret_v1 {
    path
    field
    version
    format
}

query CloudflareDnsZone {
  zones: cloudflare_dns_zone_v1 {
    identifier
    zone
    account {
      name
      type
      description
      providerVersion
      enforceTwofactor
      apiCredentials {
        ... VaultSecret
      }
      terraformStateAccount {
        name
        consoleUrl
        terraformUsername
        automationToken {
          ... VaultSecret
        }
        terraformState {
          provider
          bucket
          region
          integrations {
            integration
            key
          }
        }
      }
      deletionApprovals {
        expiration
        name
        type
      }
    }
    records {
      identifier
      name
      type
      ttl
      value
      priority
      proxied
      data {
        algorithm
        protocol
        public_key
        digest_type
        digest
        key_tag
        flags
      }
    }
    type
    plan
    max_records
    delete
  }
}
"""


class ConfiguredBaseModel(BaseModel):
    class Config:
        smart_union=True
        extra=Extra.forbid


class AWSTerraformStateIntegrationsV1(ConfiguredBaseModel):
    integration: str = Field(..., alias="integration")
    key: str = Field(..., alias="key")


class TerraformStateAWSV1(ConfiguredBaseModel):
    provider: str = Field(..., alias="provider")
    bucket: str = Field(..., alias="bucket")
    region: str = Field(..., alias="region")
    integrations: list[AWSTerraformStateIntegrationsV1] = Field(..., alias="integrations")


class AWSAccountV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    console_url: str = Field(..., alias="consoleUrl")
    terraform_username: Optional[str] = Field(..., alias="terraformUsername")
    automation_token: VaultSecret = Field(..., alias="automationToken")
    terraform_state: Optional[TerraformStateAWSV1] = Field(..., alias="terraformState")


class DeletionApprovalV1(ConfiguredBaseModel):
    expiration: str = Field(..., alias="expiration")
    name: str = Field(..., alias="name")
    q_type: str = Field(..., alias="type")


class CloudflareAccountV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    q_type: Optional[str] = Field(..., alias="type")
    description: Optional[str] = Field(..., alias="description")
    provider_version: str = Field(..., alias="providerVersion")
    enforce_twofactor: Optional[bool] = Field(..., alias="enforceTwofactor")
    api_credentials: VaultSecret = Field(..., alias="apiCredentials")
    terraform_state_account: AWSAccountV1 = Field(..., alias="terraformStateAccount")
    deletion_approvals: Optional[list[DeletionApprovalV1]] = Field(..., alias="deletionApprovals")


class CloudflareDnsRecordDataSettingsV1(ConfiguredBaseModel):
    algorithm: Optional[int] = Field(..., alias="algorithm")
    protocol: Optional[int] = Field(..., alias="protocol")
    public_key: Optional[str] = Field(..., alias="public_key")
    digest_type: Optional[int] = Field(..., alias="digest_type")
    digest: Optional[str] = Field(..., alias="digest")
    key_tag: Optional[int] = Field(..., alias="key_tag")
    flags: Optional[int] = Field(..., alias="flags")


class CloudflareDnsRecordV1(ConfiguredBaseModel):
    identifier: str = Field(..., alias="identifier")
    name: str = Field(..., alias="name")
    q_type: str = Field(..., alias="type")
    ttl: int = Field(..., alias="ttl")
    value: Optional[str] = Field(..., alias="value")
    priority: Optional[int] = Field(..., alias="priority")
    proxied: Optional[bool] = Field(..., alias="proxied")
    data: Optional[CloudflareDnsRecordDataSettingsV1] = Field(..., alias="data")


class CloudflareDnsZoneV1(ConfiguredBaseModel):
    identifier: str = Field(..., alias="identifier")
    zone: str = Field(..., alias="zone")
    account: CloudflareAccountV1 = Field(..., alias="account")
    records: Optional[list[CloudflareDnsRecordV1]] = Field(..., alias="records")
    q_type: Optional[str] = Field(..., alias="type")
    plan: Optional[str] = Field(..., alias="plan")
    max_records: Optional[int] = Field(..., alias="max_records")
    delete: Optional[bool] = Field(..., alias="delete")


class CloudflareDnsZoneQueryData(ConfiguredBaseModel):
    zones: Optional[list[CloudflareDnsZoneV1]] = Field(..., alias="zones")


def query(query_func: Callable, **kwargs: Any) -> CloudflareDnsZoneQueryData:
    """
    This is a convenience function which queries and parses the data into
    concrete types. It should be compatible with most GQL clients.
    You do not have to use it to consume the generated data classes.
    Alternatively, you can also mime and alternate the behavior
    of this function in the caller.

    Parameters:
        query_func (Callable): Function which queries your GQL Server
        kwargs: optional arguments that will be passed to the query function

    Returns:
        CloudflareDnsZoneQueryData: queried data parsed into generated classes
    """
    raw_data: dict[Any, Any] = query_func(DEFINITION, **kwargs)
    return CloudflareDnsZoneQueryData(**raw_data)
