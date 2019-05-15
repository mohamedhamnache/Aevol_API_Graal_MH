from flask_restful import Resource, reqparse
import requests
import json
import datetime, time

from execo_g5k import *
import config
from Packages.ResourceAlloc.helper import Helper
from Models import DeploymentModel, g5kHostsModel

parser = reqparse.RequestParser()
parser.add_argument('NbNodes', help = 'This field cannot be blank', required = False)
parser.add_argument('walltime', help = 'This field cannot be blank', required = False)
parser.add_argument('jobName', help = 'This field cannot be blank', required = False)

parser.add_argument('job_id', help = 'This field cannot be blank', required = False)
parser.add_argument('frontend', help = 'This field cannot be blank', required = False)


class NodeReservation(Resource):
    def post(self):
        data = parser.parse_args()
        print(data)
        # try :
        h = Helper()
            #print(h.SiteList())
        hosts,time,job_id,frontend = h.AllocDeployG5k(data['NbNodes'],data['walltime'],data['jobName'])
        #Model Creation 
        deployment = DeploymentModel(
            job_name=data['jobName'],
            nb_nodes= data['NbNodes'],
            frontend = frontend,
            walltime= self.toSeconds(data['walltime']),
            job_id = job_id,
            deployment_time =self.toSeconds(str(time))
        )
        try:
            deployment.save_to_db()
            lastDep = int(DeploymentModel.getLastid())-1
            for host in hosts:
                hostBD = g5kHostsModel(
                   id_dep = lastDep,
                   hostName = str(host)
                )
                hostBD.save_to_db()
                

        except:
            return {'message': 'Something went wrong'}, 500
        return {
            "message" :"successfuly deployed",
            "frontend":str(frontend),
            "job_id" :str(job_id),
            "hosts": hosts,
            "deploymentTime":str(time)
        },200
        # except:
            #return {"message":"error !!"},400
    def toSeconds(self,date):
        Dtime = (datetime.datetime.strptime(date.partition('.')[0], "%H:%M:%S")).time()
        seconds = (Dtime.hour * 60 + Dtime.minute) * 60 + Dtime.second
        return seconds




class NodeDestroy(Resource):
    def post(self):
        data = parser.parse_args()
        print(data)
        h = Helper()
        h.removeResources(data['job_id'],data['frontend'])

class AllDeployments(Resource):
    def get(self):
        print(DeploymentModel.getNextId())
        return DeploymentModel.return_allDeployments()

class getLastJob(Resource):
    def get(self):
        lastDepID = int(DeploymentModel.getLastid())-1
        res,job_id_frontend,status =DeploymentModel.getLastDeployment(lastDepID)
        return res,status
        
class getJobG5kInfo(Resource):
    def get(self):
        lastDepID = int(DeploymentModel.getLastid())-1
        res,job_id,frontend,status =DeploymentModel.getLastDeployment(lastDepID)
        ansG5k = get_oar_job_info(oar_job_id=job_id, frontend=frontend)
        ansG5k = json.dumps(ansG5k)
        res =json.loads(ansG5k)
        now = datetime.datetime.now()
        unixTS =oar.oar_date_to_unixts(str(now))
        timeLeft = (res['start_date'] + res['walltime'])- unixTS
        print (timeLeft)
        res.update({'time_left': timeLeft})
        res.update({'id_deployment': lastDepID})
        print(res)
        return res


        



