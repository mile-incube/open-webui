import logging
import uuid
import aiohttp
from typing import Optional, List
from pydantic import BaseModel

from open_webui.apps.webui.models.users import (
    Users
)
from open_webui.apps.webui.models.groups import (
    Groups,
    GroupForm,
    GroupUpdateForm
)
from open_webui.apps.webui.models.models import (
    Models,
    ModelForm
)

from open_webui.config import (
    MILE_IDENTITY_URL,
    MILE_PORTAL_URL,
    AppConfig,
)

log = logging.getLogger(__name__)


class OrgInfo(BaseModel):
    orgId: str
    orgName: str

# Static definition of models
IMG_EUROPE_FLAG: str = "data:image/png;base64,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"

mile_sync_config = AppConfig()
mile_sync_config.MILE_IDENTITY_URL = MILE_IDENTITY_URL
mile_sync_config.MILE_PORTAL_URL = MILE_PORTAL_URL

class MileSync:
    def __init__(self):
        self.admin_user = Users.get_first_user()

    async def get_group_by_org(self, orgId: str):
        existing_groups = Groups.get_groups()
        return next((group for group in existing_groups if group.name.startswith(orgId)), None)

    async def create_or_update_group(self, orgId: str, orgName: str):
        group = await self.get_group_by_org(orgId)

        form_data = GroupForm(name=f"{orgId} ({orgName})", description=orgName)
        if not group:
            group = Groups.insert_new_group(self.admin_user.id, form_data)
            log.info(f"Created new group: {group}")

        return group

    async def create_or_update_models(self, orgId: str, orgName: str, models: List[ModelForm], group_id: str):
        for model in models:
            model_id = f"{model.id}_{orgId}"
            existing_model = Models.get_model_by_id(model_id)

            meta = model.meta.dict() if model.meta else {}
            meta.update({"filterIds": ["mile_internal_check_token_limit"]})

            access_control = {
                "read": {"group_ids": [group_id], "user_ids": []},
                "write": {"group_ids": [], "user_ids": []}
            }

            form_data = ModelForm(
                id=model_id,
                base_model_id=model.id,
                name=model.name,
                meta=meta,
                params=model.params,
                access_control=access_control,                
                is_active=True
            )

            if not existing_model:
                Models.insert_new_model(form_data, self.admin_user.id)
            else:
                Models.update_model_by_id(model_id, form_data)

    async def create_or_update_group_assignments(self, userId: str, orgIds: List[str]):
        current_groups = Groups.get_groups_by_member_id(userId)
        target_group_ids = set()

        for orgId in orgIds:
            group = await self.get_group_by_org(orgId)
            if group:
                target_group_ids.add(group.id)

        log.warning(f'Found {len(target_group_ids)} target groups to assign')

        # Remove user from groups they should no longer be in
        for group in current_groups:
            if group.id not in target_group_ids:
                updated_user_ids = [uid for uid in group.user_ids if uid != userId]
                form_data = GroupUpdateForm(
                    name=group.name,
                    description=group.description,
                    user_ids=updated_user_ids,
                    permissions=group.permissions
                )
                Groups.update_group_by_id(group.id, form_data, overwrite=True)
                log.warning(f"Removed user {userId} from group {group.id}")

        # Add user to target groups
        for target_group_id in target_group_ids:
            group = Groups.get_group_by_id(target_group_id)
            if group:
                updated_user_ids = group.user_ids + [userId] if userId not in group.user_ids else group.user_ids
                form_data = GroupUpdateForm(
                    name=group.name,
                    description=group.description,
                    user_ids=updated_user_ids,
                    permissions= {
                        "workspace": {
                            "models": False,
                            "knowledge": False,
                            "prompts": False,
                            "tools": False,
                        },
                        "chat": {
                            "file_upload": False,
                            "delete": True,
                            "edit": True,
                            "temporary": True,
                        }
                    }
                )
                Groups.update_group_by_id(group.id, form_data, overwrite=True)
                log.warning(f"Added user {userId} to group {group.id}")

    async def fetch_org_infos(self, userEmail: str) -> List[OrgInfo]:
        url = f"{mile_sync_config.MILE_IDENTITY_URL}/openwebui/getorgsbyuser"
        payload = {
            "userEmail": userEmail
        }
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'e2cc960a-a913-4d0a-a8dd-42c581decb10_fc34b792-e6f1-4b5c-9c9d-43b42152db4a'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, ssl=False) as response:
                if response.status == 200:
                    data = await response.json()
                    return [OrgInfo(orgId=org["id"], orgName=org["name"]) for org in data]
                else:
                    return []

    async def do_sync(self, userEmail: str):
        orgInfos = await self.fetch_org_infos(userEmail)
        await self.do_sync_with_orginfos(userEmail, orgInfos)

    async def do_sync_with_orginfos(self, userEmail: str, orgInfos: List[OrgInfo]):
        user = Users.get_user_by_email(userEmail)
        log.warning(f'User {user.email}')

        for orgInfo in orgInfos:
            log.warning(f'Creating group for {orgInfo.orgName}')
            group = await self.create_or_update_group(orgInfo.orgId, orgInfo.orgName)

            if group:
                ## Sample Prompt
                #[
                #    {
                #        "title": [
                #            "Zeile 1",
                #            "Zeile 2"
                #        ],
                #        "content": "Das ist der Prompt!"
                #    }
                #]

                models: List[ModelForm] = [
                    ModelForm(
                        id="gpt-4o-mini-eu",
                        base_model_id=None,
                        name="Alltägliche Aufgaben",
                        meta={
                            "profile_image_url": IMG_EUROPE_FLAG,
                            "description": f"Liefert schnell gute Ergebnisse bei alltäglichen Aufgaben.\nBereitgestellt in Europa, basiert auf dem Modell GPT-4o-mini von OpenAI.",
                            "capabilities": {
                                "vision": True,
                                "usage": True,
                                "citations": True
                            },
                            "suggestion_prompts": None,
                            "tags": [ { "name": orgInfo.orgName } ],
                            "filterIds": []
                        },
                        params={
                            #"stream_response": True
                        },
                        is_active=True
                    ),
                    ModelForm(
                        id="gpt-4o-eu",
                        base_model_id=None,
                        name="Komplexe Aufgaben",
                        meta={
                            "profile_image_url": IMG_EUROPE_FLAG,
                            "description": f"Versteht komplexe zusammenhänge und ist  für anspruchsvolle Aufgaben geeignet.\nBereitgestellt in Europa, basiert auf dem Modell GPT-4o von OpenAI.",
                            "capabilities": {
                                "vision": True,
                                "usage": True,
                                "citations": True
                            },
                            "suggestion_prompts": None,
                            "tags": [{ "name": orgInfo.orgName }],
                            "filterIds": []
                        },
                        params={
                            #"stream_response": True
                        },
                        is_active=True
                    )
                ]

                log.warning(f'Creating models for {orgInfo.orgName}')
                await self.create_or_update_models(orgInfo.orgId, orgInfo.orgName, models, group.id)

        orgIds = [orgInfo.orgId for orgInfo in orgInfos]
        log.warning(f'Create assignments for {len(orgIds)} orgIds')
        await self.create_or_update_group_assignments(user.id, orgIds)

        if user.role != "admin":
            if len(orgIds) > 0:
                Users.update_user_role_by_id(user.id, "user")
            else:
                Users.update_user_role_by_id(user.id, "pending")

mile_sync = MileSync()
