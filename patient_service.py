from database import DatabaseManager


class PatientService:

    def __init__(self):
        self.db = DatabaseManager()

    def find_patient_by_qr(self, qr_code):
        qr_code = qr_code.strip()

        connection = self.db.connection
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT patient_id, qr_code, name, phone
                FROM patients
                WHERE TRIM(qr_code) = %s
                """,
                (qr_code,)
            )

            patient = cursor.fetchone()

            print("DEBUG QR:", repr(qr_code))
            print("DEBUG Patient:", patient)

            return patient

        finally:
            cursor.close()  