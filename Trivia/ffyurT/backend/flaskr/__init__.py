import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    def paginate_questions(request, selection):
        page= request.args.get('page', 1, type=int)
        start= (page - 1) * QUESTIONS_PER_PAGE
        end= start + QUESTIONS_PER_PAGE
        questions= [question.format() for question in selection]
        current_questions= questions[start:end]

        return current_questions


    @app.route('/categories', methods=['GET'])
    def categories():
        selection= Category.query.all()
        categories= {cat.id: cat.type for cat in selection}
        #categories= [cat.format for cat in categories]
        return  jsonify({"categories":categories})
   
       
    @app.route('/questions', methods= ['GET'])
    def questions():
        selection= Question.query.order_by(Question.id).all()
        questions= paginate_questions(request, selection)
        #current_Category= " " #[question.category for question in current_questions]
        selection2= Category.query.order_by(Category.id).all()
        categories= {cat.id: cat.type for cat in  selection2}
        #categories= [cat.format for cat in selection2]
        total_questions= len(selection)
        current_category= "History"
        
        if len(selection) == 0:
            abort(404)
        return jsonify({"questions":questions, 
                    "totalQuestions":total_questions, "currentCategory": current_category,
                    'categories': categories})

        #delete
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question_byId(question_id):
        try:
            question=  Question.query.filterby(Question.id==question_id).one_or_none()
            if question is None:
                abort(404)
        
            question.delete()
            selection= Question.query.order_by(Question.id).all()
            current_questions= paginate_questions(request, selection)

        except:
            abort(422)

        #return jsonify({ 'deleted':question.id,#'question': current_questions,
                        #success': True})
                        #"totalQuestions": selection
        
   
    
    @app.route('/questions', methods=['POST'])
    def create_Question():
        body= request.get_json()
        
        question= body.get('question', None)
        answer= body.get('answer', None)
        category= body.get('category', None)
        difficulty= body.get('difficulty', None)
        try:
            question1= Question(question=question, answer=answer, category=category, difficulty=difficulty)
            question1.insert()

            selection= Question.query.order_by(Question.id).all()
            current_questions= paginate_questions(request, selection)

            return jsonify({'question':current_questions})
                        #'created':question.id,
                        #'success': True,})
                        #'totalQuestions': len(selection)
        except:
            abort(400)

    #TEST: When you submit a question on the "Add" tab,
    #the form will clear and the question will appear at the end of the last page
    #of the questions list in the "List" tab.
    


   # @TODO:
    #Create a POST endpoint to get questions based on a search term.
    #
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body= request.get_json()
        search_term= body.get('searchTerm', None)
        print(search_term)
        if search_term:
            search_results= Question.query.filterby(
                Question.question.ilike(f'%{search_term}')).all()

            return jsonify({'questions':[que.format for que in search_results],
            'total_questions': len(search_results),
            'current_category': 'History'})

    #TEST: Search by any phrase. The questions list will update to include
    #only question that include that string within their question.
    #Try using the word "title" to start.
    
    
    
    #@TODO:
    #Create a GET endpoint to get questions based on category.
   
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_question_by_category(category_id):
        try:
            selection= Category.query.filterby(Category.id==category_id).one_or_none()
            category=selection.type
            question= Question.query.filterby(Question.category==category)
            return jsonify({"question": question, "totalQuestions":len(question), "currentCategory":"History"})   #return question
        except:    
            abort(422)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(422)
    def unable_to_load(error):
        return jsonify({'error':'Unable to load questions. Please try your request again'}), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error':'resource not found'}), 404
    
    

    return app

