CREATE TABLE urls IF NOT EXISTS(
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255),
    created_at date);


CREATE TABLE url_checks IF NOT EXISTS(
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id bigint REFERENCES urls (id),
    status_code int,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at date);


INSERT INTO urls(name, created_at) VALUES ('https://www.google.com', '2023-09-14');
INSERT INTO urls(name, created_at) VALUES ('http://docs.python.org:80', '2023-09-14');