# pgres_database.md

Documentation on the heroku postgres database.

## CLI Access
To view all tables: `\dt`
To leave CLI: `\q`
To view all columns: `select * from <table>;`

## Table Information
```
CREATE TABLE twitteraccs(
    key                 SERIAL PRIMARY KEY,
    email               varchar(40) NOT NULL,
    twitter_id          BIGSERIAL NOT NULL,
    access_token        varchar(255) NOT NULL,
    access_token_secret varchar(255) NOT NULL,
    hashtags            varchar(255)
);
```
Hashtags table to maintain retweeted hashtags.
```
CREATE TABLE hashtags(
    key                 SERIAL PRIMARY KEY,
    hashtags            varchar(255) NOT NULL,
    retweets            INT NOT NULL,
);
```