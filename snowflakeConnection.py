from snowflake import connector


def sfconnect():
    cnx = connector.connect(
        account='uq97939.us-central1.gcp',
        user='parham',
        password='Snow2021',
        warehouse='COMPUTE_WH',
        database='DEMO_DB',
        schema='PUBLIC',
        role='SYSADMIN'
    )
    return cnx


