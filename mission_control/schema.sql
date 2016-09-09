drop table if exists scores;
create table scores (
    studentemail text primary key,
    scoreC1 integer,
    scoreC2 integer,
    scoreC3 integer,
    scoreC4 integer,
    comments text not null
);

drop table if exists users;
create table users (
    useremail text primary key,
    name text not null,
    password text not null,
    acctype text not null
);

INSERT INTO users VALUES ('clyon@muwci.net', 'C. Lyon', 'sealions', 'FAC');
INSERT INTO users VALUES ('graffe@muwci.net', 'G. Raffe','giraffes', 'STU');
INSERT INTO users VALUES ('rbbit@muwci.net', 'R. Bbit','rabbits', 'STU');

INSERT INTO scores VALUES ('graffe@muwci.net', 5, 6, 7, 5, "the neck! the neck!");
INSERT INTO scores VALUES ('rbbit@muwci.net', 7, 5, 4, 5, "led Alice down that hole thing");
