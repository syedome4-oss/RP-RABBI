import streamlit as st
import sqlite3

# 🗄️ Connect to database
conn = sqlite3.connect("employees.db")
cur = conn.cursor()

# 📋 Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT,
    position TEXT,
    salary REAL,
    email TEXT
)
""")
conn.commit()

# 🎯 App Title
st.title("💼 Employee Management System")
st.caption("🏢 Manage employee records easily")

# 🧭 Navigation tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "➕ Add Employee",
    "📋 View Employees",
    "✏️ Update Employee",
    "🗑️ Delete Employee",
    "👤 About"
])

# ➕ CREATE
with tab1:
    st.subheader("➕ Add New Employee")

    name = st.text_input("👤 Employee Name")
    department = st.text_input("🏢 Department")
    position = st.text_input("💼 Job Position")
    salary = st.number_input("💰 Monthly Salary", min_value=0.0)
    email = st.text_input("📧 Email")

    if st.button("✅ Add Employee"):
        if name.strip() and department.strip() and position.strip() and email.strip():
            cur.execute(
                """INSERT INTO employees
                (name, department, position, salary, email)
                VALUES (?, ?, ?, ?, ?)""",
                (name, department, position, salary, email)
            )
            conn.commit()
            st.success("🎉 Employee added successfully!")
        else:
            st.warning("⚠️ Please fill in all fields.")

# 📋 READ
with tab2:
    st.subheader("📋 All Employees")

    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()

    if employees:
        st.dataframe(
            employees,
            column_config={
                1: "🆔 ID",
                2: "👤 Name",
                3: "🏢 Department",
                4: "💼 Position",
                5: st.column_config.NumberColumn(
                    "💰 Salary", format="%.2f"
                ),
                6: "📧 Email"
            },
            hide_index=True
        )
        st.success(f"👥 Total Employees: {len(employees)}")
    else:
        st.info("📭 No employees found. Add an employee first!")

# ✏️ UPDATE
with tab3:
    st.subheader("✏️ Update Employee Information")

    cur.execute("SELECT id, name FROM employees")
    employees = cur.fetchall()

    if employees:
        employee_id = st.selectbox(
            "👤 Select Employee",
            [e[0] for e in employees],
            format_func=lambda x: next(
                e[1] for e in employees if e[0] == x
            )
        )

        cur.execute(
            """SELECT name, department, position, salary, email
            FROM employees WHERE id = ?""",
            (employee_id,)
        )
        employee = cur.fetchone()

        new_name = st.text_input("👤 Employee Name", value=employee[0])
        new_department = st.text_input(
            "🏢 Department", value=employee[1]
        )
        new_position = st.text_input(
            "💼 Job Position", value=employee[2]
        )
        new_salary = st.number_input(
            "💰 Monthly Salary",
            min_value=0.0,
            value=float(employee[3])
        )
        new_email = st.text_input("📧 Email", value=employee[4])

        if st.button("💾 Update Employee"):
            if new_name.strip() and new_department.strip() and new_position.strip() and new_email.strip():
                cur.execute(
                    """UPDATE employees
                    SET name = ?, department = ?, position = ?,
                        salary = ?, email = ?
                    WHERE id = ?""",
                    (
                        new_name, new_department, new_position,
                        new_salary, new_email, employee_id
                    )
                )
                conn.commit()
                st.success("🎉 Employee updated successfully!")
                st.rerun()
            else:
                st.warning("⚠️ Please fill in all fields.")
    else:
        st.info("📭 No employees available to update.")

# 🗑️ DELETE
with tab4:
    st.subheader("🗑️ Delete Employee")

    cur.execute("SELECT id, name FROM employees")
    employees = cur.fetchall()

    if employees:
        employee_id = st.selectbox(
            "👤 Choose Employee to Delete",
            [e[0] for e in employees],
            format_func=lambda x: next(
                e[1] for e in employees if e[0] == x
            ),
            key="delete_employee"
        )

        st.warning("⚠️ Deleting an employee cannot be undone!")

        if st.button("🗑️ Delete Employee"):
            cur.execute(
                "DELETE FROM employees WHERE id = ?",
                (employee_id,)
            )
            conn.commit()
            st.success("✅ Employee deleted successfully!")
            st.rerun()
    else:
        st.info("📭 No employees available to delete.")

# 👤 ABOUT
with tab5:
    st.subheader("👤 About the Developer")

    st.write("🎓 **Name:** RP rabbi")
    st.write("🆔 **Roll:** 778501")
    st.write("🏫 **Department:** CST")
    st.write("📚 **Semester:** 6th")

    st.divider()

    st.subheader("💻 Project Information")
    st.write("📌 **Project:** Employee Management System")
    st.write("🐍 **Backend:** Python + Streamlit")
    st.write("🗄️ **Database:** SQLite3")
    st.write("🔄 **Operations:** Create, Read, Update, Delete")

    st.success("✨ Thank you for visiting my project!")

conn.close()
