drop table if exists users;
create table users (
    username text primary key,
    email text,
    name text not null,
    password text not null,
    acctype text not null
);

drop table if exists students;
create table students (
    username text primary key,
    year integer not null
);

drop table if exists grades;
create table grades (
    username text primary key,
    C1 integer,     C11 integer,    C111 integer,   C112 integer,
    C12 integer,    C121 integer,   C13 integer,    C131 integer,
    C132 integer,   C14 integer,    C141 integer,   C142 integer,
    C143 integer,   C2 integer,     C21 integer,    C211 integer,
    C212 integer,   C213 integer,   C22 integer,    C221 integer,
    C222 integer,   C23 integer,    C231 integer,   C24 integer,
    C241 integer,   C242 integer,   C243 integer,   C244 integer,
    C3 integer,     C31 integer,    C311 integer,   C312 integer,
    C32 integer,    C321 integer,   C322 integer,   C323 integer,
    C33 integer,    C331 integer,   C4 integer,     C41 integer,
    C411 integer,   C412 integer,   C413 integer,   C414 integer,
    C415 integer,   C416 integer,   C417 integer,   C42 integer,
    C421 integer,   C422 integer,   C43 integer,    C431 integer,
    C432 integer,   C5 integer,     C51 integer,    C511 integer,
    C512 integer,   C52 integer,    C521 integer,   C522 integer,
    C6 integer,     C61 integer,    C611 integer,   C62 integer,
    C621 integer,   C622 integer,   C623 integer,   C63 integer,
    C631 integer,   C632 integer,   C64 integer,    C641 integer,
    C642 integer,   C643 integer
);
