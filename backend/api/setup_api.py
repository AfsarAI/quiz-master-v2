# routes/__init__.py
from flask_restful import Api

from .admin_api import AdminStatsResource, AllRecentActivityResource, RecentActivityResource
from .auth_api import UserResource, UserByIDResource, UserRegisterResource, UserLoginResource
from .subject_api import SubjectResource, SubjectsWithQualificationResource
from .qual_api import QualificationResource, QualificationSubjectResource
# और भी routes import करें...

api = Api(prefix='/api')

#users routes
api.add_resource(UserResource, '/all/users/data')
api.add_resource(UserByIDResource, '/user/<int:user_id>/data', methods=['GET'])
api.add_resource(UserRegisterResource, '/user/register', methods=['POST'])
api.add_resource(UserLoginResource, '/user/login', methods=['POST'])

#subjests routes
api.add_resource(SubjectResource, '/subjects')
api.add_resource(SubjectsWithQualificationResource, '/qualifications/<int:qualification_id>/subjects')

#qual routes
api.add_resource(QualificationResource, '/qualifications')
api.add_resource(QualificationSubjectResource, '/create/qualification-subjects')

#Admin Dash
api.add_resource(AdminStatsResource, '/dashboard/stats')
api.add_resource(AllRecentActivityResource, '/dashboard/get/recent-activity/data', methods=['GET'])
api.add_resource(RecentActivityResource, '/dashboard/post/recent-activity/data', methods=['POST'])