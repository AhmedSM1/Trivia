import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://root:rootpwd@localhost:5432/trivia_test'

        # self.database_path = 'postgresql://root:rootpwd@localhost:5432/trivia_test'

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


    '''
    create Catagory
    '''
    def test_create_catagory(self):
        category = Category( type = 'technology')
        request = self.client().post('/categories', json=category.to_dict())
        data = json.loads(request.data)
        self.assertEqual(request.status_code, 201) 

    '''
    Get Categories Success 200
    '''
    def test_get_catagories(self):
        request = self.client().get('/categories')
        print(request)
        data = json.loads(request.data)
        self.assertEqual(request.status_code, 200) 
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])


    '''
    Get Categories Page not found 404
    '''
    def test_not_find_catagories(self):
        request = self.client().get('/categories/')
        data = json.loads(request.data)
        self.assertEqual(request.status_code, 404)
        self.assertEqual(data['success'], False)
       


    '''
    Get Questions Success 200
    ''' 
    def test_get_all_questions(self):
        results = self.client().get('/questions')
        data = json.loads(results.data)
        self.assertEqual(results.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
       

    def test_404_get_all_questions_beyond_valid_page(self):
        given_page = 1000000
        res = self.client().get('/questions?page='+str(given_page))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')










    '''
    Create Question Success 201
    ''' 
    def test_create_question(self):
        question = Question(question= 'test question',
            answer= 'test answer', difficulty= 1,
            category=  1)

        total_questions_before = len(Question.query.all())
        results = self.client().post('/questions', json=question.to_dict())
        data = json.loads(results.data)
        total_questions_after = len(Question.query.all())
        self.assertEqual(results.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_questions_after, total_questions_before + 1)


    '''
    delete Question Success 200
    ''' 
    def test_delete_question(self):
        given_question_id = 9
        res = self.client().delete('/questions/'+str(given_question_id))
        data = json.loads(res.data)

        deleted_question = Question.query.filter(Question.id == given_question_id).one_or_none()
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], int(given_question_id))
        self.assertEqual(deleted_question, None)


    '''
    delete Question Success 404
    ''' 
    def test_delete_not_found_question(self):
        given_question_id = 100000
        results = self.client().delete('/questions/'+str(given_question_id))
        deleted_question = Question.query.filter(Question.id == given_question_id).one_or_none()
        self.assertEqual(results.status_code, 404) 
        





   # Make the tests conveniently executable
if __name__ == "__main__":
       unittest.main()





        

