
from datetime import date

from patient_service import PatientService
from prescription_service import PrescriptionService
from inventory_service import InventoryService
from payment_service import PaymentService
from billing_service import BillingService
from dosage_service import DosageService
from patient_history_service import PatientHistoryService
from monthly_analysis_service import MonthlyAnalysisService


def main():

    print("==============================")
    print(" PHARMACY MANAGEMENT SYSTEM")
    print("==============================")

    # 1. Patient Identification

    qr_code = input("Scan / Enter Patient QR Code: ").strip()

    patient_service = PatientService()
    patient = patient_service.find_patient_by_qr(qr_code)

    if not patient:
        print("Patient not found.")
        return

    patient_id = patient["patient_id"]

    print("\nPatient Details")
    print("----------------")
    print("Patient ID :", patient_id)
    print("Name       :", patient["name"])
    print("Phone      :", patient["phone"])

    # 2. Prescription

    prescription_service = PrescriptionService()

    prescriptions = prescription_service.get_patient_prescriptions(
        patient_id
    )

    if not prescriptions:
        print("No prescription found.")
        return

    prescription = prescriptions[0]
    prescription_id = prescription["prescription_id"]

    print("\nPrescription ID:", prescription_id)

    # 3. Dosage Details

    dosage_service = DosageService()

    dosage_found = dosage_service.display_patient_dosage(
        prescription_id
    )

    if not dosage_found:
        print("Cannot continue without prescription items.")
        return

    # 4. Medicine Costs

    items = prescription_service.get_prescription_items(
        prescription_id
    )

    if not items:
        print("No prescription medicines found.")
        return

    print("\nMedicine Bill Details")
    print("------------------------------")

    total = 0.0

    for item in items:
        item_total = (
            float(item["unit_price"]) * int(item["quantity"])
        )
        total += item_total

        print(
            item["name"],
            "| Quantity:", item["quantity"],
            "| Amount: ₹{:.2f}".format(item_total)
        )

    print("\nTotal Amount: ₹{:.2f}".format(total))

    # 5. Inventory Check

    inventory_service = InventoryService()

    available = inventory_service.all_available(
        prescription_id
    )

    if not available:
        print("\nSome medicines are not available.")
        return

    print("\nAll medicines are available.")

    # 6. Payment

    method = input(
        "Payment Method (CASH/UPI/CARD): "
    ).strip().upper()

    if method not in ["CASH", "UPI", "CARD"]:
        print("Invalid payment method.")
        return

    payment_service = PaymentService()

    payment_id = payment_service.make_payment(
        prescription_id,
        total,
        method
    )

    if not payment_id:
        print("Payment failed. Bill not generated.")
        return

    print("\nPayment Successful!")
    print("Payment ID:", payment_id)

    # 7. Bill Generation

    billing_service = BillingService()

    bill_id = billing_service.create_bill(
        payment_id,
        total
    )

    if not bill_id:
        print("Bill generation failed.")
        return

    print("Bill generated successfully.")
    print("Bill ID:", bill_id)

    # 8. Token Generation

    token_no = billing_service.create_token(bill_id)

    if not token_no:
        print("Warning: Token generation may have failed.")

    # 9. Patient Visit History

    patient_history_service = PatientHistoryService()

    next_visit_input = input(
        "\nNext Visit Date (YYYY-MM-DD, or press Enter to skip): "
    ).strip()

    if next_visit_input:
        try:
            next_visit_date = date.fromisoformat(next_visit_input)

            if next_visit_date < date.today():
                print("Next visit date cannot be in the past.")
                next_visit_date = None

        except ValueError:
            print("Invalid date. Next visit date will be left empty.")
            next_visit_date = None
    else:
        next_visit_date = None

    visit_id = patient_history_service.record_visit(
        patient_id=patient_id,
        prescription_id=prescription_id,
        next_visit_date=next_visit_date,
        visit_notes=(
            "Prescription processed; payment and billing completed"
        )
    )

    if visit_id:
        print("\nPatient visit recorded. Visit ID:", visit_id)
        patient_history_service.display_patient_history(patient_id)
    else:
        print("\nWarning: Patient visit history was not saved.")

    # 10. Monthly Analysis

    print("\n========== MONTHLY ANALYSIS ==========")

    monthly_analysis_service = MonthlyAnalysisService()

    today = date.today()

    try:
        # The service expects year and month arguments.
        analysis_updated = (
            monthly_analysis_service.generate_monthly_summary(
                today.year,
                today.month
            )
        )

        if analysis_updated is False:
            print("Monthly analysis could not be generated.")

    except Exception as error:
        print("Monthly analysis error:", error)

    # 11. Transaction Summary

    print("\n==============================")
    print("       TRANSACTION COMPLETE")
    print("==============================")
    print("Patient :", patient["name"])
    print("Amount  : ₹{:.2f}".format(total))
    print("Payment :", method)
    print("Bill ID :", bill_id)
    print("Token   :", token_no)
    print("Visit ID:", visit_id)
    print("==============================")


if __name__ == "__main__":
    main()
