from flask import Blueprint
from flask_restful import Api




api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from Packages.ResourceAlloc import ResourceAlloc
from Packages.SimulationManager import SimulationManager
from Packages.auth import Authentication
from Packages.user import UserManager
from Packages.FileManager import FileManager

#Resource Allocation endpoints 
api.add_resource(ResourceAlloc.NodeReservation, '/nodeReservation')
api.add_resource(ResourceAlloc.NodeDestroy, '/NodeDestroy')
api.add_resource(ResourceAlloc.AllDeployments, '/deployments')
api.add_resource(ResourceAlloc.getLastJob, '/lastDeploy')
api.add_resource(ResourceAlloc.getJobG5kInfo, '/job-info-g5k')
#UserManager endpoints 

api.add_resource(UserManager.ActivateAccount, '/activate-account')
api.add_resource(UserManager.SetAccountPermission, '/set-permission')
api.add_resource(UserManager.RemoveUser, '/remove-user')
api.add_resource(UserManager.AllUsers, '/users')

#Simulation endpoints
api.add_resource(SimulationManager.Jobs,'/Jobs')
api.add_resource(SimulationManager.CreateJob,'/create-job')
api.add_resource(SimulationManager.UpdateStartTime,'/set-start-time')
api.add_resource(SimulationManager.UpdateEndTime,'/set-end-time')
api.add_resource(SimulationManager.UpdateStatus,'/update-status')
api.add_resource(SimulationManager.UpdateProgress,'/update-progress')
api.add_resource(SimulationManager.DeletJob,'/remove-job')
api.add_resource(SimulationManager.GetStatus,'/get-status')
api.add_resource(SimulationManager.AevolTools,'/aevol-tools')
api.add_resource(SimulationManager.GetUserJobs,'/userJobs')
api.add_resource(SimulationManager.GetFinishedUserJobs,'/user-finished-jobs')
api.add_resource(SimulationManager.launchSingleSImulation,'/run-single-sim')
# Authentication endpoints 

api.add_resource(Authentication.UserRegistration, '/registration')
api.add_resource(Authentication.UserLogin, '/login')
api.add_resource(Authentication.UserLogoutAccess, '/logout/access')
api.add_resource(Authentication.UserLogoutRefresh, '/logout/refresh')
api.add_resource(Authentication.TokenRefresh, '/token/refresh')
api.add_resource(Authentication.SecretResource, '/secret')
api.add_resource(Authentication.ResetPasswordMail, '/resetmail')
api.add_resource(Authentication.ResetPassword, '/resetpassword')

# FileManager
api.add_resource(FileManager.ParamFileUpload,'/upload-param-file')
