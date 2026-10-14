from database import DatabaseManager
class MedicineService:

    def __init__(self):
        self.db = DatabaseManager()

    def get_all_medicines(self):

        query = """
        SELECT *
        FROM medicines
        ORDER BY name
        """

        return self.db.fetch_all(query)

    def get_medicine(self, medicine_id):

        query = """
        SELECT *
        FROM medicines
        WHERE medicine_id = %s
        """

        return self.db.fetch_one(
            query,
            (medicine_id,)
        )