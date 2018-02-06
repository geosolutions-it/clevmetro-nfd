CREATE TABLE cmifamilies AS (

SELECT 
s.tsn AS species_tsn, t7.tsn AS family_tsn
FROM cmispecies s
LEFT JOIN taxonomic_units t1 ON s.parent_tsn = t1.tsn
LEFT JOIN taxonomic_units t2 ON t1.parent_tsn = t2.tsn
LEFT JOIN taxonomic_units t3 ON t2.parent_tsn = t3.tsn
LEFT JOIN taxonomic_units t4 ON t3.parent_tsn = t4.tsn
LEFT JOIN taxonomic_units t5 ON t4.parent_tsn = t5.tsn
LEFT JOIN taxonomic_units t6 ON t5.parent_tsn = t6.tsn
LEFT JOIN taxonomic_units t7 ON t6.parent_tsn = t7.tsn
WHERE ( 
t7.rank_id = 140
)
UNION

SELECT 
s.tsn AS species_tsn, t6.tsn AS family_tsn
FROM cmispecies s
LEFT JOIN taxonomic_units t1 ON s.parent_tsn = t1.tsn
LEFT JOIN taxonomic_units t2 ON t1.parent_tsn = t2.tsn
LEFT JOIN taxonomic_units t3 ON t2.parent_tsn = t3.tsn
LEFT JOIN taxonomic_units t4 ON t3.parent_tsn = t4.tsn
LEFT JOIN taxonomic_units t5 ON t4.parent_tsn = t5.tsn
LEFT JOIN taxonomic_units t6 ON t5.parent_tsn = t6.tsn
WHERE ( 
t6.rank_id = 140
)

UNION

SELECT 
s.tsn AS species_tsn, t5.tsn AS family_tsn
FROM cmispecies s
LEFT JOIN taxonomic_units t1 ON s.parent_tsn = t1.tsn
LEFT JOIN taxonomic_units t2 ON t1.parent_tsn = t2.tsn
LEFT JOIN taxonomic_units t3 ON t2.parent_tsn = t3.tsn
LEFT JOIN taxonomic_units t4 ON t3.parent_tsn = t4.tsn
LEFT JOIN taxonomic_units t5 ON t4.parent_tsn = t5.tsn
WHERE ( 
t5.rank_id = 140
)

UNION

SELECT 
s.tsn AS species_tsn, t4.tsn AS family_tsn
FROM cmispecies s
LEFT JOIN taxonomic_units t1 ON s.parent_tsn = t1.tsn
LEFT JOIN taxonomic_units t2 ON t1.parent_tsn = t2.tsn
LEFT JOIN taxonomic_units t3 ON t2.parent_tsn = t3.tsn
LEFT JOIN taxonomic_units t4 ON t3.parent_tsn = t4.tsn
WHERE ( 
t4.rank_id = 140
)

UNION

SELECT 
s.tsn AS species_tsn, t3.tsn AS family_tsn
FROM cmispecies s
LEFT JOIN taxonomic_units t1 ON s.parent_tsn = t1.tsn
LEFT JOIN taxonomic_units t2 ON t1.parent_tsn = t2.tsn
LEFT JOIN taxonomic_units t3 ON t2.parent_tsn = t3.tsn
WHERE ( 
t3.rank_id = 140
)

UNION

SELECT 
s.tsn AS species_tsn, t2.tsn AS family_tsn
FROM cmispecies s
LEFT JOIN taxonomic_units t1 ON s.parent_tsn = t1.tsn
LEFT JOIN taxonomic_units t2 ON t1.parent_tsn = t2.tsn
WHERE ( 
t2.rank_id = 140
)


UNION

SELECT 
s.tsn AS species_tsn, t1.tsn AS family_tsn
FROM cmispecies s
LEFT JOIN taxonomic_units t1 ON s.parent_tsn = t1.tsn
WHERE ( 
t1.rank_id = 140
)

);