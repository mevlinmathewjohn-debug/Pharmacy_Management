from database import DatabaseManager
from datetime import datetime


class PaymentService:

    def __init__(self):
        self.db = DatabaseManager()

    def make_payment(
        self,
        prescription_id,
        amount,
        method
    ):

        query = """
        INSERT INTO payments
        (
            prescription_id,
            amount,
            method,
            status,
            paid_at
        )
        VALUES
        (%s, %s, %s, 'SUCCESS', %s)
        """

        self.db.execute(
            query,
            (
                prescription_id,
                amount,
                method,
                datetime.now()
            )
        )

        self.db.commit()

        return self.db.cursor.lastrowid