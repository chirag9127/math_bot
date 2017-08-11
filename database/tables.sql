CREATE TABLE user_request(
	id varchar(36),
	sender_id varchar(20) NOT NULL,
	query varchar(1024),
	intent varchar(1024),
	entities varchar(1024),
	PRIMARY KEY (id)
);



CREATE TABLE user_response(
	id varchar(36),
	sender_id varchar(20) NOT NULL,
	response varchar(1024),
	action varchar(1024),
	FOREIGN KEY (id) REFERENCES user_request(id)
);

ALTER TABLE user_response ADD UNIQUE(id);

ALTER TABLE questions_question
  ADD COLUMN correct BOOLEAN DEFAULT FALSE;

CREATE TABLE questions_given(
	id varchar(36),
	sender_id varchar(20) NOT NULL,
	question_id varchar(20) NOT NULL,
	time_asked timestamp DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (id) REFERENCES user_request(id)
	);
ALTER TABLE questions_given ADD UNIQUE(id);

CREATE TABLE answer_provided(
	id varchar(36),
	sender_id varchar(20) NOT NULL,
	question_id varchar(20) NOT NULL,
	time_asked timestamp DEFAULT CURRENT_TIMESTAMP,
	answer varchar(1024),
	is_correct BOOLEAN NOT NULL,
	FOREIGN KEY (id) REFERENCES user_request(id)
	);

ALTER TABLE answer_provided ADD UNIQUE(id);

CREATE TABLE answer_provided(
	id varchar(36),
	sender_id varchar(20) NOT NULL,
	question_id varchar(20) NOT NULL,
	time_asked timestamp DEFAULT CURRENT_TIMESTAMP,
	answer_id varchar(20) NOT NULL,
	test_id varchar(36),
	is_correct BOOLEAN NOT NULL,
	question_request_id varchar(36) NOT NULL
	);
ALTER TABLE answer_provided ALTER COLUMN test_id varchar (36);


# how many questions did I answer today, this week, this month


select count(*) from answer_provided where time_asked 
BETWEEN (select CURRENT_TIMESTAMP + interval '-1' day) 
AND (select CURRENT_TIMESTAMP) 
AND is_correct = 1 
AND sender_id = '1384341615018517';
;

# how many questions did I get right today, this week, this month

select count(*) from answer_provided where time_asked 
BETWEEN (select CURRENT_TIMESTAMP + interval '-7' day) 
AND (select CURRENT_TIMESTAMP)
AND is_correct = 1 AND sender_id = x;

select count(*) from answer_provided where time_asked 
BETWEEN (select CURRENT_TIMESTAMP + interval '-30' day) 
AND (select CURRENT_TIMESTAMP) 
AND is_correct = 1 
AND sender_id = x;

# score in given topic - sum over eternity


select count(*)
from answer_provided a join questions_question q 
on q.id = a.question_id
where a.is_correct = 1 
AND q.topic = 'Arithmetic' ANDAND a.sender_id = '1384341615018517';

# top two areas , bottom two areas - based on correct answers

# top 2
select count(*), q.topic
from answer_provided a join questions_question q 
on q.id = a.question_id
where a.is_correct = 1 AND a.sender_id = '1384341615018517'
GROUP BY q.topic
ORDER BY count(*) DESC
LIMIT 2;

# bottom 2
select count(*), q.topic
from answer_provided a join questions_question q 
on q.id = a.question_id
where a.is_correct = 1 AND a.sender_id = '1384341615018517'
GROUP BY q.topic 
LIMIT 2;

# get questions answered during last week
select DATE(time_asked) AS ForDate, count(*)
from answer_provided 
where time_asked 
BETWEEN (select CURRENT_TIMESTAMP + interval '-7' day) 
AND (select CURRENT_TIMESTAMP) AND
sender_id = '1384341615018517'
GROUP BY ForDate;

# get questions answered correctly during last week
select DATE(time_asked) AS ForDate, count(*)
from answer_provided 
where time_asked 
BETWEEN (select CURRENT_TIMESTAMP + interval '-7' day) 
AND (select CURRENT_TIMESTAMP) AND is_correct = 1 AND
sender_id = '1384341615018517'
GROUP BY ForDate;

select DATE(time_asked) AS ForDate, count(*)
from answer_provided 
where time_asked 
BETWEEN (select CURRENT_TIMESTAMP + interval '-8' day) 
AND (select CURRENT_TIMESTAMP) AND is_correct = 1 AND
sender_id = '1384341615018517'
GROUP BY ForDate;