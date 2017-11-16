SELECT * from taxonomic_units u
  JOIN vernaculars v ON  u.tsn = v.tsn
WHERE
  u.tsn = 173769
  and
  (language = 'English'
  OR language = 'Spanish')