# Top10-Youtube-Videos
This Project is a small Web application to give you top 10 Youtube videos on any topic of your interest. The list of top 10 videos consists of Video Title, number of comments and Youtube links and the list is shown in descending order of comments. 

# Prerequisites
You need to create Youtube API key and use it in the variable - API_KEY. For creating Youtube API key, refer to - https://developers.google.com/youtube/v3/getting-started

# Installation steps
sudo yum update <br>
sudo yum install python3 <br>
sudo yum install python3-pip <br>
python3 --version <br>
pip3 --version <br>
python3 -m venv venv <br>
cd ~/venv <br>
source bin/activate <br>

pip install flask <br>
flask run <br>

pip install gunicorn <br>
gunicorn -w 4 -b 0.0.0.0:5000 app:app --daemon <br>

# author
https://www.linkedin.com/in/jasmine-maheshwari-8812948 <br>

# About Author
I am a tech enthusiast , love to experiment on technology without boundaries. 
