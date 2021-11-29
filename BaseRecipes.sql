INSERT INTO recipe (recipe_name, beer_style, mash_time, mash_temp, IBU, abv, grav_og, grav_fn)
VALUES 
    ('Perfect NEIPA', 'NEIPA', 60, 152, 59.3, 6.5 ,1.062, 1.013),
    ('Sierra Nevada Pale Ale', 'American Pale Ale', 60, 153, 39.8, 5.6, 1.055, 1.013);

INSERT INTO grain (recipe_id, grain_name, quantity)
VALUES
    (1, 'Pale 2-Row', 4.9),
    (1, 'Wheat', 0.63),
    (1, 'Flaked Oats', 0.63),
    (1, 'Honey Malt', 0.2),
    (2, 'Pale 2-Row', 5.2),
    (2, 'Caramel/Crystal 60L', 0.4);

INSERT INTO hop (recipe_id, hop_name, quantity, use_type, use_time)
VALUES
    (1, 'Citra', 1, 'Boil', 10),
    (1, 'Galaxy', 1, 'Boil', 10),
    (1, 'Citra', 1.5, 'Whirlpool', 15),
    (1, 'Galaxy', 1.5, 'Whirlpool', 15),
    (1, 'Mosaic', 1.5, 'Whirlpool', 15),
    (1, 'Citra', 1, 'Dry Hop', 7),
    (1, 'Galaxy', 1.5, 'Dry Hop', 7),
    (1, 'Mosaic', 1, 'Dry Hop', 7),
    (1, 'Citra', 1.25, 'Dry Hop', 3),
    (1, 'Galaxy', 1.5, 'Dry Hop', 3),
    (1, 'Mosaic', 1, 'Dry Hop', 3),
    (2, 'Magnum', 0.5, 'Boil', 60),
    (2, 'Perle', 0.5, 'Boil', 30),
    (2, 'Cascade', 1, 'Boil', 10),
    (2, 'Cascade', 2, 'Boil', 0),
    (2, 'Cascade', 2, 'Dry Hop', 4);

INSERT INTO yeast (recipe_id, yeast_name)
VALUES
    (1, 'Wyeast - London Ale III 1318'),
    (2, 'Safale - American Ale Yeast US-05');


