CREATE TABLE cmispecies2 AS (
 SELECT s.tsn, s.complete_name AS name_sci, s.rank_id, ''::text AS synonym, 
 s.vern1 AS first_common, s.vern2 AS second_common, s.vern3 AS third_common, f.family_tsn AS family_tsn,
 tu.kingdom_id 
 FROM  cmispecies s JOIN cmifamilies f ON s.tsn = f.species_tsn JOIN taxonomic_units tu ON s.tsn = tu.tsn
);

