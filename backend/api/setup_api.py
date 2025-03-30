from flask_restful import Api
from .admin_api import AddQualificationResource, AddQuizResource, AddSubjectResource, AdminAllQuizzesResource, AdminStatsResource, AllChaptersResource, AllQualificationsResource, AllRecentActivityResource, AllSubjectsResource, AddChapterResource, AllUsersResource, DeleteChapterResource, DeleteQualificationResource, DeleteQuizResource, DeleteSubjectResource, EditQuizResource, QuizDetailResource, TopScorersResource, UpdateChapterResource, UpdateQualificationResource, UpdateSubjectResource, UserEngagementResource, UserStatusResource
from .user_api import QuizScoresResource, SubmitQuizResource, TaskCSVResource, TaskStatusResource, UpcomingQuizzesResource, UserAllQuizzesResource, UserByIDResource, UserQuizResource, UserStatsResource
from .auth_api import QualificationResource, SubjectsWithQualificationResource, UserRegisterResource, UserLoginResource

api = Api(prefix='/api')


# Auth API
#qual routes for registration page
api.add_resource(QualificationResource, '/qualifications')
#subject for registeration page
api.add_resource(SubjectsWithQualificationResource, '/qualifications/<int:qualification_id>/subjects')
# user login & register api
api.add_resource(UserRegisterResource, '/user/register', methods=['POST'])
api.add_resource(UserLoginResource, '/user/login', methods=['POST'])


#Admin Dashboard
api.add_resource(AdminStatsResource, '/admin/dashboard/stats', methods=['GET'])
api.add_resource(AllRecentActivityResource, '/admin/dashboard/recent-activity/data', methods=['GET'])
api.add_resource(TopScorersResource, '/admin/dashboard/top-scorers', methods=['GET'])

# user routes
api.add_resource(AllUsersResource, '/all/users/data', methods=['GET'])
api.add_resource(UserStatusResource, '/user/<int:user_id>/status', methods=['PUT'])
api.add_resource(UserEngagementResource, '/admin/dashboard/user-engagement', methods=['GET'])

# qualification routes
api.add_resource(AllQualificationsResource, '/admin/dashboard/all/qualifications', methods=['GET'])
api.add_resource(AddQualificationResource, '/admin/dashboard/add/qualification', methods=['POST'])
api.add_resource(UpdateQualificationResource, '/admin/dashboard/update/qualification/<int:qual_id>', methods=['PUT'])
api.add_resource(DeleteQualificationResource, '/admin/dashboard/delete/qualification/<int:qual_id>', methods=['DELETE'])

# subject routes
api.add_resource(AllSubjectsResource, '/admin/dashboard/all/subjects', methods=['GET'])
api.add_resource(AddSubjectResource, '/admin/dashboard/add/subject', methods=['POST'])
api.add_resource(UpdateSubjectResource, '/admin/dashboard/update/subject/<int:subject_id>', methods=['PUT'])
api.add_resource(DeleteSubjectResource, '/admin/dashboard/delete/subject/<int:subject_id>', methods=['DELETE'])

# chapter routes
api.add_resource(AllChaptersResource, '/admin/dashboard/all/chapters', methods=['GET'])
api.add_resource(AddChapterResource, '/admin/dashboard/add/chapter', methods=['POST'])
api.add_resource(UpdateChapterResource, '/admin/dashboard/update/chapter/<int:chapter_id>', methods=['PUT'])
api.add_resource(DeleteChapterResource, '/admin/dashboard/delete/chapter/<int:chapter_id>', methods=['DELETE'])

# quiz routes
api.add_resource(AdminAllQuizzesResource, '/admin/dashboard/all/quizzes')
api.add_resource(AddQuizResource, '/admin/dashboard/add/quiz', methods=['POST'])
api.add_resource(QuizDetailResource, '/admin/dashboard/quiz/<int:quiz_id>', methods=['GET'])
api.add_resource(EditQuizResource, '/admin/dashboard/<int:quiz_id>', methods=['PUT'])
api.add_resource(DeleteQuizResource, '/admin/dashboard/quiz/<int:quiz_id>', methods=['DELETE'])



#User Dashboard
api.add_resource(UserStatsResource, '/user/dashboard/<int:user_id>/user-stats', methods=['GET'])
api.add_resource(UpcomingQuizzesResource, '/user/dashboard/upcoming-quizzes', methods=['GET'])
api.add_resource(QuizScoresResource, '/user/dashboard/<int:user_id>/quiz-scores', methods=['GET'])
api.add_resource(UserAllQuizzesResource, '/user/<int:user_id>/dashboard/all/quizzes', methods=['GET'])
api.add_resource(UserQuizResource, '/user/dashboard/quiz/<int:quiz_id>/quiz-data', methods=['GET'])
api.add_resource(SubmitQuizResource, '/user/dashboard/quiz/<int:quiz_id>/submit', methods=['POST'])
api.add_resource(TaskCSVResource, '/user/dashboard/task/csv-export/<int:user_id>', methods=['GET'])
api.add_resource(TaskStatusResource, '/user/dashboard/task/csv-download/<task_id>', methods=['GET'])
# for profile
api.add_resource(UserByIDResource, '/user/<int:user_id>/data', methods=['GET'])