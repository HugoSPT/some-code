CREATE DATABASE hotel;

use hotel;

CREATE TABLE accommodation (
	id            int             NOT NULL   auto_increment,
	type          varchar(255)    NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE stars_rating (
	id            int             NOT NULL   auto_increment,
	rating        int             NOT NULL,
	image_url     varchar(64),
	PRIMARY KEY (id)
);

CREATE TABLE hotel (
	id                   int             NOT NULL   auto_increment,
	name                 varchar(255)    NOT NULL,
	stars_rating_id      int             NOT NULL,
	accommodation_id     int             NOT NULL,
	address              varchar(255),
	PRIMARY KEY (id),
	FOREIGN KEY (stars_rating_id) REFERENCES stars_rating(id),
	FOREIGN KEY (accommodation_id) REFERENCES accommodation(id)
);

INSERT INTO accommodation (
	type
) VALUES
	('Hotel'),
	('Hostel'),
	('Motel'),
	('Cottage'),
	('Chalet'),
	('Mansion'), 
	('Lodge');

INSERT INTO stars_rating (
	rating
) VALUES
	(1), (2), (3), (4), (5);
