Testing procedure:
Ensure docker desktop is install and running 

Ensure python3.8 is installed on the your computer

Else on mac run brew install:  brew install python@3.8

From terminal, type:  git clone https://github.com/frankfurtmacmoses/kafka-learning.git

followed by:  git checkout version-3.0

type: python3.8 -m venv venv

on mac whe, type source/venv/bin/activate

type pip install -r requirements.txt

Navigate to home-directory of cloned repocle

type: docker-compose up -d

Confirm all containers are running: docker ps -a

From terminal type : Python3.8 streaming.py or if directory is open from IDE, right click and run streaming.py

from display confirm tweets are been collected......

on another terminal, 
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088 
 
 or 

 ksql http://localhost:8088

From ksql prompt, type as it is:   print 'appletopics'    

To desplay output in a well formatted way : 

create  stream appletopics_st(
user_id VARCHAR ,
user_name VARCHAR,
number_of_follower VARCHAR,
location VARCHAR,
nubmer_of_time_retweeted VARCHAR
)
WITH(
    KAFKA_TOPIC ='appletopics',
    VALUE_FORMAT = 'JSON' 
);



select * 
from appletopics_st
emit changes;


SET 'auto.offset.reset' = 'earliest';

select * 
from appletopics_st 
emit changes;





To kill the processes press Control + C 


