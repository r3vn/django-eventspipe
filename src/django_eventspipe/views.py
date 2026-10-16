from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import PipelineArtifact

@login_required
def get_artifact(request: HttpRequest, artifact_id: int) -> HttpResponse:
    """
    Get a file from Database
    """
    file = PipelineArtifact.objects.get(pk=artifact_id)

    response = HttpResponse(file.artifact.data, content_type='application/octet-stream')
    response['Content-Disposition']='attachment;filename=%s' % file.file_name

    return response
