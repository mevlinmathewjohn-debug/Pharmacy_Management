
from database import DatabaseManager
class DosageService:

    def __init__(self):
        self.db = DatabaseManager()

    def get_patient_dosage(self, prescription_id):

        query = """
            SELECT
                pi.item_id,
                pi.prescription_id,
                m.medicine_id,
                m.name AS medicine_name,
                m.strength,
                m.form,
                m.unit_price,
                pi.quantity,
                pi.dosage
            FROM prescription_items pi
            JOIN medicines m
                ON pi.medicine_id = m.medicine_id
            WHERE pi.prescription_id = %s
        """

        return self.db.fetch_all(
            query,
            (prescription_id,)
        )

    def display_patient_dosage(self, prescription_id):

        medicines = self.get_patient_dosage(
            prescription_id
        )

        if not medicines:
            print("No dosage details found.")
            return False

        print("\n======================================")
        print("       PATIENT MEDICINE DETAILS")
        print("======================================")

        for medicine in medicines:
            print("\nMedicine     :", medicine["medicine_name"])
            print("Strength     :", medicine["strength"])
            print("Form         :", medicine["form"])
            print("Quantity     :", medicine["quantity"])
            print("Dosage       :", medicine["dosage"])
            print("--------------------------------------")

        print("\nPlease follow your prescribed dosage.")
        return True
