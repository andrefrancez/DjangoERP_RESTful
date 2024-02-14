from companies.views.base import Base
from companies.utils.exceptions import RequiredField
from companies.utils.permissions import GroupPermissions
from companies.serializers import GroupSerializers
from accounts.models import Group, Group_Permissions
from rest_framework.views import Response
from rest_framework.exceptions import APIException
from django.contrib.auth.models import Permission

class Groups(Base):
    permission_classes = [GroupPermissions]

    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)
        groups = Group.objects.filter(enterprise_id=enterprise_id).all()

        serializer = GroupSerializers(groups, many=True)

        return Response({'groups': serializer.data})

    def post(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)

        name = request.data.get('name')
        permissions = request.data.get('permissions')

        if not name:
            raise RequiredField

        created_group = Group.objects.create(
            name=name,
            enterprise_id=enterprise_id
        )

        if permissions:
            permissions = permissions.split(',')

            try:
                for item in permissions:
                    permission = Permission.objects.filter(id=item).exists()

                    if not permission:
                        created_group.delete()
                        raise APIException('The permission {p} does not exist'.format(p=item))

                    if not Group_Permissions.objects.filter(group_id=created_group.id, permission_id=item).exists():
                        Group_Permissions.objects.create(
                            group_id=created_group.id,
                            permission_id=item
                        )
            except ValueError:
                created_group.delete()
                raise APIException('Send the permissions in the correct standard')

        return Response({'success': True})


class GroupDetail(Base):
    permission_classes = [GroupPermissions]

    def get(self, request, group_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        self.get_group(group_id, enterprise_id)
        group = Group.objects.filter(id=group_id).first()

        serializer = GroupSerializers(group)

        return Response({'group': serializer.data})

    def put(self, request, group_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        self.get_group(group_id, enterprise_id)

        name = request.data.get('name')
        permissions = request.data.get('permissions')

        if name:
            Group.objects.filter(id=group_id).update(
                name=name
            )

        Group_Permissions.objects.filter(group_id=group_id).delete()

        if permissions:
            permissions = permissions.split(',')

            try:
                for item in permissions:
                    permission = Permission.objects.filter(id=item).exists()

                    if not permission:
                        raise APIException('The permission {p} does not exist'.format(p=item))

                    if not Group_Permissions.objects.filter(group_id=group_id, permission_id=item).exists():
                        Group_Permissions.objects.create(
                            group_id=group_id,
                            permission_id=item
                        )
            except ValueError:
                raise APIException("Send the permissions in the correct standard")

        return Response({'success': True})
    
    def delete(self, request, group_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        Group.objects.filter(id=group_id, enterprise_id=enterprise_id).delete()

        return Response({'success': True})