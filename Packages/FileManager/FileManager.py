from flask_restful import Resource, reqparse
from flask import send_file
import werkzeug, os
import shutil

UPLOAD_FOLDER = '/home/mhamnache/Simulations'
parser = reqparse.RequestParser()
parser.add_argument('file',type=werkzeug.datastructures.FileStorage, location='files')
parser.add_argument('id_job', help = 'This field cannot be blank', required = False)
parser.add_argument('Nom_simu', help = 'This field cannot be blank', required = False)
class ParamFileUpload(Resource):
    decorators=[]

    def post(self):
        data = parser.parse_args()
        #print(data)
        if data['file'] == "":
            return {
                    'data':'',
                    'message':'No file found',
                    'status':'error'
                    }
        param = data['file']
        #print(param)
        if param:
            filename = 'param.in'
            #print(os.path.join(UPLOAD_FOLDER+'/'+data['id_job'],filename))
            param.save(os.path.join(UPLOAD_FOLDER +'/'+data['id_job'],filename))
            return {
                    'data':'',
                    'message':'photo uploaded',
                    'status':'success'
                    }
        return {
                'data':'',
                'message':'Something when wrong',
                'status':'error'
                }
class DownloadResult(Resource):
    def post(self):
        data = parser.parse_args()
        print(data['id_job'])
        print(data['Nom_simu'])
        try:
            path = UPLOAD_FOLDER+'/'+data['id_job']
            fileName = data['Nom_simu']+'-'+data['id_job']
            return send_file(shutil.make_archive(fileName, 'zip', path), as_attachment=True)
        except:
            return{
                'message' : 'Error'
            }
