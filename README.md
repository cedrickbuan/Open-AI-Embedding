# Open-AI-Embedding

Libraries
- pip install -U Flask
- pip install openai
- pip install pandas
- pip install numpy
- pip install pprint
- pip install Flask-RESTful
- pip install -U flask-cors

We have 3 python file to run here.
1. prepare_embedding_data.py
 - this will create anew csv file based on the gund_data that we have
2. create_embedding_for_gun_data.py
 - will create another column in our dun data embedding.csv to add the generated vector representation of the text
3. main.py
 - the main application, will use the embedding to determine the answer for the question of the user.


Usage:
- First create a openaiapikey.txt in the project root directory and put  your api key inside.
- run the code using python <file_name.py>

API USAGE:
- First run our python application using "python main.py"


API Documentation:

GET: /chatgpt/question
 - get all messages

POST: /chatgpt/question
 - ask a question
 BODY:
 {
  "question": "sample question you want to  ask"
 }
 
 RESPONSE:
 {
    "gptanswer": "Sure! You can watch a video of the Akdal Ghost TR01 by following this link: <iframe src=\\https://www.youtube.com/embed/PZy55e6NSqU\\\" title=\\\"YouTube video player\\\" allowfullscreen></iframe>.",
    "question": "how about a video of akdal ghost?"
 }
 ![image](https://user-images.githubusercontent.com/4272175/236098410-e2db110b-7c72-4d90-b322-6ac4152eae91.png)
                                                                                                     
                                                                                                      
                                                                                                      
                                                                                                      
  
