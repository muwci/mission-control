drop table if exists scores;
create table scores (
    studentid integer primary key,
    name text not null,
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
