from cs50 import SQL
from datetime import datetime
import pytz

# create a database object to connect to our db
db = SQL("sqlite:///signinout.db")

def get_today():
  # set the timezone to our timezone
  indytz = pytz.timezone("America/Indiana/Indianapolis")
  today = datetime.now(indytz) #get the current date and time
  cur_date = today.strftime("%m-%d-%Y") #date format 04-12-2023
  cur_time = today.strftime("%-I:%M %p") #time format 3:05 PM
  #return a dict with the current date and time
  return {'c_date':cur_date,'c_time':cur_time}


# this function will get all the passes from the database
def get_all_passes():
  sql = """
  SELECT *
    FROM passes
    ORDER BY pass_date DESC, out_time DESC
  """
  results = db.execute(sql)
  return results

# get just the passes for today
def get_todays_passes(today):
  sql = "SELECT * FROM passes WHERE pass_date = ?"
  return db.execute(sql, today)

def get_summary():
  sql = """SELECT COUNT(id) as total, f_name, l_name, student_id
  FROM passes
  GROUP BY student_id ORDER BY total DESC"""
  return db.execute(sql)
  
def get_stu_summary(stu_id):
  sql = """SELECT COUNT(id) as total, location, student_id
  FROM passes
  WHERE student_id = ?
  GROUP BY location ORDER BY total DESC"""
  return db.execute(sql, stu_id)

# this function will get the name of the student
def get_student_name(stu_id):
  sql = "SELECT f_name, l_name FROM passes WHERE student_id = ?"
  results = db.execute(sql, stu_id)[0]
  #[0] will get the first row in the list of rows
  first = results.get('f_name')
  last = results.get('l_name')
  return f"{first} {last}"
  
def get_stu_loc_summary(stu_id, loc):
  sql = """SELECT id, pass_date, out_time, in_time FROM passes
  WHERE student_id = ? AND location = ?
  ORDER BY pass_date DESC, out_time DESC"""
  return db.execute(sql, stu_id, loc)
  




  