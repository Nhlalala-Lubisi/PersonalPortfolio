package nhlaks.employeemanagementsystem;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Scanner;

public class EmployeeManagementSystem {

    private static final List<Employee> employees = new ArrayList<>();
    private static int nextId = 1;
    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.println("=== Employee Management System ===");

        // Seed some data so you have something to work with immediately
        addEmployee("Nhlalala Khoza", "IT", 35000);
        addEmployee("Thabo Nkosi", "Finance", 42000);
        addEmployee("Lerato Dlamini", "HR", 31500);

        boolean running = true;
        while (running) {
            printMenu();
            int choice = readInt("Enter choice: ");
            System.out.println();

            switch (choice) {
                case 1 -> createEmployee();
                case 2 -> readAllEmployees();
                case 3 -> readEmployeeById();
                case 4 -> updateEmployee();
                case 5 -> deleteEmployee();
                case 6 -> { running = false; System.out.println("Goodbye!"); }
                default -> System.out.println("Invalid option. Try again.\n");
            }
        }

        scanner.close();
    }

    // ─── CRUD Operations ─────────────────────────────────────────────────────

    /** CREATE — prompts user for employee details and adds to list */
    private static void createEmployee() {
        System.out.println("--- Add New Employee ---");
        String name = readString("Name: ");
        String dept = readString("Department: ");
        double salary = readDouble("Salary (R): ");

        Employee emp = addEmployee(name, dept, salary);
        System.out.printf("✔ Employee added with ID %d.%n%n", emp.getId());
    }

    /** READ ALL — displays every employee in the list */
    private static void readAllEmployees() {
        System.out.println("--- All Employees ---");
        if (employees.isEmpty()) {
            System.out.println("No employees found.\n");
            return;
        }
        employees.forEach(System.out::println);
        System.out.printf("%nTotal: %d employee(s)%n%n", employees.size());
    }

    /** READ ONE — finds an employee by ID */
    private static void readEmployeeById() {
        int id = readInt("Enter employee ID: ");
        findById(id).ifPresentOrElse(
                emp -> System.out.println("\nFound: " + emp + "\n"),
                ()  -> System.out.println("No employee with ID " + id + ".\n")
        );
    }

    /** UPDATE — lets user change name, department, or salary */
    private static void updateEmployee() {
        int id = readInt("Enter employee ID to update: ");
        Optional<Employee> result = findById(id);

        if (result.isEmpty()) {
            System.out.println("Employee not found.\n");
            return;
        }

        Employee emp = result.get();
        System.out.println("Current record: " + emp);
        System.out.println("(Press Enter to keep current value)");

        String name = readString("New name [" + emp.getName() + "]: ");
        String dept = readString("New department [" + emp.getDepartment() + "]: ");
        String salaryInput = readString("New salary [" + emp.getSalary() + "]: ");

        if (!name.isBlank())       emp.setName(name);
        if (!dept.isBlank())       emp.setDepartment(dept);
        if (!salaryInput.isBlank()) {
            try { emp.setSalary(Double.parseDouble(salaryInput)); }
            catch (NumberFormatException e) { System.out.println("Invalid salary — kept original."); }
        }

        System.out.println("✔ Updated: " + emp + "\n");
    }

    /** DELETE — removes an employee by ID */
    private static void deleteEmployee() {
        int id = readInt("Enter employee ID to delete: ");
        boolean removed = employees.removeIf(e -> e.getId() == id);
        System.out.println(removed
                ? "✔ Employee " + id + " deleted.\n"
                : "Employee not found.\n");
    }

    // ─── Helpers ─────────────────────────────────────────────────────────────

    private static Employee addEmployee(String name, String dept, double salary) {
        Employee emp = new Employee(nextId++, name, dept, salary);
        employees.add(emp);
        return emp;
    }

    private static Optional<Employee> findById(int id) {
        return employees.stream().filter(e -> e.getId() == id).findFirst();
    }

    private static void printMenu() {
        System.out.println("""
                ┌─────────────────────────┐
                │  1. Add Employee        │
                │  2. View All            │
                │  3. View by ID          │
                │  4. Update Employee     │
                │  5. Delete Employee     │
                │  6. Exit                │
                └─────────────────────────┘""");
    }

    private static String readString(String prompt) {
        System.out.print(prompt);
        return scanner.nextLine().trim();
    }

    private static int readInt(String prompt) {
        while (true) {
            System.out.print(prompt);
            try {
                int val = Integer.parseInt(scanner.nextLine().trim());
                return val;
            } catch (NumberFormatException e) {
                System.out.println("Please enter a whole number.");
            }
        }
    }

    private static double readDouble(String prompt) {
        while (true) {
            System.out.print(prompt);
            try {
                return Double.parseDouble(scanner.nextLine().trim());
            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid number.");
            }
        }
    }
}