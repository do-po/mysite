log_in_query = '''
    select
    *
    from
    `user`
    where
    `id` = %s
    and
    `password` = %s
'''

check_id_query = """
    select
    *
    from
    `user`
    where
    id = %s
"""

sign_up_query = """
    insert
    into
    `user`
    values (%s, %s, %s)
"""