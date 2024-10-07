CREATE TABLE users (
    sub VARCHAR(1000) NOT NULL unique,
    avatar VARCHAR(1000) NOT NULL,
    username VARCHAR(256) NOT NULL,
    email VARCHAR (319) NOT NULL
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    sub VARCHAR(1000) REFERENCES users(sub),
    review_text VARCHAR(500) NOT NULL,
    place_reviewed TEXT not null,
    time_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    place_type TEXT not null,
    star_count INT not null,
    images bytea,
    place_id VARCHAR(1000)
);

CREATE TABLE user_reviews (
    sub VARCHAR(1000) REFERENCES users(sub),
    review_id INT REFERENCES reviews(review_id),
    PRIMARY KEY (sub, review_id)
);

CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    sub VARCHAR(1000) REFERENCES users(sub),
    review_id INT REFERENCES reviews(review_id) on delete cascade,
    comment_text VARCHAR(250) NOT NULL,
    time_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- CREATE TABLE images (
--     image_id SERIAL PRIMARY KEY,
--     image_code bytea,
-- );