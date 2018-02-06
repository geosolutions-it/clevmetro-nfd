SELECT * FROM taxonomic_units u
JOIN vernaculars v ON  u.tsn = v.tsn
WHERE
(language = 'English'
OR language = 'Spanish')
AND complete_name LIKE '%Chrysemys%'

 LIMIT 1000