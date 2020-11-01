import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_path = 'postgresql://root:rootpwd@localhost:5432/trivia'
        self.database_path = 'postgresql://root:rootpwd@localhost:5432/trivia_test'
        setup_db(self.app, self.database_path)

        # self.new_catagory = {
        #     'type': 'technology'
        # }

        # self.new_question = {
        #     'question': 'What does “HTTP” stand for?',
        #     'answer': 'HyperText Transfer Protocol',
        #     'difficulty': 1,
        #     'category': 1
        # }




        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()




    



    question = Question(question = 'What does “HTTP” stand for?',
        answer = 'HyperText Transfer Protocol',
        difficulty = 1,
        category = 1 )




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
    def should_create_catagory(self):
        print("Test ")
        catagory = Category( type = 'technology')
        request = self.client().post('/categories', json=catagory)
        print(request)
        data = json.loads(request.data)
        print(data)
        self.assertEqual(request.status_code, 201) 
        self.assertEqual(data['success'], True)
        self.assertEqual(data['type'],catagory.type)










    '''
    Get Categories
    '''
    # def should_get_catagories(self):
    #     results = self.client().get('/categories')
    #     print(results)
    #     data = json.loads(results.data)
    #     self.assertEqual(results.status_code, 200) 
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['categories'])
    #     self.assertEqual(len(data['categories']), 1) 


    # def should_not_find_catagories(self):
    #     results = self.client().get('/categories/')
    #     data = json.loads(results.data)
    #     self.assertEqual(results.status_code, 404)
    #     self.assertEqual(data['success'], False)
       


        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()