
from database import DatabaseManager
from datetime import date


class MonthlyAnalysisService:

    def __init__(self):
        self.db = DatabaseManager()

    def generate_monthly_summary(self, year, month):

        if not 1 <= month <= 12:
            raise ValueError("Month must be between 1 and 12.")

        month_start = date(year, month, 1)

        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)

        # 1. Calculate patient visits

        visit_query = """
            SELECT COUNT(*) AS total_visits
            FROM patient_visits
            WHERE visit_date >= %s
              AND visit_date < %s
        """

        visit_result = self.db.fetch_all(
            visit_query,
            (month_start, next_month)
        )

        total_visits = visit_result[0]["total_visits"]

        # 2. Calculate successful payments and sales

        sales_query = """
            SELECT
                COUNT(*) AS total_payments,
                COALESCE(SUM(amount), 0) AS total_sales,
                COALESCE(SUM(
                    CASE WHEN method = 'CASH'
                    THEN amount ELSE 0 END
                ), 0) AS cash_sales,
                COALESCE(SUM(
                    CASE WHEN method = 'UPI'
                    THEN amount ELSE 0 END
                ), 0) AS upi_sales,
                COALESCE(SUM(
                    CASE WHEN method = 'CARD'
                    THEN amount ELSE 0 END
                ), 0) AS card_sales
            FROM payments
            WHERE status = 'SUCCESS'
              AND paid_at >= %s
              AND paid_at < %s
        """

        sales_result = self.db.fetch_all(
            sales_query,
            (month_start, next_month)
        )

        sales = sales_result[0]

        # 3. Insert or update the monthly analysis record

        save_query = """
            INSERT INTO monthly_analysis (
                month_start,
                total_visits,
                total_payments,
                total_sales,
                cash_sales,
                upi_sales,
                card_sales,
                generated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE
                total_visits = VALUES(total_visits),
                total_payments = VALUES(total_payments),
                total_sales = VALUES(total_sales),
                cash_sales = VALUES(cash_sales),
                upi_sales = VALUES(upi_sales),
                card_sales = VALUES(card_sales),
                generated_at = NOW()
        """

        self.db.execute(
            save_query,
            (
                month_start,
                total_visits,
                sales["total_payments"],
                sales["total_sales"],
                sales["cash_sales"],
                sales["upi_sales"],
                sales["card_sales"]
            )
        )

        self.db.commit()

        print("\n========== MONTHLY SUMMARY ==========")
        print("Month:", month_start.strftime("%B %Y"))
        print("Patient visits:", total_visits)
        print("Successful payments:", sales["total_payments"])
        print("Total sales: ₹{:.2f}".format(
            float(sales["total_sales"])
        ))
        print("Cash sales: ₹{:.2f}".format(
            float(sales["cash_sales"])
        ))
        print("UPI sales: ₹{:.2f}".format(
            float(sales["upi_sales"])
        ))
        print("Card sales: ₹{:.2f}".format(
            float(sales["card_sales"])
        ))
        print("=====================================")

        return True

    def display_monthly_summary(self, year, month):

        month_start = date(year, month, 1)

        query = """
            SELECT *
            FROM monthly_analysis
            WHERE month_start = %s
        """

        result = self.db.fetch_all(query, (month_start,))

        if not result:
            print("No monthly analysis found.")
            return

        row = result[0]

        print("\n========== SAVED MONTHLY ANALYSIS ==========")
        print("Month:", row["month_start"])
        print("Total visits:", row["total_visits"])
        print("Total payments:", row["total_payments"])
        print("Total sales: ₹{:.2f}".format(
            float(row["total_sales"])
        ))
        print("Cash sales: ₹{:.2f}".format(
            float(row["cash_sales"])
        ))
        print("UPI sales: ₹{:.2f}".format(
            float(row["upi_sales"])
        ))
        print("Card sales: ₹{:.2f}".format(
            float(row["card_sales"])
        ))
        print("Generated at:", row["generated_at"])
        print("============================================")
