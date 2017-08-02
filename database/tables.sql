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
	test_id varchar(20),
	is_correct BOOLEAN NOT NULL,
	FOREIGN KEY (id) REFERENCES user_request(id)
	);