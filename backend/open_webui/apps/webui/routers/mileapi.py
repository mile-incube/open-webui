from typing import Optional

from open_webui.apps.webui.models.models import (
    ModelForm,
    ModelModel,
    ModelResponse,
    ModelUserResponse,
    Models,
)

from open_webui.apps.webui.models.mileapi import MileOrgForm
from open_webui.constants import ERROR_MESSAGES
from fastapi import APIRouter, Depends, HTTPException, Request, status


from open_webui.utils.utils import get_admin_user, get_verified_user
from open_webui.utils.access_control import has_access, has_permission


router = APIRouter()


###########################
# Sync orgs
###########################

@router.get("/org", response_model=bool)
async def sync_mile_org(
    request: Request
):
    if False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.UNAUTHORIZED,
        )

    return True

@router.post("/org/sync", response_model=bool)
async def sync_mile_org(
    request: Request,
    form_data: MileOrgForm,
):
    if False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.UNAUTHORIZED,
        )

    return True