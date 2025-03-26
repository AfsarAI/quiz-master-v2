# routes/__init__.py
from flask_restful import Api

from .admin_api import AddQualificationResource, AddQuizResource, AddSubjectResource, AdminAllQuizzesResource, AdminStatsResource, AllChaptersResource, AllQualificationsResource, AllRecentActivityResource, AllSubjectsResource, AddChapterResource, AllUsersResource, RecentActivityResource, TopScorersResource
from .user_api import QuizScoresResource, UpcomingQuizzesResource, UserAllQuizzesResource, UserQuizResource, UserStatsResource, UserSubjectsResource
from .auth_api import UserByIDResource, UserRegisterResource, UserLoginResource
from .subject_api import SubjectResource, SubjectsWithQualificationResource
from .qual_api import QualificationResource, QualificationSubjectResource
# और भी routes import करें...

api = Api(prefix='/api')

#users routes
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
api.add_resource(AdminStatsResource, '/admin/dashboard/stats', methods=['GET'])
api.add_resource(AllRecentActivityResource, '/admin/dashboard/get/recent-activity/data', methods=['GET'])
api.add_resource(RecentActivityResource, '/admin/dashboard/post/recent-activity/data', methods=['POST'])
api.add_resource(TopScorersResource, '/admin/dashboard/top-scorers', methods=['GET'])
api.add_resource(AllQualificationsResource, '/admin/dashboard/all/qualifications', methods=['GET'])
api.add_resource(AllSubjectsResource, '/admin/dashboard/all/subjects', methods=['GET'])
api.add_resource(AllChaptersResource, '/admin/dashboard/all/chapters', methods=['GET'])
api.add_resource(AllUsersResource, '/all/users/data', methods=['GET'])
api.add_resource(AddQualificationResource, '/admin/dashboard/add/qualification', methods=['POST'])
api.add_resource(AddSubjectResource, '/admin/dashboard/add/subject', methods=['POST'])
api.add_resource(AddChapterResource, '/admin/dashboard/add/chapter', methods=['POST'])
api.add_resource(AdminAllQuizzesResource, '/admin/dashboard/all/quizzes')
api.add_resource(AddQuizResource, '/admin/dashboard/add/quiz', methods=['POST'])

#User Dash
api.add_resource(UserStatsResource, '/user/dashboard/<int:user_id>/user-stats', methods=['GET'])
api.add_resource(UpcomingQuizzesResource, '/user/dashboard/upcoming-quizzes', methods=['GET'])
api.add_resource(UserSubjectsResource, '/user/dashboard/<int:user_id>/subjects', methods=['GET'])
api.add_resource(QuizScoresResource, '/user/dashboard/<int:user_id>/quiz-scores', methods=['GET'])
api.add_resource(UserAllQuizzesResource, '/user/dashboard/all/quizzes', methods=['GET'])
api.add_resource(UserQuizResource, '/user/dashboard/quiz/<int:quiz_id>/quiz-data', methods=['GET'])