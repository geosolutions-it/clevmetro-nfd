CREATE TABLE cmifamilies2 AS (

SELECT t.* FROM crosstab(
   'SELECT tsn, complete_name, rank_id, parent_tsn, kingdom_id, rn, vernacular_name
     FROM  (
        SELECT u.tsn, u.complete_name, u.rank_id, u.parent_tsn, u.kingdom_id, v.vernacular_name,
        row_number() OVER (PARTITION BY u.tsn
                            ORDER BY vern_id ASC NULLS LAST) AS rn
        FROM (SELECT family_tsn FROM cmifamilies GROUP BY family_tsn) f JOIN taxonomic_units u ON f.family_tsn = u.tsn JOIN vernaculars v ON u.tsn = v.tsn
        WHERE  (v.language = ''English'' or v.language = ''unspecified'')
        AND
        (name_usage = ''valid'' OR name_usage = ''accepted'')
        ) sub
     WHERE  rn < 4
     ORDER  BY tsn
   ', 'VALUES (1),(2),(3)'
   ) AS t (tsn int, name_sci text, rank_id int, parent_tsn int, kingdom_id int, first_common text, second_common text, third_common text)

);