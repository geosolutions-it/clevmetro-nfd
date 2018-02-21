"""Utilities for contacting with the ITIS species database"""

from collections import namedtuple

from django.db import connections


def search_taxon(search_string, kingdoms, page_size=100, page=0):
    """Search existent taxa

    Parameters
    ----------
    search_string: str
        Part of the name of the taxon to search for
    kingdoms: list
        An iterable with the names of the kingdoms where the search is to be
        performed

    Returns
    -------

    """
    size = (
        page_size.upper() if isinstance(page_size, basestring) else page_size)
    offset = page * size if size != "ALL" else 0

    query = """
        SELECT 
            u.tsn AS tsn, 
            u.complete_name AS name, 
            t.rank_name AS rank, 
            json_agg(json_build_array(v.language, v.vernacular_name)) AS common_names
        FROM taxonomic_units AS u 
            INNER JOIN kingdoms AS k ON u.kingdom_id = k.kingdom_id 
            INNER JOIN taxon_unit_types AS t ON u.rank_id = t.rank_id
                AND u.kingdom_id = t.kingdom_id
            LEFT OUTER JOIN vernaculars AS v ON u.tsn = v.tsn
        WHERE k.kingdom_name = ANY(%(kingdoms)s)
            AND (
            u.complete_name ILIKE %(search_string)s
                OR v.vernacular_name ILIKE %(search_string)s
            )
        GROUP BY u.tsn, t.rank_name
        ORDER BY u.rank_id 
        LIMIT {size}
        OFFSET {offset}
    """.format(size=size, offset=offset)
    with connections["itis"].cursor() as cursor:
        cursor.execute(query, {
            "kingdoms": [kingdom.capitalize() for kingdom in kingdoms],
            "search_string": "%{}%".format(search_string),
        })
        return list(
            _gen_strip_rows(
                cursor,
                fix_common_names=True,
                group_common_names_by_language=False
            )
        )



# a tsn that has no vernaculars: 107045
# a tsn that has vernaculars: 17025
def get_taxon_upper_ranks(tsn):
    query = """
        SELECT
          u.tsn AS tsn, 
          u.complete_name AS name, 
          t.rank_name AS rank, 
          json_agg(json_build_array(v.language, v.vernacular_name)) AS common_names
        FROM taxonomic_units AS u
          LEFT OUTER JOIN vernaculars AS v ON u.tsn = v.tsn
          INNER JOIN taxon_unit_types AS t ON u.rank_id = t.rank_id 
              AND u.kingdom_id = t.kingdom_id
        WHERE u.tsn IN (
            SELECT CAST(unnest(string_to_array(hierarchy_string, '-')) AS integer)
            FROM hierarchy AS h
            WHERE h.tsn = %(tsn)s
        )
        GROUP BY u.tsn, t.rank_name
        ORDER BY u.rank_id;
    """
    with connections["itis"].cursor() as cursor:
        cursor.execute(query, {"tsn": tsn})
        return list(_gen_strip_rows(cursor, fix_common_names=True))


def get_taxon_details(tsn):
    query = """
        SELECT 
            u.tsn AS tsn, 
            u.complete_name AS name, 
            t.rank_name AS rank, 
            json_agg(json_build_array(v.language, v.vernacular_name)) AS common_names
        FROM taxonomic_units AS u 
          LEFT OUTER JOIN vernaculars as v ON u.tsn = v.tsn 
          INNER JOIN taxon_unit_types AS t ON u.rank_id = t.rank_id 
            AND u.kingdom_id = t.kingdom_id
        WHERE u.tsn = %(tsn)s
        GROUP BY u.tsn, t.rank_name
    """
    with connections["itis"].cursor() as cursor:
        cursor.execute(query, {"tsn": int(tsn)})
        row = cursor.fetchone()
        if row is not None:
            stripped = [
                c.strip() if isinstance(c, basestring) else c for c in row]
            fixed_names = _fix_common_names(stripped)
            ResultTuple = namedtuple(
                "Result", [col[0] for col in cursor.description])
            result = ResultTuple(*fixed_names)
        else:
            result = None
        return result


def _gen_strip_rows(cursor, fix_common_names=False,
                    group_common_names_by_language=True):
    Result = namedtuple("Result", [col[0] for col in cursor.description])
    for row in cursor.fetchall():
        stripped = [c.strip() if isinstance(c, basestring) else c for c in row]
        if fix_common_names:
            fixed = _fix_common_names(
                stripped,
                group_by_language=group_common_names_by_language
            )
        else:
            fixed = stripped
        yield Result(*fixed)


def _group_common_names_by_language(common_names):
    available_languages = set(i[0] for i in common_names)
    fixed_names = {}
    for lang in available_languages:
        fixed_names[lang] = [i[1] for i in common_names if i[0] == lang]
    return fixed_names


def _fix_common_names(raw_result, group_by_language=False):
    common_names = raw_result[-1]
    any_names = any(common_names[0])
    if any_names:
        if group_by_language:
            fixed_names = _group_common_names_by_language(common_names)
        else:
            fixed_names = [i[-1] for i in common_names]
    else:
        fixed_names = None
    return raw_result[:-1] + [fixed_names]
