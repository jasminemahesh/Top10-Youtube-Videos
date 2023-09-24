# Top10-Youtube-Videos
This Project is a small Web application to give you top 10 Youtube videos on any topic of your interest. The list of top 10 videos consists of Video Title, number of comments and Youtube links and the list is shown in descending order of comments. 

# Installation steps
sudo yum update
sudo yum install python3
sudo yum install python3-pip
python3 --version
pip3 --version
python3 -m venv venv
cd ~/venv
source bin/activate

pip install flask
flask run

pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app --daemon
