from google.adk.agents import Agent
import mysql.connector

# --- Login tool ---
def login(username: str, password: str) -> dict:
    """
    Checks the given username and password against MySQL.
    Stores logged-in user in agent state for session persistence.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="asha"
        )
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            # Persist login in agent state
            state["logged_in_user"] = username
            return {"status": "success", "message": f"Congrats {username}! Welcome back."}
        else:
            return {"status": "error", "message": "Invalid username or password."}

    except mysql.connector.Error as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


# --- Enrollment tool ---
def enroll_person(name: str, dob: str, address: str, district: str, state_name: str, category: str,) -> dict:
    """
    Enrolls a new person (child or woman) into the database.
    Only works if a user is logged in.
    """
    

    if category.lower() not in ['child', 'woman']:
        return {"status": "error", "message": "Category must be 'child' or 'woman'."}

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="asha"
        )
        cursor = conn.cursor()
        query = """
            INSERT INTO persons (name, dob, address, district, state, category)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, dob, address, district, state_name, category.lower()))
        conn.commit()

        return {
            "status": "success",
            "message": f"{name} has been successfully enrolled as a {category} by {logged_in_user}."
        }

    except mysql.connector.Error as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()



def add_visit(
    patient_name: str,
    visit_type: str,
    blood_pressure: str,
    temperature: float,
    weight: float,
    pulse_rate: int,
    symptoms: str,
    additional_info: str,
) -> dict:
    """
    Adds a new visit to the 'visits' table.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="asha"
        )
        cursor = conn.cursor()
        query = """
            INSERT INTO visits
            (patient_name, visit_type, blood_pressure, temperature, weight, pulse_rate, symptoms, additional_info)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                patient_name,
                visit_type,
                blood_pressure,
                temperature,
                weight,
                pulse_rate,
                json.dumps(symptoms),  # store list as JSON
                additional_info
            )
        )
        conn.commit()

        return {
            "status": "success",
            "message": f"Visit for {patient_name} successfully added."
        }

    except mysql.connector.Error as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# --- Create the agent ---
root_agent = Agent(
    name="asha_agent",
    model="gemini-2.0-flash",
    description="Interactive ASHA agent for login and enrolling persons (child/woman).",
    instruction="""
You are a helpful ASHA assistant agent.
1. Ask users to log in using their username and password.
2. Only allow enrolling a person if the user is logged in.
3. When enrolling, ask for name, date of birth (YYYY-MM-DD), address, district, state, and category (child/woman).
4. Return clear messages to the user.
""",
    tools=[login, enroll_person, add_visit],
)
