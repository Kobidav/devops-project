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
        <!DOCTYPE html>
        <html lang="en">
        <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Last 20 Records</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
                <body class="bg-light">
                    <div class="container py-5">
                    <div class="row justify-content-center">
                        <div class="col-md-8">
                        <div class="card shadow">
                            <div class="card-header bg-primary text-white text-center">
                            <h2 class="mb-0">Last 20 Records</h2>
                            </div>
                            <div class="card-body">
                            <table class="table table-striped table-hover align-middle">
                                <thead class="table-dark">
                                <tr>
                                    <th>Name</th>
                                    <th>Date</th>
                                </tr>
                                </thead>
                                <tbody>
                                % for name, date in records:
                                <tr>
                                    <td>{{name}}</td>
                                    <td>{{date}}</td>
                                </tr>
                                % end
                                </tbody>
                            </table>
                            </div>
                        </div>
                        </div>
                    </div>
                    </div>
                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
                </body>
                </html>
                '''
    return SimpleTemplate(tpl).render(records=records)

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)
