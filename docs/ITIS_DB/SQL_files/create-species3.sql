CREATE TABLE cmispecies3 AS (
 SELECT s.tsn, s.complete_name AS name_sci, s.rank_id, 
 s.vern1 AS first_common, s.vern2 AS second_common, s.vern3 AS third_common,
 f.family_tsn AS family_tsn,
 p.phylum_tsn AS phylum_tsn,
 syn.tsn AS synonym_tsn,
 tu.kingdom_id 
 FROM  cmispecies s
 LEFT JOIN cmifamilies f ON s.tsn = f.species_tsn
 LEFT JOIN cmiphylums p ON s.tsn = p.species_tsn
 LEFT JOIN synonym_links syn ON s.tsn = syn.tsn_accepted
 JOIN taxonomic_units tu ON s.tsn = tu.tsn
);

-- select distinct(name_sci), rank_id, first_common, second_common, third_common, family_tsn, phylum_tsn, synonym_tsn, kingdom_id FROM cmispecies3 WHERE family_tsn is not NULL and phylum_tsn is not NULL

