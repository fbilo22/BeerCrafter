PRAGMA foreign_keys = ON;

CREATE TABLE recipe (
   id integer PRIMARY KEY,
   recipe_name text NOT NULL UNIQUE,
   beer_style  text,
   mash_time  integer,
   mash_temp integer,
   IBU real,
   abv  real,
   grav_og  real,
   grav_fn  real,
   picture_id  text
);

CREATE TABLE  brew_session  (
   id  integer PRIMARY KEY,
   recipe_id  integer,
   beer_style  text,
   mash_time  integer,
   mash_temp integer,
   IBU real,
   abv  real,
   grav_og  real,
   grav_fn  real,
   brew_date  integer,
   rating  real,
   picture_id  text,
   FOREIGN KEY (recipe_id) REFERENCES recipe (id)
    ON DELETE CASCADE
);

CREATE TABLE  grain  (
   id  integer PRIMARY KEY,
   recipe_id  integer,
   session_id integer,
   grain_name  text NOT NULL,
   quantity  real NOT NULL,
   FOREIGN KEY (recipe_id) REFERENCES recipe (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
   FOREIGN KEY (session_id) REFERENCES brew_session (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE  hop  (
   id  integer PRIMARY KEY,
   recipe_id  integer,
   session_id integer,
   hop_name  text NOT NULL,
   quantity  real NOT NULL,
   use_type  text NOT NULL,
   use_time  integer NOT NULL,
   FOREIGN KEY (recipe_id) REFERENCES recipe (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
   FOREIGN KEY (session_id) REFERENCES brew_session (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE  yeast  (
   id  integer PRIMARY KEY,
   recipe_id  integer,
   session_id integer,
   yeast_name  text NOT NULL,
   FOREIGN KEY (recipe_id) REFERENCES recipe (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
   FOREIGN KEY (session_id) REFERENCES brew_session (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE  other_ingredient  (
   id  integer PRIMARY KEY,
   recipe_id  integer,
   session_id integer,
   ing_name  text NOT NULL,
   quantity  real NOT NULL,
   details  text,
   FOREIGN KEY (recipe_id) REFERENCES recipe (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
   FOREIGN KEY (session_id) REFERENCES brew_session (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE  note  (
   id  integer PRIMARY KEY,
   recipe_id  integer,
   session_id integer,
   note text, 
   FOREIGN KEY (recipe_id) REFERENCES recipe (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
   FOREIGN KEY (session_id) REFERENCES brew_session (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

