from re import findall


def extract_col_from_query_string(query):
    if query is isinstance(query, str):
        return []
    return list(
        set(
            map(
                lambda col: col.replace("`", ""),
                findall(r"\`.*?\`", query),
            ),
        )
    )
