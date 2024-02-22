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


DEFINITION = """
query AwsSamlRolesAwsGroupQuery {
  aws_groups: awsgroups_v1 {
    name
    account {
      name
      uid
      sso
      disable {
        integrations
      }
    }
    roles {
      users {
        org_username
      }
    }
    policies
  }
}
"""


class ConfiguredBaseModel(BaseModel):
    class Config:
        smart_union=True
        extra=Extra.forbid


class DisableClusterAutomationsV1(ConfiguredBaseModel):
    integrations: Optional[list[str]] = Field(..., alias="integrations")


class AWSAccountV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    uid: str = Field(..., alias="uid")
    sso: Optional[bool] = Field(..., alias="sso")
    disable: Optional[DisableClusterAutomationsV1] = Field(..., alias="disable")


class UserV1(ConfiguredBaseModel):
    org_username: str = Field(..., alias="org_username")


class RoleV1(ConfiguredBaseModel):
    users: list[UserV1] = Field(..., alias="users")


class AWSGroupV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    account: AWSAccountV1 = Field(..., alias="account")
    roles: Optional[list[RoleV1]] = Field(..., alias="roles")
    policies: Optional[list[str]] = Field(..., alias="policies")


class AwsSamlRolesAwsGroupQueryQueryData(ConfiguredBaseModel):
    aws_groups: Optional[list[AWSGroupV1]] = Field(..., alias="aws_groups")


def query(query_func: Callable, **kwargs: Any) -> AwsSamlRolesAwsGroupQueryQueryData:
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
        AwsSamlRolesAwsGroupQueryQueryData: queried data parsed into generated classes
    """
    raw_data: dict[Any, Any] = query_func(DEFINITION, **kwargs)
    return AwsSamlRolesAwsGroupQueryQueryData(**raw_data)
