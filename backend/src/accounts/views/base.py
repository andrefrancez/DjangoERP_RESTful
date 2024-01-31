from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from companies.models import Enterprise, Employee
from accounts.models import User_Groups, Group_Permissions

class Base(APIView):
    def get_enterprise_user(self, user_id):
        enterprise = {
            'is_owner': False,
            'permissions': []
        }

        enterprise['is_owner'] = Enterprise.objects.filter(user_id=user_id).exists()

        if enterprise['is_owner']: 
            return enterprise

        employee = Employee.objects.filter(user_id=user_id).first()

        if not employee:
            raise APIException('Employee not found.')
        
        groups = User_Groups.objects.filter(user_id=user_id).All()

        for g in groups:
            group = g.group

            permissions = Group_Permissions.objects.filter(group_id=group.id).All()

            for p in permissions:
                enterprise['permissions'].append({
                    'id': p.permissions.id,
                    'label': p.permissions.label,
                    'codename': p.permissions.codename
                })

        return enterprise