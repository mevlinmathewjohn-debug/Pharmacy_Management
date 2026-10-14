from database import DatabaseManager


class PrescriptionService:

    def __init__(self):
        self.db = DatabaseManager()

    def get_patient_prescriptions(self, patient_id):
        query = """
            SELECT
                prescription_id,
                patient_id,
                prescribed_date,
                status
            FROM prescriptions
            WHERE patient_id = %s
            ORDER BY prescription_id DESC
        """

        return self.db.fetch_all(query, (patient_id,))

    def get_prescription_items(self, prescription_id):
        query = """
            SELECT
                pi.item_id,
                pi.prescription_id,
                m.medicine_id,
                m.name,
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

        return self.db.fetch_all(query, (prescription_id,))