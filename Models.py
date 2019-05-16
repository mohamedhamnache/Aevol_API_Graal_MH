from flask_sqlalchemy import *
import datetime
from passlib.hash import pbkdf2_sha256 as sha256
db = SQLAlchemy()




#########################  Deployment ###########################
class DeploymentModel(db.Model):
    __tablename__ = 'deployment'

    id_deployment = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_name =db.Column(db.String(120), nullable=False)
    nb_nodes = db.Column(db.Integer, nullable=False)
    frontend= db.Column(db.String(120), nullable=False)
    walltime = db.Column(db.Integer, nullable=False)
    job_id = db.Column(db.Integer, nullable=False)
    deployment_time = db.Column(db.Integer, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_jobid_frontend(cls, job_id,frontend):
        return cls.query.filter_by(job_id=job_id,frontend=frontend).first()
    
    @classmethod
    def return_allDeployments(cls):
        def to_json(x):
            return {
                'id_deployment' :x.id_deployment,
                'job_name': x.job_name,
                'nb_nodes' : x.nb_nodes,
                'frontend': x.frontend,
                'walltime': x.walltime,
                'job_id': x.job_id,
                'deployment_time': x.deployment_time,
            }
        return {'deployments': list(map(lambda x: to_json(x), DeploymentModel.query.all()))}
    
    @classmethod
    def getLastid(cls):
        sql ="SELECT AUTO_INCREMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'deployment'"
        result = db.engine.execute(sql)
        for r in result:
            return r[0]
    @classmethod
    def getLastDeployment(cls,id):
        deployment = cls.query.filter_by(id_deployment=id).first()
        if(deployment):
            return {
                'id_deployment' :id,
                'frontend': deployment.frontend,
                'job_id':deployment.job_id
            },deployment.job_id,deployment.frontend,200
        else:
            return{'message': 'An error accured'},400
        
    
#########################  g5khosts ########################### 
       
class g5kHostsModel(db.Model):
    __tablename__ = 'g5khosts'
    id_host = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_dep =db.Column(db.Integer,nullable=False)
    hostName= db.Column(db.String(80), nullable=False)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_allg5kHosts(cls):
        def to_json(x):
            return {
                'id_host' :x.id_host,
                'id_dep': x.id_dep,
                'hostName' : x.hostName       
            }

        return {'G5k_Hosts': list(map(lambda x: to_json(x), g5kHostsModel.query.all()))}

    @classmethod
    def return_hosts(cls,id_deployment):
        def to_json(x):

            return {
              'hostName' : x.hostName,     
            }

        return {'hosts': list(map(lambda x: to_json(x), cls.query.filter_by(id_dep=id_deployment)))}


#########################  Jobs ########################### 

class JobModel(db.Model):
    __tablename__ = 'Jobs'

    ID_JOB = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_USER = db.Column(db.Integer, nullable = False)
    Nom_simu =db.Column(db.String(120), nullable=False)
    Statut= db.Column(db.String(40), nullable=False)
    Start_time = db.Column(db.DateTime)
    End_time = db.Column(db.DateTime)
    Percentage = db.Column(db.Integer, nullable = False,default=0)
    id_deployment = db.Column(db.Integer, nullable = False)

    # Save an entry to Jobs Table
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    #Get all jobs in the database
    @classmethod
    def return_Jobs(cls):
        def to_json(x):
            return {
                'ID_JOB': x.ID_JOB,
                'ID_USER' :x.ID_USER,
                'Nom_simu': x.Nom_simu,
                'Statut': x.Statut, 
                'Start_time': str(x.Start_time), 
                'End_time': str(x.End_time), 
                'Percentage': x.Percentage,
                'id_deployment': x.id_deployment,       
            }

        return {'Jobs': list(map(lambda x: to_json(x), JobModel.query.all()))}

    @classmethod
    def return_userJobs(cls,ID_USER):
        def to_json(x):

            if (str(x.Start_time) =='None'):
                start ="0000-00-00 00:00:00"
            else:
                 start = str(x.Start_time)
            if (str(x.End_time) =='None'):
                end ="0000-00-00 00:00:00" 
            else:
                end =str(x.End_time)

            return {
                'ID_JOB': x.ID_JOB,
                'ID_USER' :x.ID_USER,
                'Nom_simu': x.Nom_simu,
                'Statut': x.Statut, 
                'Start_time': start, 
                'End_time': end, 
                'Percentage': x.Percentage,
                'id_deployment': x.id_deployment,       
            }

        return {'Jobs': list(map(lambda x: to_json(x), cls.query.filter_by(ID_USER=ID_USER))),'ID_USER':ID_USER}
    #Update start simulation time 

    @classmethod
    def updateStartTime(cls,ID_JOB,ID_USER):
        job = cls.query.filter_by(ID_JOB=ID_JOB,ID_USER=ID_USER).first()
        if(job.Start_time is None):
            job.Start_time =datetime.datetime.now()
            db.session.commit()
        return job.Start_time
    @classmethod
    def updateStartTime(cls,ID_JOB,ID_USER):
        job = cls.query.filter_by(ID_JOB=ID_JOB,ID_USER=ID_USER).first()
        if(job.Start_time is None):
            job.Start_time =datetime.datetime.now()
            db.session.commit()
        return job.Start_time
    @classmethod
    def updateEndTime(cls,ID_JOB,ID_USER,End_time):
        job = cls.query.filter_by(ID_JOB=ID_JOB,ID_USER=ID_USER).first()
        if(job.End_time is None):
            job.End_time =End_time
            db.session.commit()
        return job.End_time
    @classmethod
    def getLastid(cls):
        sql ="SELECT AUTO_INCREMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Jobs'"
        result = db.engine.execute(sql)
        for r in result:
            return r[0]
    
    @classmethod
    def updateStatus(cls,ID_JOB,ID_USER,status):
        job = cls.query.filter_by(ID_JOB=ID_JOB,ID_USER=ID_USER).first()
        job.Statut = status
        db.session.commit()
        return status 
    @classmethod
    def updateProgress(cls,ID_JOB,ID_USER,progress):
        job = cls.query.filter_by(ID_JOB=ID_JOB,ID_USER=ID_USER).first()
        job.Percentage = progress
        db.session.commit()
        return progress
    @classmethod
    def removeJob(cls,ID_JOB,ID_USER):
        job = cls.query.filter_by(ID_JOB=ID_JOB,ID_USER=ID_USER).first()
        if (job):         
            db.session.delete(job)
            db.session.commit()  
            return {'message': 'The job {}, {} has been removed'.format(job.ID_JOB,job.ID_USER)}                   
        else :
            return{'message' : 'Can not remove job, job does not exist'}  
    @classmethod
    def getStatus(cls,ID_JOB,ID_USER):
        job = cls.query.filter_by(ID_JOB=ID_JOB,ID_USER=ID_USER).first()
        if (job):
            return {"status":job.Statut}
        else:
            return {"status":"None"}
    @classmethod
    def getLastid(cls):
        sql ="SELECT AUTO_INCREMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'Jobs'"
        result = db.engine.execute(sql)
        for r in result:
            return r[0]
        
######################### Users ########################### 

class UserModel(db.Model):
    __tablename__ = 'Users'
 
    ID_USER = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username =db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'ID_USER' :x.ID_USER,
                'fullName': x.username,
                'email' : x.email,
                'registered_on': str(x.registered_on),
                'admin': str(x.admin),
                'active': str(x.active)
            }

        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}
    @classmethod
    def changePass(cls,email,password):
        user = cls.query.filter_by(email=email).first()
        if (user):
            user.password = sha256.hash(password)
            db.session.commit()
            return {'message': "The Password has been changed successfully"}
        else :
            return{'message' : 'Can not change Password'}
    @classmethod
    def activateAccount(cls,email,activation):
        user = cls.query.filter_by(email=email).first()
        if (user):
            if (activation == "True"):
                user.active = True
                db.session.commit()
                return {'message': "The Account has been Activated successfully"}
            else:
                user.active = False
                db.session.commit()
                return {'message': "The Account has been Deactivated successfully"}
        else :
            return{'message' : 'Can not Activate account'}           
    @classmethod
    def setPermission(cls,email,permission):
        user = cls.query.filter_by(email=email).first()
        if (user):         
            if (permission == "True"):
                user.admin = True 
                db.session.commit()  
                return {'message': 'The Account has been set to Admin'}
            else :
                user.admin = False
                db.session.commit()
                return{'message': 'The Account has been set to user'}
                   
        else :
            return{'message' : 'Can not Activate account'}  
    
    @classmethod
    def removeUser(cls,email):
        user = cls.query.filter_by(email=email).first()
        if (user):         
            db.session.delete(user)
            db.session.commit()  
            return {'message': 'The User {} has been removed'.format(user.email)}                   
        else :
            return{'message' : 'Can not remove account'}  
    
    
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id_token = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)    