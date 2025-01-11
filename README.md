# PocketSense API Documentation

## Core Implementation

### 1. **Database Design and Models:**

- **Expenses**: Stores details about each expense, including:
  - `amount`: The cost of the expense.
  - `category`: The category of the expense (food, travel, academics, entertainment, etc.).
  - `split_type`: How the expense is split (even, unequal).
  - `date`: The date the expense was recorded.
  - `receipt_image`: An optional field to store the receipt image for the expense.

- **Students**: Extends Django's built-in `User` model, adding:
  - `college`: The student's college name.
  - `semester`: The student's current semester.
  - `default_payment_methods`: Default payment methods used by the student.

- **Groups**: Used for managing user groups, such as:
  - `hostel_roommates`, `project_teams`, `trip_groups`.

- **Settlements**: Tracks payment settlements between users.
  - `payment_status`: Indicates whether the payment is completed, pending, etc.
  - `settlement_method`: Describes the method used for the settlement.
  - `due_date`: The due date for the payment settlement.

- **Categories**: Represents the types of expenses:
  - `food`, `travel`, `academics`, `entertainment`.

---

## Authentication System

### **1. Token-Based Authentication**
- Users authenticate via JWT tokens. Each user is given a unique token when they log in.
  
- **Login Endpoint**: `/login/`
    - This endpoint returns a JWT token upon successful login.
  
- **Authorization**: 
    - All API requests are authorized. Only authenticated users can access the services. The JWT token must be included in the `Authorization` header for every request.

### **2. College Email Verification**
- Upon registration, users must verify their college email.
  
- **Email Verification Endpoint**: `/verify-email/<uidb64>/<token>/`
    - This endpoint verifies the user’s email address after they click on the verification link sent to their email.

---

## API Endpoints

### **1. User Authentication:**

- **Register**: `POST /register/`
    - Registers a new user by providing details such as name, email, password, etc.
  
- **Login**: `POST /login/`
    - Logs in a user and provides a JWT token for authentication.
  
- **Email Verification**: `GET /verify-email/<uidb64>/<token>/`
    - Verifies the user’s email address after clicking on the verification link.

---

### **2. Expense Management:**

- **Create Expense**: `POST /create/`
    - Creates a new expense record. The user must provide the expense amount, category, date, and split type.

- **Expense Categorization**: `GET /expense-categorization/`
    - Retrieves a list of possible categories for the expense.

---

### **3. Category Management:**

- **Create Category**: `POST /categories/create/`
    - Allows an authenticated user to create a new category.
  
- **List Categories**: `GET /categories/list/`
    - Lists all available expense categories.
  
- **Retrieve Category**: `GET /categories/retrieve/<int:pk>/`
    - Retrieves details of a specific category by its ID.
  
- **Update Category**: `PUT /categories/update/<int:pk>/`
    - Updates an existing category’s details.
  
- **Delete Category**: `DELETE /categories/delete/<int:pk>/`
    - Deletes a category by its ID.

---

### **4. Group Management:**

- **Create Group**: `POST /group/create/`
    - Creates a new group (e.g., project team, roommates, etc.).
  
- **List Groups**: `GET /group/list/`
    - Lists all user groups.
  
- **Retrieve Group**: `GET /group/retrieve/<int:pk>/`
    - Retrieves details of a specific group by its ID.
  
- **Update Group**: `PUT /group/update/<int:pk>/`
    - Updates the details of an existing group.
  
- **Delete Group**: `DELETE /group/delete/<int:pk>/`
    - Deletes a group by its ID.

---

### **5. Settlement Management:**

- **Create Settlement**: `POST /settlements/create/`
    - Creates a new settlement between users, indicating the payment status and due date.
  
- **List Settlements**: `GET /settlements/list/`
    - Lists all the settlements created by the user.
  
- **Retrieve Settlement**: `GET /settlements/retrieve/<int:pk>/`
    - Retrieves details of a specific settlement by its ID.
  
- **Update Settlement**: `PUT /settlements/update/<int:pk>/`
    - Updates the settlement details.
  
- **Delete Settlement**: `DELETE /settlements/delete/<int:pk>/`
    - Deletes a settlement by its ID.

---

### **6. Monthly Analysis:**

- **Monthly Analysis**: `GET /monthly-analysis/`
    - Provides an analysis of monthly expenses, including total expenses, category breakdowns, and trends over time.

---

### **7. Budget Management:**

- **Create Budget**: `POST /budget/create/`
    - Creates a new budget for the user with a specific limit and category allocation.

- **List Budgets**: `GET /budget/list/`
    - Lists all budgets for the user.
  
- **Retrieve Budget**: `GET /budget/retrieve/<int:pk>/`
    - Retrieves details of a specific budget by its ID.

- **Update Budget**: `PUT /budget/update/<int:pk>/`
    - Updates a specific budget.

- **Delete Budget**: `DELETE /budget/delete/<int:pk>/`
    - Deletes a specific budget.

---

### **8. Budget Analysis:**

- **Budget Analysis**: `GET /budget-analysis/`
    - Analyzes and provides insights into a user’s budget spending over time.

---

### **9. Spending Patterns Analysis:**

- **Spending Patterns**: `GET /spending-analysis/`
    - Provides an analysis of user spending patterns, including total spending, category-wise breakdown, and trends over time (monthly/weekly).

---

### **10. Settlement Suggestions:**

- **Settlement Suggestions**: `GET /settlement-suggestion/`
    - Provides suggestions for settlement based on user spending patterns and debts.

---

## Advanced Features

### **1. Expense Categorization:**
- Expenses are categorized automatically based on pre-defined categories such as food, travel, entertainment, etc.
- Users can customize their categorization rules for more accuracy.

### **2. Monthly Budget Tracking:**
- Users can create budgets and track how much of the budget they’ve spent in different categories over the month.
- Provides insights into the budget status.

### **3. Spending Patterns Analysis:**
- Provides deeper insights into a user’s spending habits, including total spending per category, trends over time, and spending distributions.

---

## Scripts and Background Jobs

### **1. Payment Reminder Script**
- An automated script runs to remind users about any outstanding payments or settlements.
- The reminder is triggered based on user-defined criteria (e.g., due date or spending thresholds).

---

## Conclusion

The PocketSense API provides an efficient way for users to manage their expenses, track settlements, and analyze spending patterns. The flexible endpoints for user authentication, expense categorization, and group management make it an effective tool for financial planning and budgeting. With advanced features like monthly budget tracking and spending pattern analysis, users can gain deeper insights into their financial habits.
