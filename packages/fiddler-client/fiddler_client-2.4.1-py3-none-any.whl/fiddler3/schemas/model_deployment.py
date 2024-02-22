from datetime import datetime
from uuid import UUID

from fiddler3.schemas.base import BaseModel
from fiddler3.schemas.model import ModelCompactResp
from fiddler3.schemas.organization import OrganizationCompactResp
from fiddler3.schemas.project import ProjectCompactResp
from fiddler3.schemas.user import UserCompactResp


class ModelDeploymentResponse(BaseModel):
    id: UUID
    model: ModelCompactResp
    project: ProjectCompactResp
    organization: OrganizationCompactResp
    artifact_type: str
    deployment_type: str
    active: bool
    image_uri: str
    replicas: int
    cpu: int
    memory: int
    created_at: datetime
    updated_at: datetime
    created_by: UserCompactResp
    updated_by: UserCompactResp
