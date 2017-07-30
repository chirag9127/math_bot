CREATE TABLE user_request(
	id varchar(20) NOT NULL,
	query varchar(1024),
	intent varchar(1024),
	entities varchar(1024),
	PRIMARY KEY (id)
);

CREATE TABLE user_response(
	id varchar(20) NOT NULL,
	response varchar(1024),
	action varchar(1024),
	FOREIGN KEY (id) REFERENCES user_request(id)
);

ALTER TABLE questions_question
  ADD COLUMN correct BOOLEAN DEFAULT FALSE;