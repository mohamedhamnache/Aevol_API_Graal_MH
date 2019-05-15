from flask_restful import Resource, reqparse
import requests
import json
import datetime, time
import os
import config
from Packages.ResourceAlloc.helper import Helper
from Models import UserModel, JobModel


parser = reqparse.RequestParser()

parser.add_argument('ID_USER', help = 'This field cannot be blank', required = False)
parser.add_argument('Nom_simu', help = 'This field cannot be blank', required = False)
parser.add_argument('id_deployment', help = 'This field cannot be blank', required = False)


parser.add_argument('ID_JOB', help = 'This field cannot be blank', required = False)
parser.add_argument('End_time', help = 'This field cannot be blank', required = False)
parser.add_argument('status', help = 'This field cannot be blank', required = False)
parser.add_argument('progress', help = 'This field cannot be blank', required = False)

parser.add_argument('nb_gen', help = 'This field cannot be blank', required = False)
parser.add_argument('nb_th', help = 'This field cannot be blank', required = False)

class Users(Resource):
    def get(self):
        return UserModel.return_Users()
class Jobs(Resource):
    def get(self):
        return JobModel.return_Jobs()

class CreateJob(Resource):
    def post(Resource):
        data = parser.parse_args()
        new_job = JobModel(
            ID_USER=data['ID_USER'],
            Nom_simu= data['Nom_simu'],
            id_deployment = data ['id_deployment'],
            Statut ="creating",
            Start_time ="0000-00-00 00:00:00",
            End_time = "0000-00-00 00:00:00"
        )
        try:
            new_job.save_to_db()
            job_id =int(JobModel.getLastid())-1
            os.mkdir( config.SimulationDir+'/'+str(job_id))
            return {
                'message': 'Job successfully created',
                'ID_JOB' : job_id
            }
        except:
            return {'message': 'Something went wrong'}, 500

class UpdateStartTime(Resource):
    def post(self):
        data = parser.parse_args()
        try:
            JobModel.updateStartTime(int(data['ID_JOB']),int(data['ID_USER']))
            return{'message':'Start Time Updated Successfully'},200
        except:
            return{'message':"Something Wrong Happened"},500

class UpdateEndTime(Resource):
    def post(self):
        data = parser.parse_args()
        try:
            JobModel.updateEndTime(int(data['ID_JOB']),int(data['ID_USER']),data['End_time'])
            return{'message':'End Time Updated Successfully'},200
        except:
            return{'message':"Something Wrong Happened"},500
class UpdateStatus(Resource):
    def post(self):
        data = parser.parse_args()
        print(data)
        try:
            JobModel.updateStatus(int(data['ID_JOB']),int(data['ID_USER']),data['status'])
            return{'message':'Status Updated Successfully'},200
        except:
            return{'message':"Something Wrong Happened"},500
class UpdateProgress(Resource):
    def post(self):
        data = parser.parse_args()
        try:
            JobModel.updateProgress(int(data['ID_JOB']),int(data['ID_USER']),int(data['progress']))
            return{'message':'Progress Updated Successfully'},200
        except:
            return{'message':"Something Wrong Happened"},500

class DeletJob(Resource):
    def post(self):
        data = parser.parse_args()
        try:
            r = JobModel.removeJob(int(data['ID_JOB']),int(data['ID_USER']))
            return r
        except:
            return{'message':"Something Wrong Happened"},500
class GetStatus(Resource):
    def post(self):
        data = parser.parse_args()
        try:
            r = JobModel.getStatus(int(data['ID_JOB']),int(data['ID_USER']))
            if (r['status']!="None"):
            
                return str(r['status']),200
            else:
                return{"message" :"status is not set"}
        except:
            return{'message':"Something Wrong Happened"},500
class AevolTools(Resource):
    def get(self):
        return{'message':"Welcome to Aevol_Tools API *___* "},200

class GetUserJobs(Resource):
    def post(self):
        data = parser.parse_args()
        try:  
            return JobModel.return_userJobs(int(data['ID_USER']))
        except:
            return{'message':"Something Wrong Happened"},500

class launchSingleSImulation(Resource):
    def post(self):
        data = parser.parse_args()
        simDir = config.SimulationDir+'/'+str(data['ID_JOB'])
        cd = "cd "+simDir
        runCmd =config.launchSimulationClient+' '+ config.configClient+' param.in '+data['ID_USER'] +' '+data['ID_JOB']+' "'+data['Nom_simu']+'" '+ data['nb_gen']+' '+data['nb_th']
        print(runCmd)
        os.system(cd +' && '+runCmd)
        return 0