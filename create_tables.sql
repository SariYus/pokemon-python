USE sql_intro;


CREATE TABLE Trainer (
    name VARCHAR(50) PRIMARY KEY,
    town VARCHAR(50)
);

create TABLE pokemon(
    id int PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20),
    height NUMERIC,
    weight NUMERIC
);

CREATE TABLE Owns (
    pokemon_id INT,
    trainer_name VARCHAR(50),
    PRIMARY KEY (pokemon_id, trainer_name),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id)
    ON DELETE CASCADE,
    FOREIGN KEY (trainer_name) REFERENCES Trainer(name)
    ON DELETE CASCADE
);

create table types(
    name VARCHAR(20) primary key
);


create TABLE pokemon_type(
    pokemon_id int,
    typ VARCHAR(20),
    PRIMARY KEY (pokemon_id, typ),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id)
    ON DELETE CASCADE,
    FOREIGN KEY (typ) REFERENCES types(name)
    ON DELETE CASCADE
);
