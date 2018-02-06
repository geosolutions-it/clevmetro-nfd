CREATE EXTENSION tablefunc;

SELECT t.* FROM crosstab(
   'SELECT tsn, complete_name, rank_id, parent_tsn, rn, vernacular_name
     FROM  (
        SELECT u.tsn, u.complete_name, u.rank_id, u.parent_tsn, v.vernacular_name,
        row_number() OVER (PARTITION BY u.tsn
                            ORDER BY vern_id ASC NULLS LAST) AS rn
        FROM taxonomic_units u JOIN vernaculars v ON u.tsn = v.tsn
        WHERE  (v.language = ''English'' or v.language = ''unspecified'')
        AND u.rank_id >= 220 AND u.rank_id <= 230 AND 
        (name_usage = ''valid'' OR name_usage = ''accepted'')
        ) sub
     WHERE  rn < 4
     ORDER  BY tsn
   ', 'VALUES (1),(2),(3)'
   ) AS t (tsn int, complete_name text, rank_id int, parent_tsn int, vern1 text, vern2 text, vern3 text)
  