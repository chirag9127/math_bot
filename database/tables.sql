CREATE TABLE user_request(
	id int NOT NULL,
	query varchar(1024),
	intent varchar(1024),
	entities varchar(1024),
	PRIMARY KEY (id)
);

CREATE TABLE user_response(
	id int NOT NULL,
	response varchar(1024),
	action varchar(1024),
	FOREIGN KEY (id) REFERENCES user_request(id)
);

