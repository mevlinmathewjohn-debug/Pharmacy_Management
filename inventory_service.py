from database import DatabaseManager


class InventoryService:

    def __init__(self):
        self.db = DatabaseManager()

    def check_availability(
        self,
        prescription_id
    ):

        query = """
        SELECT
            m.medicine_id,
            m.name,
            pi.quantity AS required_qty,
            i.stock_qty,

            CASE
                WHEN i.stock_qty >= pi.quantity
                THEN 'AVAILABLE'
                ELSE 'NOT AVAILABLE'
            END AS availability

        FROM prescription_items pi

        JOIN medicines m
        ON pi.medicine_id = m.medicine_id

        JOIN inventory i
        ON m.medicine_id = i.medicine_id

        WHERE pi.prescription_id = %s
        """

        return self.db.fetch_all(
            query,
            (prescription_id,)
        )

    def all_available(
        self,
        prescription_id
    ):

        medicines = self.check_availability(
            prescription_id
        )

        for medicine in medicines:

            if medicine["availability"] != "AVAILABLE":
                return False

        return True