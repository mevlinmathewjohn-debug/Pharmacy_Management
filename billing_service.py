from database import DatabaseManager
import random


class BillingService:

    def __init__(self):
        self.db = DatabaseManager()

    def create_bill(
        self,
        payment_id,
        total_amount
    ):

        bill_no = "BILL" + str(
            random.randint(10000, 99999)
        )

        query = """
        INSERT INTO bills
        (
            payment_id,
            bill_no,
            total_amount
        )
        VALUES
        (%s, %s, %s)
        """

        self.db.execute(
            query,
            (
                payment_id,
                bill_no,
                total_amount
            )
        )

        self.db.commit()

        return self.db.cursor.lastrowid

    def create_token(self, bill_id):

        query = """
        SELECT COALESCE(MAX(token_no), 0) + 1
        AS next_token
        FROM tokens
        """

        result = self.db.fetch_one(query)

        token_no = result["next_token"]

        query = """
        INSERT INTO tokens
        (
            bill_id,
            token_no,
            status
        )
        VALUES
        (%s, %s, 'WAITING')
        """

        self.db.execute(
            query,
            (
                bill_id,
                token_no
            )
        )

        self.db.commit()

        return token_no