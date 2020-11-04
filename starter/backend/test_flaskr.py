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
       
    '''
    Get Questions Page Not found 404
    ''' 
    def test_404_get_all_questions(self):
        given_page = 1000000
        req = self.client().get('/questions?page='+str(given_page))
        data = json.loads(req.data)
        self.assertEqual(req.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')



    '''
    Get All Questions from Catagory 200
    ''' 
    def test_get_all_question_from_catagory(self):
        given_catagory_id = 1
        req = self.client().get('/categories/'+str(given_catagory_id)+'/questions')
        data = json.loads(req.data)
        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])




    '''
    Get All Questions from Catagory that doesnt exist 404
    ''' 
    def test_get_all_question_from_catagory_doesnt_exist(self):
        given_catagory_id = 99990
        req = self.client().get('/categories/'+str(given_catagory_id)+'/questions')
        data = json.loads(req.data)
        self.assertEqual(req.status_code, 404)
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
        given_question_id = 1
        res = self.client().delete('/questions/'+str(given_question_id))
        data = json.loads(res.data)

        deleted_question = Question.query.filter(Question.id == given_question_id).one_or_none()
        self.assertEqual(res.status_code, 200) 
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], int(given_question_id))
        self.assertEqual(deleted_question, None)


    '''
    delete Question thats doesnt exist Error 422
    ''' 
    def test_delete_not_found_question(self):
        given_question_id = 100000
        req = self.client().delete('/questions/'+str(given_question_id))
        self.assertEqual(req.status_code, 422) 


    '''
    Search Question Success 200
    '''  
    def test_search_questions(self):
        # given_search_term = 'Who discovered penicillin'
        given_search_term = 'test question'
        searchQuesitonRequest = {
            'searchTerm': given_search_term
        }
        req = self.client().post('/questions/search', json=searchQuesitonRequest)
        data = json.loads(req.data)
        self.assertEqual(req.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertEqual(data['total_questions'], 1)
 
    '''
    Search Question not found 404
    '''  
    def test_search_questions_dont_exist(self):
         given_search_term = 'Random question that doesnt exist in the database 100%'
         searchQuesitonRequest = {
            'searchTerm': given_search_term
         }
         req = self.client().post('/questions/search', json=searchQuesitonRequest)
         data = json.loads(req.data)
         self.assertEqual(req.status_code,404)
         self.assertEqual(data['success'], False)
         self.assertEqual(data['message'], 'Not found')


        





   # Make the tests conveniently executable
if __name__ == "__main__":
       unittest.main()





        

