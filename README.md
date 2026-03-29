<h1 align="center"> Vendorapp </h1>
<p align="center"> A Comprehensive Multi-Vendor Marketplace Ecosystem Engineered for Seamless Commerce and Scalable Growth </p>

<p align="center">
  <img alt="Build" src="https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge">
  <img alt="Issues" src="https://img.shields.io/badge/Issues-0%20Open-blue?style=for-the-badge">
  <img alt="Contributions" src="https://img.shields.io/badge/Contributions-Welcome-orange?style=for-the-badge">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>
<!-- 
  **Note:** These are static placeholder badges. Replace them with your project's actual badges.
  You can generate your own at https://shields.io
-->

## 📑 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack & Architecture](#-tech-stack--architecture)
- [Project Structure](#-project-structure)
- [Environment Variables](#-environment-variables)
- [API Keys Setup](#-api-keys-setup)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**Vendorapp** is a sophisticated, end-to-end e-commerce solution designed to facilitate a robust multi-vendor marketplace. It bridges the gap between independent sellers and global consumers by providing a structured, secure, and intuitive platform for product discovery, transaction management, and order fulfillment. Built on the powerful Django framework, Vendorapp handles the complexities of vendor onboarding, inventory control, and customer lifecycle management within a unified digital ecosystem.

> In the modern digital economy, independent vendors often face significant technical barriers when attempting to establish a professional online presence. Managing inventory, processing secure payments, tracking complex order statuses, and maintaining customer trust through reviews are significant operational hurdles. Simultaneously, customers require a centralized, reliable destination where they can browse diverse products, manage personal wishlists, and track their purchases with confidence. Vendorapp solves these challenges by providing a turnkey infrastructure that automates the commerce lifecycle for both parties.

The solution leverages an **MVC (Model-View-Controller)** architecture to ensure a strict separation of concerns, allowing for rapid scaling and maintainable business logic. By integrating comprehensive data persistence for products, carts, wishlists, and order histories, Vendorapp delivers a professional-grade shopping experience that rivals major industry marketplaces.

---

## ✨ Key Features

### 🏪 Vendor Management & Empowerment
*   **Streamlined Vendor Onboarding:** A dedicated registration and login portal tailored specifically for sellers, ensuring a distinct entry point into the ecosystem.
*   **Intuitive Vendor Dashboard:** A centralized command center where vendors can monitor sales, manage product catalogs, and oversee pending orders in real-time.
*   **Granular Product Control:** Full CRUD (Create, Read, Update, Delete) capabilities for products, including support for categories, quantities, unit sizes, and high-quality image uploads.
*   **Order Fulfillment Lifecycle:** Vendors can update order statuses, manage delivery details, and process customer return requests through a structured workflow.

### 🛍️ Premium Customer Experience
*   **Personalized Shopping Journey:** Dedicated customer dashboards that store order history, allow for easy reordering, and provide status updates on active shipments.
*   **Advanced Cart Management:** A persistent shopping cart system that allows users to adjust quantities, select specific product sizes, and proceed through a secure checkout.
*   **Curated Wishlists:** Empower users to save products for later, with one-click functionality to move individual items or entire lists directly into the active shopping cart.
*   **Transparent Reviews:** An integrated rating and review system that builds community trust by allowing verified customers to share feedback on their purchases.

### 🛡️ Administrative Governance
*   **Custom Admin Dashboard:** A specialized interface for platform moderators to maintain marketplace integrity.
*   **Vendor Vetting System:** A critical "Toggle Approval" feature that allows administrators to vet and approve vendors before their products become visible to the public.
*   **Comprehensive Order Oversight:** Global visibility into transactions, enabling dispute resolution and delivery monitoring across the entire platform.

---

## 🛠️ Tech Stack & Architecture

Vendorapp is built using a modern, industry-standard stack focused on stability, security, and developer productivity.

| Technology | Purpose | Why it was Chosen |
| :--- | :--- | :--- |
| **Python** | Core Language | Provides high readability and extensive libraries for handling complex logic. |
| **Django** | Backend Framework | A high-level Python web framework that encourages rapid development and clean, pragmatic design. |
| **Django MVC** | Architecture Pattern | Ensures separation of data (Models), logic (Views), and presentation (Templates). |
| **SQLite / SQL** | Database | Used for robust data persistence of users, products, and transaction records. |
| **Dotenv (.env)** | Configuration | Secures sensitive environment variables and credentials outside of the codebase. |

### Architectural Design
The project follows the Django **MVC (Model-View-Template)** pattern:
-   **Models:** Located in `sales/models.py`, defining the schema for `Vendor`, `Product`, `Customer`, `Cart`, `Wishlist`, `Order`, and `Review`.
-   **Views:** Contained in `sales/views.py`, handling the heavy lifting of business logic, authentication, and state management.
-   **Templates:** A rich set of HTML components in `sales/templates/`, providing the user interface for every stage of the commerce funnel.

---

## 📁 Project Structure

```
shankars2006-Vendorapp-d102c10/
├── 📁 sales/                        # Core application logic
│   ├── 📁 migrations/               # Database schema versioning
│   ├── 📁 templates/                # UI presentation layer
│   │   └── 📁 sales/                # App-specific HTML templates
│   │       ├── 📄 customer_login.html
│   │       ├── 📄 vendor_dashboard.html
│   │       ├── 📄 cart.html
│   │       ├── 📄 checkout.html
│   │       └── 📄 index.html        # Marketplace homepage
│   ├── 📄 admin.py                  # Admin interface configuration
│   ├── 📄 forms.py                  # User input validation & processing
│   ├── 📄 models.py                 # Data architecture & relations
│   ├── 📄 urls.py                   # Routing & endpoint mapping
│   └── 📄 views.py                  # Controller logic & request handling
├── 📁 vendorapp/                    # Project-wide configuration
│   ├── 📄 settings.py               # Global app settings
│   ├── 📄 urls.py                   # Root URL routing
│   └── 📄 wsgi.py                   # Web server interface
├── 📁 media/                        # User-uploaded assets
│   ├── 📁 products/                 # Product catalog imagery
│   └── 📁 payments/                 # Transaction-related documentation
├── 📄 manage.py                     # Administrative entry point
├── 📄 requirements.txt              # Project dependencies
├── 📄 .env                          # Configuration environment
└── 📄 db.sqlite3                    # Local data persistence
```

---

## 🔐 Environment Variables

The application utilizes a `.env` file to manage configuration and sensitive data. Ensure these variables are correctly set in your environment.

| Variable | Description | Example / Required |
| :--- | :--- | :--- |
| `DATABASE_URL` | Full connection string for the database | `postgres://user:pass@host:port/db` |
| `DB_NAME` | Name of the database | `vendor_db` |
| `DB_USER` | Database access username | `admin` |
| `DB_PASSWORD` | Database access password | `********` |
| `DB_HOST` | Database host address | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `DB_CONN_MAX_AGE` | Maximum lifetime of a database connection | `600` |
| `DB_SSL` | Enable/Disable SSL for DB connection | `True/False` |

---

## 🔑 API Keys Setup

### Database Integration
Vendorapp requires a connected SQL database to function. Follow these steps to configure your data layer:
1.  **Select Provider:** Use a local SQLite instance for development or a PostgreSQL/MySQL provider for production.
2.  **Configure `.env`:** Fill in the `DB_` variables listed in the [Environment Variables](#-environment-variables) section.
3.  **Connectivity:** Ensure `DB_SSL` is set to `True` if your provider requires encrypted connections.

---

## 🚀 Getting Started

### Prerequisites
*   **Python 3.x** installed on your system.
*   **pip** (Python package manager).

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/shankars2006/Vendorapp.git
    cd Vendorapp
    ```

2.  **Set Up Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment:**
    Create a `.env` file in the root directory and add the verified environment variables provided above.

5.  **Initialize Database:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Create Superuser (Admin):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```
    Access the application at `http://127.0.0.1:8000`.

---

## 🔧 Usage

### For Vendors
1.  **Register:** Navigate to `/vendor/register` to create your seller account.
2.  **Wait for Approval:** Administrators must approve your account via the `custom_admin_dashboard`.
3.  **Manage Catalog:** Once approved, log in to your dashboard to add products, set categories, and upload images.
4.  **Fulfill Orders:** Monitor the `vendor_dashboard` for new orders and update statuses to keep customers informed.

### For Customers
1.  **Browse:** Visit the homepage to see the latest products from approved vendors.
2.  **Shop:** Add items to your cart or save them to your wishlist.
3.  **Checkout:** Provide delivery details and simulated card information to finalize your order.
4.  **Track:** Visit your `customer_dashboard` to view current order statuses or initiate returns.

### For Administrators
1.  **Dashboard Access:** Log in via the `/admin` portal.
2.  **Moderate:** Use the `custom_admin_dashboard` to toggle the `is_approved` status for new vendors.
3.  **Review Logic:** Oversee order claims and ensure smooth operation between vendors and buyers.

---

## 🤝 Contributing

We welcome contributions to improve Vendorapp! Your input helps make this project better for everyone.

### How to Contribute

1. **Fork the repository** - Click the 'Fork' button at the top right of this page
2. **Create a feature branch** 
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** - Improve code, documentation, or features
4. **Test thoroughly** - Ensure all functionality works as expected
   ```bash
   python manage.py test
   ```
5. **Commit your changes** - Write clear, descriptive commit messages
   ```bash
   git commit -m 'Add: Implementation of advanced product filtering'
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request** - Submit your changes for review

### Development Guidelines
- ✅ Follow PEP 8 style guides for Python code.
- 📝 Ensure migrations are included for any model changes.
- 🧪 Write unit tests in `sales/tests.py` for new logic.
- 📚 Update the template files in accordance with the existing design patterns.

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for complete details.

### What this means:
- ✅ **Commercial use:** You can use this project commercially.
- ✅ **Modification:** You can modify the code.
- ✅ **Distribution:** You can distribute this software.
- ✅ **Private use:** You can use this project privately.
- ⚠️ **Liability:** The software is provided "as is", without warranty.
- ⚠️ **Trademark:** This license does not grant trademark rights.

---

<p align="center">Made with ❤️ by the Gurushankar P J</p>
<p align="center">
  <a href="#">⬆️ Back to Top</a>
</p>
