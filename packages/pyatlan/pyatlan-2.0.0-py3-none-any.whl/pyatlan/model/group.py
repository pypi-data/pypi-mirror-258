# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject


class AtlanGroup(AtlanObject):
    class Attributes(AtlanObject):
        alias: Optional[List[str]] = Field(
            default=None, description="Name of the group as it appears in the UI."
        )
        created_at: Optional[List[str]] = Field(
            default=None,
            description="Time (epoch) at which the group was created, in milliseconds.",
        )
        created_by: Optional[List[str]] = Field(
            default=None, description="User who created the group."
        )
        updated_at: Optional[List[str]] = Field(
            default=None,
            description="Time (epoch) at which the group was last updated, in milliseconds.",
        )
        updated_by: Optional[List[str]] = Field(
            default=None, description="User who last updated the group."
        )
        description: Optional[List[str]] = Field(
            default=None, description="Description of the group."
        )
        is_default: Optional[List[str]] = Field(
            default=None,
            description="Whether this group should be auto-assigned to all new users or not.",
        )
        channels: Optional[List[str]] = Field(
            default=None, description="Slack channels for this group."
        )

    alias: Optional[str] = Field(
        default=None, description="Name of the group as it appears in the UI."
    )
    attributes: Optional[AtlanGroup.Attributes] = Field(
        default=None, description="Detailed attributes of the group."
    )
    decentralized_roles: Optional[List[Any]] = Field(default=None, description="TBC")
    id: Optional[str] = Field(
        default=None, description="Unique identifier for the group (GUID)."
    )
    name: Optional[str] = Field(
        default=None, description="Unique (internal) name for the group."
    )
    path: Optional[str] = Field(default=None, description="TBC")
    personas: Optional[List[Any]] = Field(
        default=None, description="Personas the group is associated with."
    )
    purposes: Optional[List[Any]] = Field(
        default=None, description="Purposes the group is associated with."
    )
    user_count: Optional[int] = Field(
        default=None, description="Number of users in the group."
    )

    def is_default(self) -> bool:
        return (
            self.attributes is not None
            and self.attributes.is_default is not None
            and self.attributes.is_default == ["true"]
        )

    @staticmethod
    def create(
        alias: str,
    ) -> AtlanGroup:
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["alias"],
            [alias],
        )
        return AtlanGroup(
            name=AtlanGroup.generate_name(alias),
            attributes=AtlanGroup.Attributes(alias=[alias]),
        )

    @staticmethod
    def create_for_modification(
        guid: str,
        path: str,
    ) -> AtlanGroup:
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["guid", "path"],
            [guid, path],
        )
        return AtlanGroup(id=guid, path=path)

    @staticmethod
    def generate_name(
        alias: str,
    ) -> str:
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["alias"],
            [alias],
        )
        internal = alias.lower()
        return internal.replace(" ", "_")


class GroupResponse(AtlanObject):
    total_record: Optional[int] = Field(description="Total number of groups.")
    filter_record: Optional[int] = Field(
        description="Number of groups in the filtered response.",
    )
    records: Optional[List[AtlanGroup]] = Field(
        description="Details of each group included in the response."
    )


class CreateGroupRequest(AtlanObject):
    group: AtlanGroup = Field(description="Group to be created.")
    users: Optional[List[str]] = Field(
        default=None,
        description="List of users (their GUIDs) to be included in the group.",
    )


class RemoveFromGroupRequest(AtlanObject):
    users: Optional[List[str]] = Field(
        default=None,
        description="List of users (their GUIDs) to remove from the group.",
    )


class CreateGroupResponse(AtlanObject):
    class UserStatus(AtlanObject):
        status: Optional[int] = Field(
            default=None,
            description="Response code for the association (200 is success).",
        )
        status_message: Optional[str] = Field(
            default=None,
            description="Status message for the association ('success' means the association was successful).",
        )

        def was_successful(self) -> bool:
            return (self.status is not None and self.status == 200) or (
                self.status_message is not None and self.status_message == "success"
            )

    group: str = Field(
        description="Unique identifier (GUID) of the group that was created."
    )
    users: Optional[Dict[str, CreateGroupResponse.UserStatus]] = Field(
        default=None,
        description="Map of user association statuses, keyed by unique identifier (GUID) of the user.",
    )
