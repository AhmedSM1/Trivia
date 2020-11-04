import os
from flask import Flask, request, abort, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_api import status
import json
import random
from models import setup_db, Question, Category,db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={'/': {"origins": "*"}})


  
  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers',
      'Content-Type,Authorization,true')
    response.headers.add(
      'Access-Control-Allow-Methods',
      'GET,PATCH,POST,DELETE,OPTIONS')
    return response



  def findQuestionByQuestionId(question_id):
    question = Question.query.get(question_id)
    if not question:
       abort(404)
    else:
       return question



  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


  def getQuestionsService(request):
    questions_list = Question.query.order_by(Question.id).all()
    paginated_questions = paginate_questions(request,questions_list)
    categories = Category.query.all()

    if len(paginated_questions) == 0:
            abort(404)

    return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(questions_list),
            'categories': {category.id: category.type for category in categories},
            'current_category': None
        })
    
         

  def find_category(id):
    category = Category.query.get(id)
    if not category:
      abort(404)
    else:
      return category

  def getCatagoriesService():
   categories =   Category.query.all()
   categories_type = {}
   for category in categories:
     categories_type[category.id] = category.type

   if len(categories_type) == 0:
            abort(404)

   return jsonify({
    'success': True,
    'categories': categories_type,
    'total_categories': len(categories)
    })


  def createCatagoryService(type):
    try:
       category = Category(type= type)
       db.session.add(category)
       db.session.commit()
       return jsonify({
           'success': True,
           'categories_type': category.type,
       })
    except Exception as e:
        print("Exception occured:  "+ e)
        db.session.rollback()
    finally:
        db.session.close()
 

  def createQuestionsService(question):
    try:
        db.session.add(question)
        db.session.commit()
        return jsonify({
                'success': True,
                'id': question.id,
                'question': question.question,
                'answer': question.answer
            })

        print("Question was successfully created")
    except Exception as e:
        print("Exception occured:  "+ e)
        db.session.rollback()
    finally:
        db.session.close()


  def deleteQuestionService(question_id):
    try:
          question = findQuestionByQuestionId(question_id)
          db.session.delete(question)
          db.session.commit()
          return jsonify({
                'success': True,
                'deleted': question_id,
                'total_questions': len(Question.query.all())
            })
    except Exception as e:
        print(e)
        db.session.rollback()
        abort(422)
    finally:
       db.session.close()


  def getQuestionsBasedOnCategoriesService(category_id):
      try:
          category = find_category(category_id)
          questions = Question.query.filter(
                Question.category == str(category_id)).all()
          return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
                'current_category': category_id
            })
      except:
            abort(404)



  def searchQuestionService(request,search_term):
      question_list = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
      results = paginate_questions(request, question_list)

      if len(results) == 0:
             abort(404)

      return jsonify({
                'success': True,
                'questions': results,
                'total_questions': len(results)
            })




  def playQuizService(current_category,previous_questions):
     try:
       if current_category['type'] == 'click':

        questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()

       else:
        questions = Question.query.filter_by(
                    category=current_category['id']).filter(Question.id.notin_((previous_questions))).all()


       if questions:
                question = random.choice(questions)
                question_formatted = question.format()
       else:
                question_formatted = False


       return jsonify({
        'success': True,
        'previous_questions': previous_questions,
        'question': question_formatted
            })
     except Exception as e:
        print(e)
        # abort(500)








  @app.route('/categories')
  def getAllCatagories():
   return getCatagoriesService(), status.HTTP_200_OK
 


  @app.route('/categories', methods=['POST'])
  def createCatagory():
    request_body =  request.get_json()
    type = request_body.get('type', None)
    return createCatagoryService(type), status.HTTP_201_CREATED

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def getQuestionsBasedOnCategories(category_id):
     return getQuestionsBasedOnCategoriesService(category_id), status.HTTP_200_OK


  


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def getQuestions():
    return getQuestionsService(request), status.HTTP_200_OK


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''


  @app.route('/questions', methods=['POST'])
  def createQuestions():
    request_body =  request.get_json()
    if not ('question' in request_body and 'answer' in request_body and 'difficulty' in request_body and 'category' in request_body):
            abort(422)
    question = Question(
    question = request_body.get('question', None),
    answer = request_body.get('answer', None),
    category = request_body.get('category', None),
    difficulty = request_body.get('difficulty', None))
    return createQuestionsService(question), status.HTTP_201_CREATED

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route("/questions/<question_id>", methods=['DELETE'])
  def deleteQuestion(question_id):
      return deleteQuestionService(question_id), status.HTTP_200_OK



  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def searchQuestion():
      request_body =  request.get_json()
      if not ('searchTerm' in request_body):
        abort(422)

      search_term = request_body.get('searchTerm', None)
      return searchQuestionService(request,search_term), status.HTTP_200_OK



  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def playQuiz():
        request_body = request.get_json()
        if not ('quiz_category' in request_body and 'previous_questions' in request_body):
                abort(422)
        current_category = request_body.get('quiz_category', None)
        previous_questions = request_body.get('previous_questions', [])
        return playQuizService(current_category,previous_questions), status.HTTP_200_OK













  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(500)
  def server_error(error):
    return 'System error', 500

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

  return app








