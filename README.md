# OpenAI chatbot with embedding 

Requirements:

Python 3.x

- pip install -U Flask
- pip install openai
- pip install pandas
- pip install numpy
- pip install pprint
- pip install Flask-RESTful
- pip install -U flask-cors

COMMAND (project_root/commands/) files for generating the data:
1. prepare_embedding_data.py
 - this will create a new csv file based on the gun_data that we have. We must run this first to format the csv for the embedding.
2. create_embedding_for_gun_data.py
 - will create another column in our dun data embedding.csv to add the generated vector representation of the text

Usage:
- First create a openaiapikey.txt in the project root directory and put  your api key inside.
- run the code using **python <main.py>**

API USAGE:
- First run our python application using **python main.py**

API Documentation:

GET: `/chatgpt/question`
 - get all messages

POST: `/chatgpt/question`
 - ask a question
 ```
 BODY:
 {
  "question": "sample question you want to  ask"
 }
 ```
 RESPONSE:
 ```
 {
    "gptanswer": "Sure! You can watch a video of the Akdal Ghost TR01 by following this link: <iframe src=\\https://www.youtube.com/embed/PZy55e6NSqU\\\" title=\\\"YouTube video player\\\" allowfullscreen></iframe>.",
    "question": "how about a video of akdal ghost?"
 }
 ```
 ![image](https://user-images.githubusercontent.com/4272175/236098410-e2db110b-7c72-4d90-b322-6ac4152eae91.png)
                                                                                                     
                                                                                                      
                                                                                                      
**NOTE**
> This is a prop on concept application for openai

  
