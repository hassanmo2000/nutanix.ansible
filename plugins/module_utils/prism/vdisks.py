# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .clusters import get_cluster_uuid
from .groups import get_entity_uuid
from .prism import Prism


class VDisks:

    def get_spec(self, module, vdisk):
        payload = self._get_default_spec()
        spec, error = self._build_spec_vdisk(module, payload, vdisk)
        if error:
            return None, error
        return spec, None

    @staticmethod
    def _get_default_spec():
        return deepcopy(
            {
                "diskSizeBytes": None,
                "diskDataSourceReference": {
                    "$objectType": "common.v1.config.EntityReference",
                    "$reserved": {
                        "$fqObjectType": "common.v1.r0.a3.config.EntityReference"
                    },
                    "$unknownFields": {},
                    "extId": None,
                    "entityType": "STORAGE_CONTAINER"
                }
            }
        )

    @staticmethod
    def _build_spec_vdisk(module, payload, vdisk):

        disk_size_bytes = vdisk["size_gb"] * 1024 * 1024 * 1024

        payload["diskSizeBytes"] = disk_size_bytes
        uuid, error = get_entity_uuid(
            vdisk["storage_container"],
            module,
            key="container_name",
            entity_type="storage_container",
        )
        if error:
            return None, error

        payload["diskDataSourceReference"]["extId"] = uuid

        return payload, None
