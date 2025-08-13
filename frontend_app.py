from bottle import Bottle, run, SimpleTemplate
import psycopg2
from create_envs import import_envs_and_create_db_config
# Ensure there is no local file named 'bottle.py' in this directory or PYTHONPATH

app = Bottle()

DB_CONFIG = import_envs_and_create_db_config()



def get_last_20_records():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('SELECT name, date FROM data ORDER BY id DESC LIMIT 20')
        rows = cur.fetchall()
    except Exception as e:
        print(f"Error fetching records: {e}")
        rows = []
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
    return rows

@app.route('/')
def index():
    records = get_last_20_records()
    tpl = '''
        <h2 style="text-align:center;">Last 20 Records</h2>
        <div style="display: flex; justify-content: center;">
            <table border="1">
                <tr><th>Name</th><th>Data</th></tr>
                % for name, date in records:
                    <tr><td>{{name}}</td><td>{{date}}</td></tr>
                % end
            </table>
        </div>
    '''
    return SimpleTemplate(tpl).render(records=records)

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)