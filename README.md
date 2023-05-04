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
- pip install python-dotenv

FIRST TIME USAGE:
- install python prerequisites
- create `.env` file in your root directory (same directory as your main.py) and copy the content of `.env.back`.
- copy the content of the `.env.back` file and update the `OPENAI_API_KEY`.
- run the code using **python <main.py>**

COMMAND (project_root/commands/) files for generating the data:
1. prepare_embedding_data.py
 - this will create a new csv file based on the gun_data that we have. We must run this first to format the csv for the embedding.
2. create_embedding_for_gun_data.py
 - will create another column in our gun_data_embedding.csv to add the generated vector representation of the text.

API USAGE:
- We used python FLASK for creating the api. You need to run our `main.py` file using this command **python main.py** first to be able to use the api's.

API Documentation:

GET: `/chatgpt/question`
 - get all messages


POST: `/chatgpt/sentiment/checkifpositive`
 - return if 'message' you send is positive.
 ```
 BODY:
 {
    "message": "We honor your sacrifice and service to our country. You fought bravely for the freedoms and values we hold dear, andwill never forget the ultimate price you paid."
}
 ```
 RESPONSE:
 ```
{
    "gptanswer": "TRUE. The text is positive because it honors the sacrifice and service of the person who fought for the country. It expresses gratitude and acknowledges the bravery and courage of the person. The text also assures that the sacrifice has not gone unnoticed and the person will always be remembered as a hero.",
    "isPositive": true
}
 ```
 
 POST: `/chatgpt/sentiment/checkifpositiveimage`
 - return if 'image_url' you send is positive.
 ```
 BODY:
 {
    "image_url": "https://img.freepik.com/free-photo/gorgeous-arrangement-flowers-wallpaper_23-2149057015.jpg?w=2000"
}
 ```
 RESPONSE:
 ```
{
    "gptanswer": "TRUE. The image is positive because its a boquet of flowers that simbolizes beauty",
    "isPositive": true
}
 ```


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
> This is a proof of concept application for openai

  
