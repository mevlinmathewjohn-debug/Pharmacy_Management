
from database import DatabaseManager


class PatientHistoryService:

    def __init__(self):
        self.db = DatabaseManager()

    # 1. Record a new patient visit
    def record_visit(
        self,
        patient_id,
        prescription_id,
        next_visit_date=None,
        visit_notes="Pharmacy visit completed"
    ):
        query = """
            INSERT INTO patient_visits
            (
                patient_id,
                prescription_id,
                next_visit_date,
                visit_notes
            )
            VALUES (%s, %s, %s, %s)
        """

        try:
            self.db.execute(
                query,
                (
                    patient_id,
                    prescription_id,
                    next_visit_date,
                    visit_notes
                )
            )

            self.db.commit()

            visit_id = self.db.cursor.lastrowid

            print("Patient visit saved successfully.")
            print("Visit ID:", visit_id)

            return visit_id

        except Exception as error:
            print("Error recording patient visit:", error)
            return None

    # 2. Get history for a specific patient
    def get_patient_history(self, patient_id):
        query = """
            SELECT
                visit_id,
                patient_id,
                prescription_id,
                visit_date,
                next_visit_date,
                visit_notes
            FROM patient_visits
            WHERE patient_id = %s
            ORDER BY visit_date DESC
        """

        return self.db.fetch_all(query, (patient_id,))

    # 3. Display a specific patient's history
    def display_patient_history(self, patient_id):
        visits = self.get_patient_history(patient_id)

        print("\n========== PATIENT VISIT HISTORY ==========")

        if not visits:
            print("No visit history found.")
            return

        for visit in visits:
            print("\nVisit ID       :", visit["visit_id"])
            print("Patient ID     :", visit["patient_id"])
            print("Prescription ID:", visit["prescription_id"])
            print("Visit Date     :", visit["visit_date"])
            print("Next Visit     :", visit["next_visit_date"])
            print("Notes          :", visit["visit_notes"])
            print("-------------------------------------------")

    # 4. Display visit history for all patients
    def display_all_visits(self):
        query = """
            SELECT
                pv.visit_id,
                pv.patient_id,
                p.name AS patient_name,
                pv.prescription_id,
                pv.visit_date,
                pv.next_visit_date,
                pv.visit_notes
            FROM patient_visits pv
            JOIN patients p
                ON pv.patient_id = p.patient_id
            ORDER BY pv.visit_date DESC
        """

        visits = self.db.fetch_all(query)

        print("\n========== ALL PATIENT VISITS ==========")

        if not visits:
            print("No visit records found.")
            return

        for visit in visits:
            print("\nVisit ID       :", visit["visit_id"])
            print("Patient Name   :", visit["patient_name"])
            print("Patient ID     :", visit["patient_id"])
            print("Prescription ID:", visit["prescription_id"])
            print("Visit Date     :", visit["visit_date"])
            print("Next Visit     :", visit["next_visit_date"])
            print("Notes          :", visit["visit_notes"])
            print("----------------------------------------")
