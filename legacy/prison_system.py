import sqlite3

# ------------------------------------------------------------
# LEGACY VERSION - Prison Management System
# Intentional code smells:
#  - One God class doing everything (data, business logic, DB, UI)
#  - Hardcoded values / magic numbers
#  - Duplicated code (insert/print logic repeated)
#  - Long methods
#  - No separation of concerns
#  - Mixed responsibilities (DB + validation + display in same method)
# ------------------------------------------------------------

class PrisonSystem:
    def __init__(self):
        self.conn = sqlite3.connect("prison.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS inmates (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                age INTEGER,
                                crime TEXT,
                                cell_no INTEGER,
                                sentence_years INTEGER)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS staff (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                role TEXT,
                                salary INTEGER)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS visitors (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                inmate_id INTEGER,
                                date TEXT)""")
        self.conn.commit()

    def add_inmate(self, name, age, crime, cell_no, sentence_years):
        # magic numbers everywhere
        if age < 18:
            print("Cannot add inmate, must be 18 or older")
            return
        if cell_no < 1 or cell_no > 50:
            print("Invalid cell number, must be between 1 and 50")
            return
        if sentence_years < 0 or sentence_years > 100:
            print("Invalid sentence")
            return

        self.cur.execute("INSERT INTO inmates (name, age, crime, cell_no, sentence_years) VALUES (?,?,?,?,?)",
                          (name, age, crime, cell_no, sentence_years))
        self.conn.commit()
        print("Inmate added: " + name + ", Age: " + str(age) + ", Crime: " + crime +
              ", Cell: " + str(cell_no) + ", Sentence: " + str(sentence_years) + " years")

    def add_staff(self, name, role, salary):
        if salary < 10000:
            print("Salary too low")
            return
        if role != "Guard" and role != "Warden" and role != "Doctor" and role != "Cook":
            print("Invalid role")
            return

        self.cur.execute("INSERT INTO staff (name, role, salary) VALUES (?,?,?)", (name, role, salary))
        self.conn.commit()
        print("Staff added: " + name + ", Role: " + role + ", Salary: " + str(salary))

    def add_visitor(self, name, inmate_id, date):
        # duplicated lookup code (also appears in get_inmate_info)
        self.cur.execute("SELECT * FROM inmates WHERE id=?", (inmate_id,))
        inmate = self.cur.fetchone()
        if inmate is None:
            print("Inmate not found")
            return

        self.cur.execute("INSERT INTO visitors (name, inmate_id, date) VALUES (?,?,?)", (name, inmate_id, date))
        self.conn.commit()
        print("Visitor " + name + " logged for inmate " + inmate[1] + " on " + date)

    def get_inmate_info(self, inmate_id):
        # duplicated lookup code (also appears in add_visitor)
        self.cur.execute("SELECT * FROM inmates WHERE id=?", (inmate_id,))
        inmate = self.cur.fetchone()
        if inmate is None:
            print("Inmate not found")
            return

        print("ID: " + str(inmate[0]))
        print("Name: " + inmate[1])
        print("Age: " + str(inmate[2]))
        print("Crime: " + inmate[3])
        print("Cell: " + str(inmate[4]))
        print("Sentence: " + str(inmate[5]) + " years")

        # business logic mixed with display logic
        if inmate[5] > 10:
            print("Status: High-risk prisoner")
        elif inmate[5] > 5:
            print("Status: Medium-risk prisoner")
        else:
            print("Status: Low-risk prisoner")

    def list_all_inmates(self):
        self.cur.execute("SELECT * FROM inmates")
        rows = self.cur.fetchall()
        for r in rows:
            print("ID: " + str(r[0]) + ", Name: " + r[1] + ", Age: " + str(r[2]) +
                  ", Crime: " + r[3] + ", Cell: " + str(r[4]) + ", Sentence: " + str(r[5]))

    def list_all_staff(self):
        self.cur.execute("SELECT * FROM staff")
        rows = self.cur.fetchall()
        for r in rows:
            print("ID: " + str(r[0]) + ", Name: " + r[1] + ", Role: " + r[2] + ", Salary: " + str(r[3]))

    def calculate_release_year(self, inmate_id, current_year):
        self.cur.execute("SELECT sentence_years FROM inmates WHERE id=?", (inmate_id,))
        row = self.cur.fetchone()
        if row is None:
            print("Inmate not found")
            return None
        release = current_year + row[0]
        print("Release year: " + str(release))
        return release

    def close(self):
        self.conn.close()


# ------------------------------------------------------------
# Simple CLI menu (also tangled into the same file - bad design)
# ------------------------------------------------------------
def main():
    system = PrisonSystem()

    while True:
        print("\n--- Prison Management System (Legacy) ---")
        print("1. Add Inmate")
        print("2. Add Staff")
        print("3. Add Visitor")
        print("4. View Inmate Info")
        print("5. List All Inmates")
        print("6. List All Staff")
        print("7. Calculate Release Year")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Name: ")
            age = int(input("Age: "))
            crime = input("Crime: ")
            cell_no = int(input("Cell No: "))
            sentence = int(input("Sentence (years): "))
            system.add_inmate(name, age, crime, cell_no, sentence)
        elif choice == "2":
            name = input("Name: ")
            role = input("Role (Guard/Warden/Doctor/Cook): ")
            salary = int(input("Salary: "))
            system.add_staff(name, role, salary)
        elif choice == "3":
            name = input("Visitor Name: ")
            inmate_id = int(input("Inmate ID: "))
            date = input("Date (YYYY-MM-DD): ")
            system.add_visitor(name, inmate_id, date)
        elif choice == "4":
            inmate_id = int(input("Inmate ID: "))
            system.get_inmate_info(inmate_id)
        elif choice == "5":
            system.list_all_inmates()
        elif choice == "6":
            system.list_all_staff()
        elif choice == "7":
            inmate_id = int(input("Inmate ID: "))
            year = int(input("Current Year: "))
            system.calculate_release_year(inmate_id, year)
        elif choice == "8":
            system.close()
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
