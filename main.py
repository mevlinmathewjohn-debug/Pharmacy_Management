
from patient_service import PatientService
from prescription_service import PrescriptionService
from inventory_service import InventoryService
from payment_service import PaymentService
from billing_service import BillingService
from dosage_service import DosageService


def main():

    print("==============================")
    print(" PHARMACY MANAGEMENT SYSTEM")
    print("==============================")

    # 1. Patient Identification

    qr_code = input(
        "Scan / Enter Patient QR Code: "
    ).strip()

    patient_service = PatientService()
    patient = patient_service.find_patient_by_qr(qr_code)

    if not patient:
        print("Patient not found.")
        return

    print("\nPatient Details")
    print("----------------")
    print("Patient ID :", patient["patient_id"])
    print("Name       :", patient["name"])
    print("Phone      :", patient["phone"])

    # 2. Prescription

    prescription_service = PrescriptionService()

    prescriptions = prescription_service.get_patient_prescriptions(
        patient["patient_id"]
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
            float(item["unit_price"]) * item["quantity"]
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

    # 7. Bill

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

    # 8. Token

    token_no = billing_service.create_token(bill_id)

    print("\n==============================")
    print("       TRANSACTION COMPLETE")
    print("==============================")
    print("Patient :", patient["name"])
    print("Amount  : ₹{:.2f}".format(total))
    print("Payment :", method)
    print("Bill ID :", bill_id)
    print("Token   :", token_no)
    print("==============================")


if __name__ == "__main__":
    main()
