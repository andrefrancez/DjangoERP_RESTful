from companies.views.base import Base
from companies.utils.permissions import GroupPermissions
from companies.serializers import PermissionSerializers
from rest_framework.response import Response
from django.contrib.auth.models import Permission

class PermissionDetail(Base):
    permission_classes = [GroupPermissions]

    def get(self, request):
        permissions = Permission.objects.filter(content_type_id__in=[2, 7, 11, 13]).all()

        serializer = PermissionSerializers(permissions, many=True)

        return Response({'Permissions': serializer.data})