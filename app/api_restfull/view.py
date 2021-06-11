from .models import Subject
from app import db
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from app.api_restfull import api_restfull_bp
from flask import jsonify, request, make_response
import datetime


api = Api(api_restfull_bp)
resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'teacher': fields.String,
    'type' : fields.String,
    'is_exam' : fields.Boolean,
    'specialty' : fields.String,
    'semester' : fields.Integer,
}

subject_create = reqparse.RequestParser()
subject_create.add_argument('name', type=str, help='Name is required!', required=True)
subject_create.add_argument('teacher', type=str, help='Teacher is required!', required=True)
subject_create.add_argument('type', type=str, help='Type is required!', required=True)
subject_create.add_argument('specialty', type=str, help='Specialty is required!', required=True)
subject_create.add_argument('semester', type=int, help='Semester is required!', required=True)


subject_update = reqparse.RequestParser()
subject_update.add_argument('name', type=str, help='Name is required!', required=True)
subject_update.add_argument('teacher', type=str, help='Teacher is required!', required=True)
subject_update.add_argument('type', type=str, help='Type is required!', required=True)
subject_update.add_argument('is_exam', type=str, help='Is exam is required!', required=True)
subject_update.add_argument('specialty', type=str, help='Specialty is required!', required=True)
subject_update.add_argument('semester', type=int, help='Semester is required!', required=True)


class TaskItem(Resource):

    def post(self):
        args = subject_create.parse_args()
        try:
            subject = Subject(name=args['name'], teacher=args['teacher'], type=args['type'], specialty=args['specialty'], semester=args['semester'])
            db.session.add(subject)
            db.session.commit()
            # return jsonify({'message': 'Data add in db!'}), 201 777   ?????
            return make_response(jsonify({'message': 'Data add in db!'}))
        except:
            db.session.rollback()
            # return jsonify({'message': 'Error when adding data!'}) ?????
            return make_response(jsonify({'message': 'Error when adding data!'}), 201)



    @marshal_with(resource_fields, envelope='resource')
    def get(self, id=None):
        if id is None:
            tasks_all = Subject.query.all()
            return tasks_all
        else:
            task = Subject.query.filter_by(id=id).first()
            if not task:
                return make_response(jsonify({'message': 'Subject not found!'}))
            return task

    # @marshal_with(resource_fields, envelope='resource')
    def delete(self, id):
        task = Subject.query.filter_by(id=id).first()
        if not task:
            return make_response(jsonify({'message': 'Subject not found!'}), 404)
        db.session.delete(task)
        db.session.commit()
        return  make_response(jsonify({'message': 'The task has been deleted'}))

    # @marshal_with(resource_fields, envelope='resource')
    def put(self, id):
        subject = Subject.query.filter_by(id=id).first()
        if not subject:
            return make_response(jsonify({'message': 'Subject not found!'}), 404)
        args = subject_update.parse_args()

        subject.name = args['name']
        subject.teacher = args['teacher']
        subject.type = args['type']
        if args['is_exam']=='True':
            subject.is_done = True
        elif args['is_exam']=='False':
            subject.is_done = False
        subject.specialty = args['specialty']
        subject.semester = args['semester']
        try:
            db.session.commit()
            return make_response(jsonify({"message": "Subject succesfully update!"}))
        except:
            db.session.rollback()
            return make_response(jsonify({'message': 'Error when updating data!'}), 201)




api.add_resource(TaskItem, '/subject', '/subject/<int:id>')
