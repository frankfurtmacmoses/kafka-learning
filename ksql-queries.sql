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



