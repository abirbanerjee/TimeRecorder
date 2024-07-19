import sqlite3
import inquirer
from datetime import datetime
con = sqlite3.connect('projects.db')
cur = con.cursor()

# cur.execute('Create table projects(name text, project_name text, internal boolean)')

# cur.execute("insert into projects VALUES(?,?,?)", ['Agrana', 'NPDDashboard', False])

# cur.execute('Create table recordings(project_id number, date date, hours number)')
# con.commit()

def insert_time_recording( project_id, date, hours):
    cur.execute('insert into recordings values(?,?,?)', [project_id, date, hours])
    con.commit()

# insert_time_recording(1, '2024-07-01', 2)
def get_all_projects():
    header = []
    columns = []
    result = cur.execute('SELECT rowid,name,project_name FROM projects')
    data = result.fetchall()

    for row in data:
        columns.append(row)
    return columns


def prompt_projects():
    columns = get_all_projects()
    project = [     
    inquirer.List('project',
                    message="Select project",
                    choices=columns,
                ),
    ]
    answers = inquirer.prompt(project)
    print(answers)
    return answers['project'][0]
def prompt_date_hours():
    date = [
            inquirer.Text('date', 'Enter date', default=datetime.today().strftime('%Y-%m-%d')),
            inquirer.Text('hours', 'Enter hours', default=8),
        ]
    date_hours = inquirer.prompt(date)
    return date_hours

def get_hours_for_project():
    project = prompt_projects()
    result = cur.execute(f"select hours from recordings where project_id = {project}")
    data = result.fetchall()
    tothours = 0
    for row in data:
        tothours += row[0]
    print (tothours)
def record_time():
    project = prompt_projects()
    date_hours = prompt_date_hours()
    insert_time_recording(project, date_hours['date'], date_hours['hours'])

def start():
    prmpt = [
        # inquirer.List('choice', message = 'Select an option', choices = [ (1, 'Record Time'), (2, 'Get total hours') ] ),
        inquirer.List("choice", message="Select an option", choices=[ ( 'Record Time', '1'), ('Get total hours', 2) ]),
    ]
    choice = inquirer.prompt(prmpt)
    if(choice['choice'] == 1):
        record_time()
    else:
        get_hours_for_project()
# get_hours_for_project()
start()