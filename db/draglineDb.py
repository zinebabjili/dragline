import sqlite3

from models.conducteur import Conducteur

conn = sqlite3.connect('dragline.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS conducteurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            first text,
            last text,
            password text,
            poste integer
            )""")
conn.commit()

def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO conducteurs(first, last, password, poste) VALUES (?,?,?,?)",
                  (emp.first, emp.last, emp.password, emp.poste))
    conn.commit()


def get_emps_by_password(password):
    c.execute('SELECT * FROM conducteurs WHERE password = ?', (password,))
    return c.fetchone()



cond_1 = Conducteur('Ahmed', 'Tazi', 1234, 1)
cond_2 = Conducteur('younes', 'Taki', 5678, 2)
cond_3 = Conducteur('Anouar', 'Said', 9134, 3)



insert_emp(cond_1)
insert_emp(cond_2)
insert_emp(cond_3)


