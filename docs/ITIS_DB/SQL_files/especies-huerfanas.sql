SELECT 
--count(*)
s.tsn, s.complete_name, s.rank_id srank, t1.rank_id rank1, t2.rank_id rank2, t3.rank_id rank3, t4.rank_id rank4, t5.rank_id rank5, t6.rank_id rank6
FROM cmispecies s
LEFT JOIN taxonomic_units t1 ON s.parent_tsn = t1.tsn
LEFT JOIN taxonomic_units t2 ON t1.parent_tsn = t2.tsn
LEFT JOIN taxonomic_units t3 ON t2.parent_tsn = t3.tsn
LEFT JOIN taxonomic_units t4 ON t3.parent_tsn = t4.tsn
LEFT JOIN taxonomic_units t5 ON t4.parent_tsn = t5.tsn
LEFT JOIN taxonomic_units t6 ON t5.parent_tsn = t6.tsn
LEFT JOIN taxonomic_units t7 ON t6.parent_tsn = t7.tsn
LEFT JOIN taxonomic_units t8 ON t7.parent_tsn = t8.tsn
LEFT JOIN taxonomic_units t9 ON t8.parent_tsn = t9.tsn
LEFT JOIN taxonomic_units t10 ON t9.parent_tsn = t10.tsn
LEFT JOIN taxonomic_units t11 ON t10.parent_tsn = t11.tsn
LEFT JOIN taxonomic_units t12 ON t11.parent_tsn = t12.tsn
LEFT JOIN taxonomic_units t13 ON t12.parent_tsn = t13.tsn
WHERE ( t1.rank_id <> 140 AND t2.rank_id <> 140 
AND t3.rank_id <> 140 AND t4.rank_id <> 140 AND t5.rank_id <> 140
AND t6.rank_id <> 140 
AND t7.rank_id <> 140
AND t8.rank_id <> 140
AND t9.rank_id <> 140
AND t10.rank_id <> 140
AND t11.rank_id <> 140
AND t12.rank_id <> 140
AND t13.rank_id <> 140
) LIMIT 10;


SELECT 
count(*)
-- s.tsn, s.complete_name, s.rank_id srank, t1.rank_id rank1, t2.rank_id rank2, t3.rank_id rank3, t4.rank_id rank4, t5.rank_id rank5, t6.rank_id rank6
FROM cmispecies s
LEFT JOIN taxonomic_units t1 ON s.parent_tsn = t1.tsn
LEFT JOIN taxonomic_units t2 ON t1.parent_tsn = t2.tsn
LEFT JOIN taxonomic_units t3 ON t2.parent_tsn = t3.tsn
LEFT JOIN taxonomic_units t4 ON t3.parent_tsn = t4.tsn
LEFT JOIN taxonomic_units t5 ON t4.parent_tsn = t5.tsn
LEFT JOIN taxonomic_units t6 ON t5.parent_tsn = t6.tsn
LEFT JOIN taxonomic_units t7 ON t6.parent_tsn = t7.tsn
LEFT JOIN taxonomic_units t8 ON t7.parent_tsn = t8.tsn
LEFT JOIN taxonomic_units t9 ON t8.parent_tsn = t9.tsn
LEFT JOIN taxonomic_units t10 ON t9.parent_tsn = t10.tsn
LEFT JOIN taxonomic_units t11 ON t10.parent_tsn = t11.tsn
LEFT JOIN taxonomic_units t12 ON t11.parent_tsn = t12.tsn
LEFT JOIN taxonomic_units t13 ON t12.parent_tsn = t13.tsn
WHERE ( t1.rank_id <> 140 AND t2.rank_id <> 140 
AND t3.rank_id <> 140 AND t4.rank_id <> 140 AND t5.rank_id <> 140
AND t6.rank_id <> 140 
AND t7.rank_id <> 140
AND t8.rank_id <> 140
AND t9.rank_id <> 140
AND t10.rank_id <> 140
AND t11.rank_id <> 140
AND t12.rank_id <> 140
AND t13.rank_id <> 140
);