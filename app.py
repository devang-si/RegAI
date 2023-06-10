# Importing necessary libraries
from flask import Flask, request, jsonify
from flask.wrappers import Response
from loadDocs import initialize_qa, get_answer

# Creating a Flask application
app = Flask(__name__)

# Initialize qa when the app starts
qa = initialize_qa()

# Defining a POST endpoint
@app.route('/api', methods=['POST'])
def post_json():
  data = request.get_json(force=True)

  if 'query' not in data:
      response = {
          'status': 'error',
          'message': 'Missing required key: query'
      }
      return jsonify(response), 400

  query = data['query']
  answer = get_answer(qa, query)

  response = {
      'status': 'success',
      'message': 'Query received successfully',
      'answer': answer
  }
  return jsonify(response), 200

# Running the Flask application
if __name__ == '__main__':
    app.run(debug=True)





# from flask import Flask, request, jsonify
# import openai
# from flask_cors import CORS
# import os

# app = Flask(__name__)
# CORS(app)
# openai.api_key = os.environ['OPENAI_API_KEY']



# @app.route('/')
# def index():
#   return 'Hello from Flask!'


# @app.route('/api', methods=['POST'])
# # @app.route('/api', methods=['POST'])
# def api():
#   try:
#     if not request.json or 'userPrompt' not in request.json:
#       raise ValueError(
#         "Request body must be JSON and include a 'userPrompt' key")

#     user_prompt = request.json['userPrompt']
#     print("User Prompt: " + user_prompt)

#     # First OpenAI API call
#     private_prompt = openai.ChatCompletion.create(
#       model=
#       "gpt-3.5-turbo",  # replace this with the correct model name for GPT-4 when it becomes available
#       messages=[
#         {
#           "role": "user",
#           "content": user_prompt
#         },
#         {
#           "role":
#           "system",
#           "content":
#           # "Modify this prompt and return a prompt which does not have any personal information."
#           "Rephrase the prompt masking any personal information like name, address, location, organisation name, age"
#         },
#       ])

#     first_response = private_prompt['choices'][0]['message']['content']
#     print("\n")
#     print("First response: " + first_response)
#     print("\n")

#     # Second OpenAI API call
#     response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
#                                             messages=[
#                                               {
#                                                 "role": "user",
#                                                 "content": first_response
#                                               },
#                                             ])

#     final_response = response['choices'][0]['message']['content']
#     print("Second response: " + final_response)

#     print("\n")
#     print("---------------------")
#     print("\n")

#     #record userPrompt, privatePrompt, and response to a csv file
#     with open('data.csv', 'a') as f:
#       f.write(f"{user_prompt},{first_response},{final_response}\n")

#     return jsonify(final_response)

#   except Exception as e:
#     # Log the error and return a 500 response
#     print(str(e))
#     app.logger.error(f"An error occurred: {str(e)}")
#     return jsonify(error=str(e)), 500

# app.run(host='0.0.0.0', port=81)
