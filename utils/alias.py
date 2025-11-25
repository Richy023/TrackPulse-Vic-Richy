import sqlite3

def setWebAlias(userid, alias):
    conn = sqlite3.connect('userdata/aliases.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aliases (
        userid INTEGER PRIMARY KEY,
        alias TEXT UNIQUE
    )''')
    
    # Check if alias is already taken by a different user
    cursor.execute('''
    SELECT userid FROM aliases WHERE alias = ? AND userid != ?
    ''', (alias, userid))
    if cursor.fetchone():
        conn.close()
        return False
    
    cursor.execute('''
    INSERT OR REPLACE INTO aliases (userid, alias)
    VALUES (?, ?)
    ''', (userid, alias))
    
    conn.commit()
    conn.close()
    return True