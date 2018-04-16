#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

# the following list was obtained from ITIS DB with the query:
# SELECT DISTINCT rank_id, lower(rank_name)
# FROM taxon_unit_types
# ORDER BY rank_id
TAXON_RANKS = [
    "kingdom",
    "subkingdom",
    "infrakingdom",
    "superphylum",
    "superdivision",
    "division",
    "phylum",
    "subdivision",
    "subphylum",
    "infraphylum",
    "infradivision",
    "parvphylum",
    "parvdivision",
    "superclass",
    "class",
    "subclass",
    "infraclass",
    "superorder",
    "order",
    "suborder",
    "infraorder",
    "section",
    "subsection",
    "superfamily",
    "family",
    "subfamily",
    "tribe",
    "subtribe",
    "genus",
    "subgenus",
    "section",
    "subsection",
    "species",
    "subspecies",
    "variety",
    "form",
    "race",
    "subvariety",
    "stirp",
    "form",
    "morph",
    "aberration",
    "subform",
    "unspecified",
]
