import json
import os

FILE_NAME = "repairs.json"


def load_repairs():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_repairs(repairs):
    with open(FILE_NAME, "w") as file:
        json.dump(repairs, file, indent=4)


repairs = load_repairs()

while True:
    print("\n=== SMART DEVICE CARE TRACKER ===")
    print("1. Add new repair")
    print("2. View all repairs")
    print("3. Update repair status")
    print("4. Exit")
    print("5. Search repair by ID")
    print("6. Repair Summary")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        name = input("Customer name: ")
        device = input("Device name: ")
        problem = input("Device problem: ")

        repair = {
            "id": max(
                [r.get("id", 0) for r in repairs],
                default=0
            ) + 1,
            "customer": name,
            "device": device,
            "problem": problem,
            "status": "Received"
        }

        repairs.append(repair)
        save_repairs(repairs)
        print("Repair record saved successfully!")

    elif choice == "2":
        if not repairs:
            print("No repair records found.")
        else:
            for repair in repairs:
                print("\nRepair ID:", repair["id"])
                print("Customer:", repair["customer"])
                print("Device:", repair["device"])
                print("Problem:", repair["problem"])
                print("Status:", repair["status"])

    elif choice == "3":
        repair_id = input("Enter repair ID: ").strip()
        found = False

        for repair in repairs:
            if str(repair["id"]) == repair_id:
                print("1. Received")
                print("2. In Progress")
                print("3. Ready for Pickup")
                print("4. Delivered")

                status_choice = input("Choose new status: ").strip()

                statuses = {
                    "1": "Received",
                    "2": "In Progress",
                    "3": "Ready for Pickup",
                    "4": "Delivered"
                }

                if status_choice in statuses:
                    repair["status"] = statuses[status_choice]
                    save_repairs(repairs)
                    print("Status updated successfully!")
                else:
                    print("Invalid status choice.")

                found = True
                break

        if not found:
            print("Repair ID not found.")

    elif choice == "4":
        print("Thank you for using the tracker!")
        break

    elif choice == "5":
        repair_id = input("Enter repair ID to search: ").strip()
        found = False

        for repair in repairs:
            if str(repair["id"]) == repair_id:
                print("\n--- Repair Details ---")
                print("Repair ID:", repair["id"])
                print("Customer:", repair["customer"])
                print("Device:", repair["device"])
                print("Problem:", repair["problem"])
                print("Status:", repair["status"])
                found = True
                break

        if not found:
            print("Repair ID not found.")

    elif choice == "6":
        print("\n--- Repair Summary ---")

        total = len(repairs)
        received = sum(
            1 for r in repairs if r["status"] == "Received"
        )
        in_progress = sum(
            1 for r in repairs if r["status"] == "In Progress"
        )
        ready = sum(
            1 for r in repairs if r["status"] == "Ready for Pickup"
        )
        delivered = sum(
            1 for r in repairs if r["status"] == "Delivered"
        )

        print("Total Repairs:", total)
        print("Received:", received)
        print("In Progress:", in_progress)
        print("Ready for Pickup:", ready)
        print("Delivered:", delivered)

    else:
        print("Invalid choice. Please choose 1 to 6.")