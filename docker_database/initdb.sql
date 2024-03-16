CREATE TABLE person (
  id BIGINT PRIMARY KEY,
  name VARCHAR(30) NOT NULL,
  cathegory_ids BIGINT[],
  balance BIGINT NOT NULL
);

CREATE TABLE cathegory_type (
  id BIGSERIAL PRIMARY KEY,
  type_name TEXT NOT NULL
);

INSERT INTO cathegory_type(type_name) VALUES ('expense'), ('income');

CREATE TABLE operation_type (
  id BIGSERIAL PRIMARY KEY,
  type_name TEXT NOT NULL
);

INSERT INTO operation_type(type_name) VALUES ('expense'), ('income');

CREATE TABLE cathegory (
  id BIGSERIAL PRIMARY KEY,
  person_id BIGINT REFERENCES person(id) ON DELETE CASCADE,
  cathegory_type_id BIGINT REFERENCES cathegory_type(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  money_limit BIGINT NOT NULL DEFAULT 0,
  current_money BIGINT NOT NULL DEFAULT 0
);

CREATE TABLE operation (
  id BIGSERIAL PRIMARY KEY,
  date TIMESTAMP NOT NULL DEFAULT now(),
  operation_type_id BIGINT REFERENCES operation_type(id) ON DELETE CASCADE,
  person_id BIGINT REFERENCES person(id) ON DELETE CASCADE,
  cathegory_id BIGINT REFERENCES cathegory(id) ON DELETE CASCADE,
  money_amount BIGINT NOT NULL,
  commentary TEXT
);
