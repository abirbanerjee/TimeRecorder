import sqlite3
import inquirer
from datetime import datetime
from calendar import monthrange

con = sqlite3.connect("projects.db")
cur = con.cursor()

# cur.execute('Create table projects(name text, project_name text, internal boolean)')

# cur.execute("insert into projects VALUES(?,?,?)", ['Agrana', 'NPDDashboard', False])

# cur.execute('Create table recordings(project_id number, date date, hours number)')
# con.commit()


def insert_time_recording(project_id, date, hours):
    cur.execute("insert into recordings values(?,?,?)", [project_id, date, hours])
    con.commit()


# insert_time_recording(1, '2024-07-01', 2)
def get_all_projects():
    header = []
    columns = []
    result = cur.execute("SELECT rowid,name,project_name FROM projects")
    data = result.fetchall()

    for row in data:
        columns.append(row)
    return columns

def add_new_project(company, project_name, internal_flag):
    cur.execute("insert into projects values(?,?,?)", [company, project_name, internal_flag])
    con.commit()

def prompt_projects():
    columns = get_all_projects()
    project = [
        inquirer.List(
            "project",
            message="Select project",
            choices=columns,
        ),
    ]
    answers = inquirer.prompt(project)
    return answers["project"][0]


def prompt_date_hours():
    date = [
        inquirer.Text(
            "date", "Enter date", default=datetime.today().strftime("%Y-%m-%d")
        ),
        inquirer.Text("hours", "Enter hours", default=8),
    ]
    date_hours = inquirer.prompt(date)
    return date_hours


def get_hours_for_project(month, year):
    daysofmonth = monthrange(int(year), int(month))
    project = prompt_projects()
    result = cur.execute(
        f"select hours from recordings where project_id = {project} and date >='{year}-{month}-01' and date <= '{year}-{month}-{daysofmonth[1]}'"
    )
    data = result.fetchall()
    tothours = 0
    for row in data:
        tothours += row[0]
    print(tothours)


def monthly_report(month, year):
    daysofmonth = monthrange(int(year), int(month))
    all_projects = get_all_projects()
    project_ids = []
    project_names = []
    projectwise_report =[]
    dict = {}
    projectwise_report_dict = {}
    for row in all_projects:
        project_ids.append(row[0])
        project_names.append(row[1])
        dict[row[1]] = 0
        projectwise_report.append(f"{row[1]} - {row[2]}")
        projectwise_report_dict[f"{row[1]} - {row[2]}"] = 0
    for idx, project in enumerate(project_ids):
        result = cur.execute(
            f"select hours,project_id from recordings where project_id = '{project}' and date >='{year}-{month}-01' and date <= '{year}-{month}-{daysofmonth[1]}'"
        )
        data = result.fetchall()
        if len(data) > 0:
            print(data)
            for hrs in data:
                dict[project_names[idx]] += hrs[0]
                project_select = cur.execute(f"select name, project_name from projects where rowid = {hrs[1]}")
                project_details = project_select.fetchall()
                print(project_details)
                if(len(project_details)!=0):
                    print(f"{project_details[0][0]} - {project_details[0][1]}")
                    projectwise_report_dict[f"{project_details[0][0]} - {project_details[0][1]}"] += hrs[0]
    print(dict)
    print(projectwise_report_dict)

def record_time():
    project = prompt_projects()
    date_hours = prompt_date_hours()
    insert_time_recording(project, date_hours["date"], date_hours["hours"])


def get_month_year():
    prmpt = [
        inquirer.Text("month", "Enter month", default=datetime.today().strftime("%m")),
        inquirer.Text("year", "Enter year", default=datetime.today().strftime("%Y")),
    ]
    month_year = inquirer.prompt(prmpt)
    return month_year

def prompt_new_project():
    prmpt = [
        inquirer.Text("company", "Enter company name"),
        inquirer.Text("project", "Enter project name"),
        inquirer.Text("internal", "Gramont internal?", default='N'),
    ]
    project_info = inquirer.prompt(prmpt)
    return project_info

def start():
    while True:
        prmpt = [
            # inquirer.List('choice', message = 'Select an option', choices = [ (1, 'Record Time'), (2, 'Get total hours') ] ),
            inquirer.List(
                "choice",
                message="Select an option",
                choices=[
                    ("Record Time", 1),
                    ("Get total hours", 2),
                    ("Get monthly report", 3),
                    ("Add a new project", 4),
                    ("Exit", 5),
                ],
                carousel= True
            ),
        ]
        choice = inquirer.prompt(prmpt)
        match choice["choice"]:
            case 1:
                record_time()
            case 2:
                month_year = get_month_year()
                get_hours_for_project(month_year["month"], month_year["year"])
            case 3:
                month_year = get_month_year()
                monthly_report(month_year["month"], month_year["year"])
            case 4:
                project_details = prompt_new_project()
                if project_details['internal'] == 'Y':
                    internal_flag = True
                else:
                    internal_flag = False
                add_new_project(project_details['company'], project_details['project'], internal_flag)
            case 5:
                exit()


start()
