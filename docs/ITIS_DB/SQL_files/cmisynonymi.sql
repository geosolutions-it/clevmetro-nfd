CREATE TABLE cmisynonymi AS (

SELECT 
s.tsn AS species_tsn, syn.tsn AS synonym_tsn
FROM cmispecies s
LEFT JOIN synonym_links syn ON s.tsn = syn.tsn_accepted

);