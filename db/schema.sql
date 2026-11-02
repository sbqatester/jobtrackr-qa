CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE applications (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company     VARCHAR(150) NOT NULL,
    role        VARCHAR(150) NOT NULL,
    status      VARCHAR(20) NOT NULL DEFAULT 'Applied'
                CHECK (status IN ('Applied','Screening','Interview','Offer','Rejected')),
    salary      NUMERIC(10,2) CHECK (salary IS NULL OR salary > 0),
    source      VARCHAR(50),
    applied_on  DATE NOT NULL DEFAULT CURRENT_DATE,
    updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE status_history (
    id             SERIAL PRIMARY KEY,
    application_id INTEGER NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    old_status     VARCHAR(20),
    new_status     VARCHAR(20) NOT NULL,
    changed_at     TIMESTAMP NOT NULL DEFAULT NOW()
);
