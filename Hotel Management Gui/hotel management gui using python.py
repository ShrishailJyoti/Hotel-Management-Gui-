import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
from datetime import date, timedelta

# =========================================================
# HOTEL MANAGEMENT SYSTEM
# Python 3.9 Compatible
# =========================================================

DB_NAME = "hotel_management_v2.db"

conn = sqlite3.connect(DB_NAME)
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

# =========================================================
# DATABASE TABLES
# =========================================================

cur.executescript("""
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_no TEXT UNIQUE NOT NULL,
    room_type TEXT NOT NULL,
    price REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'Available'
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    checkin TEXT NOT NULL,
    checkout TEXT NOT NULL,
    total REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'Confirmed',
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(room_id) REFERENCES rooms(id)
);
""")

conn.commit()


# =========================================================
# SAMPLE DATA
# =========================================================

def load_sample_data():

    cur.execute("SELECT COUNT(*) FROM rooms")

    if cur.fetchone()[0] > 0:
        return

    random.seed(42)

    room_types = [
        ("Standard", 1800),
        ("Deluxe", 2800),
        ("Executive", 4000),
        ("Suite", 6000),
        ("Presidential", 10000)
    ]

    # 50 ROOMS

    for i in range(1, 51):

        room_type, price = random.choice(room_types)

        cur.execute("""
            INSERT INTO rooms
            (room_no, room_type, price, status)
            VALUES (?, ?, ?, ?)
        """, (
            str(100 + i),
            room_type,
            price,
            "Available"
        ))

    # 50 FICTIONAL INDIAN CUSTOMERS

    customers = [
        ("Rahul Sharma", "9000000001", "rahul@example.com"),
        ("Priya Reddy", "9000000002", "priya@example.com"),
        ("Arjun Kumar", "9000000003", "arjun@example.com"),
        ("Sneha Patil", "9000000004", "sneha@example.com"),
        ("Aditya Verma", "9000000005", "aditya@example.com"),
        ("Kiran Desai", "9000000006", "kiran@example.com"),
        ("Ananya Rao", "9000000007", "ananya@example.com"),
        ("Vikram Singh", "9000000008", "vikram@example.com"),
        ("Pooja Kulkarni", "9000000009", "pooja@example.com"),
        ("Rohit Mehta", "9000000010", "rohit@example.com"),
        ("Neha Joshi", "9000000011", "neha@example.com"),
        ("Amit Patel", "9000000012", "amit@example.com"),
        ("Divya Nair", "9000000013", "divya@example.com"),
        ("Sandeep Gowda", "9000000014", "sandeep@example.com"),
        ("Meera Iyer", "9000000015", "meera@example.com"),
        ("Akash Yadav", "9000000016", "akash@example.com"),
        ("Riya Malhotra", "9000000017", "riya@example.com"),
        ("Manoj Kumar", "9000000018", "manoj@example.com"),
        ("Kavya Shetty", "9000000019", "kavya@example.com"),
        ("Varun Reddy", "9000000020", "varun@example.com"),
        ("Nikhil Jain", "9000000021", "nikhil@example.com"),
        ("Aishwarya Rao", "9000000022", "aishwarya@example.com"),
        ("Sanjay Mishra", "9000000023", "sanjay@example.com"),
        ("Deepika Shah", "9000000024", "deepika@example.com"),
        ("Pranav Joshi", "9000000025", "pranav@example.com"),
        ("Swati Kulkarni", "9000000026", "swati@example.com"),
        ("Ramesh Bhat", "9000000027", "ramesh@example.com"),
        ("Tanvi Deshmukh", "9000000028", "tanvi@example.com"),
        ("Harish Naidu", "9000000029", "harish@example.com"),
        ("Nisha Thomas", "9000000030", "nisha@example.com"),
        ("Abhishek Sinha", "9000000031", "abhishek@example.com"),
        ("Shreya Kapoor", "9000000032", "shreya@example.com"),
        ("Gaurav Patil", "9000000033", "gaurav@example.com"),
        ("Anjali Menon", "9000000034", "anjali@example.com"),
        ("Karthik Rao", "9000000035", "karthik@example.com"),
        ("Madhuri Pawar", "9000000036", "madhuri@example.com"),
        ("Suraj Chavan", "9000000037", "suraj@example.com"),
        ("Ishita Bose", "9000000038", "ishita@example.com"),
        ("Prakash Hegde", "9000000039", "prakash@example.com"),
        ("Nandini Rao", "9000000040", "nandini@example.com"),
        ("Ajay Kulkarni", "9000000041", "ajay@example.com"),
        ("Simran Kaur", "9000000042", "simran@example.com"),
        ("Rohini Das", "9000000043", "rohini@example.com"),
        ("Vivek Anand", "9000000044", "vivek@example.com"),
        ("Pallavi Naik", "9000000045", "pallavi@example.com"),
        ("Suresh Babu", "9000000046", "suresh@example.com"),
        ("Lavanya Reddy", "9000000047", "lavanya@example.com"),
        ("Mohit Agarwal", "9000000048", "mohit@example.com"),
        ("Aarav Shah", "9000000049", "aarav@example.com"),
        ("Shalini Nair", "9000000050", "shalini@example.com")
    ]

    cur.executemany("""
        INSERT INTO customers(name, phone, email)
        VALUES (?, ?, ?)
    """, customers)

    # 30 SAMPLE BOOKINGS

    today = date.today()

    for i in range(1, 31):

        checkin = today + timedelta(
            days=random.randint(-15, 15)
        )

        nights = random.randint(1, 5)

        checkout = checkin + timedelta(days=nights)

        cur.execute(
            "SELECT price FROM rooms WHERE id=?",
            (i,)
        )

        price = cur.fetchone()[0]

        total = price * nights

        if checkout <= today:
            status = "Completed"

        elif checkin <= today < checkout:
            status = "Checked In"

        else:
            status = "Confirmed"

        cur.execute("""
            INSERT INTO bookings
            (customer_id, room_id, checkin,
             checkout, total, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            i,
            i,
            checkin.isoformat(),
            checkout.isoformat(),
            total,
            status
        ))

    conn.commit()


load_sample_data()


# =========================================================
# MAIN APPLICATION
# =========================================================

class HotelManagement:

    def __init__(self, root):

        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1450x850")
        self.root.minsize(1100, 700)
        self.root.configure(bg="#101827")

        self.navy = "#101827"
        self.sidebar_color = "#0B1423"
        self.card = "#1B2940"
        self.gold = "#D4AF37"
        self.white = "#FFFFFF"
        self.muted = "#AAB7C8"

        self.setup_style()
        self.create_layout()
        self.show_dashboard()

    # =====================================================
    # STYLE
    # =====================================================

    def setup_style(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self.card,
            foreground="white",
            fieldbackground=self.card,
            rowheight=36,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=self.gold,
            foreground=self.navy,
            font=("Arial", 10, "bold"),
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#526783")],
            foreground=[("selected", "white")]
        )

    # =====================================================
    # LAYOUT
    # =====================================================

    def create_layout(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=self.sidebar_color,
            width=245
        )

        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="HOTEL",
            bg=self.sidebar_color,
            fg=self.gold,
            font=("Arial", 30, "bold")
        ).pack(pady=(35, 5))

        tk.Label(
            self.sidebar,
            text="MANAGEMENT SYSTEM",
            bg=self.sidebar_color,
            fg=self.muted,
            font=("Arial", 9, "bold")
        ).pack(pady=(0, 40))

        navigation = [
            ("⌂   Dashboard", self.show_dashboard),
            ("▣   Room Management",
             lambda: self.show_manager("rooms")),
            ("♙   Customer Management",
             lambda: self.show_manager("customers")),
            ("▤   Booking Management",
             lambda: self.show_manager("bookings"))
        ]

        for title, command in navigation:

            tk.Button(
                self.sidebar,
                text=title,
                command=command,
                bg=self.sidebar_color,
                fg=self.white,
                activebackground=self.gold,
                activeforeground=self.navy,
                relief="flat",
                anchor="w",
                padx=20,
                pady=16,
                font=("Arial", 11, "bold"),
                cursor="hand2"
            ).pack(fill="x", padx=10, pady=4)

        tk.Label(
            self.sidebar,
            text="HOTEL ADMIN PORTAL\nVERSION 2.0",
            bg=self.sidebar_color,
            fg="#718096",
            font=("Arial", 9)
        ).pack(side="bottom", pady=25)

        self.main = tk.Frame(
            self.root,
            bg=self.navy
        )

        self.main.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.header = tk.Frame(
            self.main,
            bg=self.navy,
            height=85
        )

        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.page_title = tk.Label(
            self.header,
            text="DASHBOARD",
            bg=self.navy,
            fg=self.white,
            font=("Arial", 21, "bold")
        )

        self.page_title.pack(
            side="left",
            padx=30,
            pady=25
        )

        tk.Label(
            self.header,
            text="HOTEL MANAGEMENT PORTAL",
            bg=self.navy,
            fg=self.gold,
            font=("Arial", 10, "bold")
        ).pack(side="right", padx=30)

        self.content = tk.Frame(
            self.main,
            bg=self.navy
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

    # =====================================================
    # CLEAR CONTENT
    # =====================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # =====================================================
    # DASHBOARD
    # =====================================================

    def show_dashboard(self):

        self.clear_content()

        self.page_title.config(
            text="DASHBOARD OVERVIEW"
        )

        cur.execute("SELECT COUNT(*) FROM rooms")
        rooms = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM customers")
        customers = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM bookings")
        bookings = cur.fetchone()[0]

        cur.execute("""
            SELECT COALESCE(SUM(total), 0)
            FROM bookings
            WHERE status != 'Cancelled'
        """)

        revenue = cur.fetchone()[0]

        stats = [
            ("TOTAL ROOMS", rooms, "▣"),
            ("TOTAL CUSTOMERS", customers, "♙"),
            ("TOTAL BOOKINGS", bookings, "▤"),
            ("TOTAL REVENUE", "₹{:,.0f}".format(revenue), "₹")
        ]

        cards = tk.Frame(
            self.content,
            bg=self.navy
        )

        cards.pack(fill="x", pady=20)

        for title, value, icon in stats:

            card = tk.Frame(
                cards,
                bg=self.card,
                height=145
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=8
            )

            card.pack_propagate(False)

            tk.Label(
                card,
                text=icon,
                bg=self.card,
                fg=self.gold,
                font=("Arial", 25, "bold")
            ).pack(anchor="w", padx=20, pady=(12, 0))

            tk.Label(
                card,
                text=title,
                bg=self.card,
                fg=self.muted,
                font=("Arial", 10, "bold")
            ).pack(anchor="w", padx=20)

            tk.Label(
                card,
                text=str(value),
                bg=self.card,
                fg=self.white,
                font=("Arial", 22, "bold")
            ).pack(anchor="w", padx=20, pady=5)

        # RECENT BOOKINGS

        section = tk.Frame(
            self.content,
            bg=self.card
        )

        section.pack(
            fill="both",
            expand=True,
            pady=15
        )

        tk.Label(
            section,
            text="  RECENT HOTEL BOOKINGS",
            bg=self.card,
            fg=self.gold,
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=15)

        columns = (
            "ID", "CUSTOMER", "ROOM",
            "CHECK-IN", "CHECK-OUT", "AMOUNT", "STATUS"
        )

        tree = ttk.Treeview(
            section,
            columns=columns,
            show="headings"
        )

        for col in columns:

            tree.heading(col, text=col)

            tree.column(
                col,
                width=130,
                anchor="center"
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        cur.execute("""
            SELECT b.id, c.name, r.room_no,
                   b.checkin, b.checkout,
                   b.total, b.status
            FROM bookings b
            JOIN customers c ON b.customer_id=c.id
            JOIN rooms r ON b.room_id=r.id
            ORDER BY b.id DESC
            LIMIT 20
        """)

        for row in cur.fetchall():
            tree.insert("", "end", values=row)

    # =====================================================
    # MANAGEMENT PAGES
    # =====================================================

    def show_manager(self, table):

        self.clear_content()

        titles = {
            "rooms": "ROOM MANAGEMENT",
            "customers": "CUSTOMER MANAGEMENT",
            "bookings": "BOOKING MANAGEMENT"
        }

        self.page_title.config(text=titles[table])

        top = tk.Frame(
            self.content,
            bg=self.navy
        )

        top.pack(fill="x", pady=10)

        search_var = tk.StringVar()

        search_entry = tk.Entry(
            top,
            textvariable=search_var,
            font=("Arial", 12),
            bg=self.card,
            fg=self.white,
            insertbackground="white",
            relief="flat",
            width=32
        )

        search_entry.pack(side="left", ipady=9)

        columns = {
            "rooms": (
                "ID", "ROOM NO", "ROOM TYPE", "PRICE", "STATUS"
            ),

            "customers": (
                "ID", "CUSTOMER NAME", "PHONE", "EMAIL"
            ),

            "bookings": (
                "ID", "CUSTOMER", "ROOM", "CHECK-IN",
                "CHECK-OUT", "TOTAL", "STATUS"
            )
        }

        tree = ttk.Treeview(
            self.content,
            columns=columns[table],
            show="headings"
        )

        for col in columns[table]:

            tree.heading(col, text=col)

            tree.column(
                col,
                width=145,
                anchor="center"
            )

        tree.pack(
            fill="both",
            expand=True,
            pady=15
        )

        # REFRESH

        def refresh():

            tree.delete(*tree.get_children())

            query = search_var.get().strip()

            if table == "rooms":

                cur.execute("""
                    SELECT id, room_no, room_type, price, status
                    FROM rooms
                    WHERE room_no LIKE ? OR room_type LIKE ?
                    ORDER BY id DESC
                """, (
                    "%" + query + "%",
                    "%" + query + "%"
                ))

            elif table == "customers":

                cur.execute("""
                    SELECT id, name, phone, email
                    FROM customers
                    WHERE name LIKE ?
                    OR phone LIKE ?
                    OR email LIKE ?
                    ORDER BY id DESC
                """, (
                    "%" + query + "%",
                    "%" + query + "%",
                    "%" + query + "%"
                ))

            else:

                cur.execute("""
                    SELECT b.id, c.name, r.room_no,
                           b.checkin, b.checkout,
                           b.total, b.status

                    FROM bookings b

                    JOIN customers c
                    ON b.customer_id=c.id

                    JOIN rooms r
                    ON b.room_id=r.id

                    WHERE c.name LIKE ?
                    OR r.room_no LIKE ?

                    ORDER BY b.id DESC
                """, (
                    "%" + query + "%",
                    "%" + query + "%"
                ))

            for row in cur.fetchall():
                tree.insert("", "end", values=row)

        tk.Button(
            top,
            text="SEARCH",
            command=refresh,
            bg=self.gold,
            fg=self.navy,
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=18,
            pady=9
        ).pack(side="left", padx=10)

        # SELECT

        def get_selected():

            selected = tree.selection()

            if not selected:

                messagebox.showwarning(
                    "Selection Required",
                    "Please select a record first."
                )

                return None

            return tree.item(selected[0])["values"]

        # =================================================
        # ADD / EDIT FORM
        # =================================================

        def open_form(edit=False):

            selected = None

            if edit:

                selected = get_selected()

                if selected is None:
                    return

            if edit and table == "bookings":

                cur.execute("""
                    SELECT id, customer_id, room_id,
                           checkin, checkout, total, status
                    FROM bookings
                    WHERE id=?
                """, (selected[0],))

                selected = cur.fetchone()

            form = tk.Toplevel(self.root)

            form.title(
                "Edit Record" if edit else "Add New Record"
            )

            form.geometry("460x650")
            form.configure(bg=self.card)
            form.resizable(False, False)
            form.grab_set()

            tk.Label(
                form,
                text="HOTEL RECORD",
                bg=self.card,
                fg=self.gold,
                font=("Arial", 21, "bold")
            ).pack(pady=20)

            entries = {}

            if table == "rooms":

                fields = [
                    ("Room Number", "room_no"),
                    ("Room Type", "room_type"),
                    ("Price Per Night", "price"),
                    ("Status", "status")
                ]

            elif table == "customers":

                fields = [
                    ("Customer Name", "name"),
                    ("Phone Number", "phone"),
                    ("Email Address", "email")
                ]

            else:

                fields = [
                    ("Customer", "customer_id"),
                    ("Room", "room_id"),
                    ("Check-in Date", "checkin"),
                    ("Check-out Date", "checkout"),
                    ("Booking Status", "status")
                ]

            for index, (label, field) in enumerate(fields):

                tk.Label(
                    form,
                    text=label,
                    bg=self.card,
                    fg=self.white,
                    font=("Arial", 10, "bold")
                ).pack(
                    anchor="w",
                    padx=35,
                    pady=(9, 3)
                )

                # CUSTOMER DROPDOWN

                if field == "customer_id":

                    cur.execute("""
                        SELECT id, name FROM customers
                        ORDER BY name
                    """)

                    records = cur.fetchall()

                    values = [
                        str(r[0]) + " - " + r[1]
                        for r in records
                    ]

                    entry = ttk.Combobox(
                        form,
                        values=values,
                        state="readonly",
                        font=("Arial", 11)
                    )

                    if edit:

                        for value in values:

                            if value.startswith(
                                str(selected[1]) + " -"
                            ):
                                entry.set(value)
                                break

                    elif values:
                        entry.current(0)

                # ROOM DROPDOWN

                elif field == "room_id":

                    cur.execute("""
                        SELECT id, room_no, room_type
                        FROM rooms
                        WHERE status='Available'
                        ORDER BY room_no
                    """)

                    records = cur.fetchall()

                    # Include currently selected room while editing

                    if edit:

                        cur.execute("""
                            SELECT id, room_no, room_type
                            FROM rooms WHERE id=?
                        """, (selected[2],))

                        current_room = cur.fetchone()

                        if current_room and current_room not in records:
                            records.append(current_room)

                    values = [
                        str(r[0]) + " - Room " + str(r[1])
                        + " (" + r[2] + ")"
                        for r in records
                    ]

                    entry = ttk.Combobox(
                        form,
                        values=values,
                        state="readonly",
                        font=("Arial", 11)
                    )

                    if edit:

                        for value in values:

                            if value.startswith(
                                str(selected[2]) + " -"
                            ):
                                entry.set(value)
                                break

                    elif values:
                        entry.current(0)

                # ROOM TYPE

                elif field == "room_type":

                    entry = ttk.Combobox(
                        form,
                        values=[
                            "Standard",
                            "Deluxe",
                            "Executive",
                            "Suite",
                            "Presidential"
                        ],
                        state="readonly",
                        font=("Arial", 11)
                    )

                    if edit:
                        entry.set(selected[index + 1])
                    else:
                        entry.current(0)

                # STATUS

                elif field == "status":

                    if table == "rooms":

                        values = [
                            "Available",
                            "Maintenance"
                        ]

                        value = selected[4] if edit else "Available"

                    else:

                        values = [
                            "Confirmed",
                            "Checked In",
                            "Completed",
                            "Cancelled"
                        ]

                        value = selected[6] if edit else "Confirmed"

                    entry = ttk.Combobox(
                        form,
                        values=values,
                        state="readonly",
                        font=("Arial", 11)
                    )

                    entry.set(value)

                # NORMAL ENTRY

                else:

                    entry = tk.Entry(
                        form,
                        font=("Arial", 11),
                        bg="#263750",
                        fg="white",
                        insertbackground="white",
                        relief="flat"
                    )

                    if edit:

                        if table == "rooms":
                            value = selected[index + 1]

                        elif table == "customers":
                            value = selected[index + 1]

                        else:
                            value = selected[index + 3]

                        entry.insert(0, str(value))

                    else:

                        if field == "checkin":
                            entry.insert(
                                0,
                                date.today().isoformat()
                            )

                        elif field == "checkout":
                            entry.insert(
                                0,
                                (
                                    date.today()
                                    + timedelta(days=1)
                                ).isoformat()
                            )

                entry.pack(
                    fill="x",
                    padx=35,
                    ipady=7
                )

                entries[field] = entry

            # =================================================
            # SAVE
            # =================================================

            def save():

                data = {
                    key: entry.get().strip()
                    for key, entry in entries.items()
                }

                if any(not value for value in data.values()):

                    messagebox.showerror(
                        "Missing Information",
                        "Please fill all fields."
                    )

                    return

                try:

                    # ROOMS

                    if table == "rooms":

                        price = float(data["price"])

                        if price <= 0:
                            raise ValueError(
                                "Price must be greater than zero."
                            )

                        if edit:

                            cur.execute("""
                                UPDATE rooms

                                SET room_no=?,
                                    room_type=?,
                                    price=?,
                                    status=?

                                WHERE id=?
                            """, (
                                data["room_no"],
                                data["room_type"],
                                price,
                                data["status"],
                                selected[0]
                            ))

                        else:

                            cur.execute("""
                                INSERT INTO rooms
                                (room_no, room_type, price, status)
                                VALUES (?, ?, ?, ?)
                            """, (
                                data["room_no"],
                                data["room_type"],
                                price,
                                data["status"]
                            ))

                    # CUSTOMERS

                    elif table == "customers":

                        if len(data["phone"]) < 10:
                            raise ValueError(
                                "Enter a valid phone number."
                            )

                        if edit:

                            cur.execute("""
                                UPDATE customers
                                SET name=?, phone=?, email=?
                                WHERE id=?
                            """, (
                                data["name"],
                                data["phone"],
                                data["email"],
                                selected[0]
                            ))

                        else:

                            cur.execute("""
                                INSERT INTO customers
                                (name, phone, email)
                                VALUES (?, ?, ?)
                            """, (
                                data["name"],
                                data["phone"],
                                data["email"]
                            ))

                    # BOOKINGS

                    elif table == "bookings":

                        customer_id = int(
                            data["customer_id"].split(" - ")[0]
                        )

                        room_id = int(
                            data["room_id"].split(" - ")[0]
                        )

                        checkin = date.fromisoformat(
                            data["checkin"]
                        )

                        checkout = date.fromisoformat(
                            data["checkout"]
                        )

                        nights = (checkout - checkin).days

                        if nights <= 0:
                            raise ValueError(
                                "Check-out must be after check-in."
                            )

                        cur.execute("""
                            SELECT price, status
                            FROM rooms
                            WHERE id=?
                        """, (room_id,))

                        room = cur.fetchone()

                        if not room:
                            raise ValueError(
                                "Room does not exist."
                            )

                        if room[1] == "Maintenance":
                            raise ValueError(
                                "Room is under maintenance."
                            )

                        # Prevent overlapping bookings

                        booking_id = selected[0] if edit else -1

                        if data["status"] in (
                            "Confirmed",
                            "Checked In"
                        ):

                            cur.execute("""
                                SELECT id FROM bookings

                                WHERE room_id=?
                                AND status IN ('Confirmed', 'Checked In')
                                AND id != ?
                                AND checkin < ?
                                AND checkout > ?
                            """, (
                                room_id,
                                booking_id,
                                checkout.isoformat(),
                                checkin.isoformat()
                            ))

                            if cur.fetchone():
                                raise ValueError(
                                    "This room is already booked "
                                    "for these dates."
                                )

                        total = nights * room[0]

                        if edit:

                            cur.execute("""
                                UPDATE bookings

                                SET customer_id=?,
                                    room_id=?,
                                    checkin=?,
                                    checkout=?,
                                    total=?,
                                    status=?

                                WHERE id=?
                            """, (
                                customer_id,
                                room_id,
                                checkin.isoformat(),
                                checkout.isoformat(),
                                total,
                                data["status"],
                                selected[0]
                            ))

                        else:

                            cur.execute("""
                                INSERT INTO bookings
                                (customer_id, room_id, checkin,
                                 checkout, total, status)

                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                customer_id,
                                room_id,
                                checkin.isoformat(),
                                checkout.isoformat(),
                                total,
                                data["status"]
                            ))

                    conn.commit()

                    form.destroy()

                    refresh()

                    messagebox.showinfo(
                        "Success",
                        "Record saved successfully!"
                    )

                except sqlite3.IntegrityError:

                    conn.rollback()

                    messagebox.showerror(
                        "Database Error",
                        "Duplicate room number or invalid record."
                    )

                except (ValueError, TypeError) as error:

                    conn.rollback()

                    messagebox.showerror(
                        "Invalid Information",
                        str(error)
                    )

            tk.Button(
                form,
                text="SAVE RECORD",
                command=save,
                bg=self.gold,
                fg=self.navy,
                font=("Arial", 11, "bold"),
                relief="flat",
                pady=13,
                cursor="hand2"
            ).pack(
                fill="x",
                padx=35,
                pady=25
            )

        # =================================================
        # DELETE
        # =================================================

        def delete():

            selected = get_selected()

            if selected is None:
                return

            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this record?"
            )

            if not confirm:
                return

            try:

                cur.execute(
                    "DELETE FROM " + table + " WHERE id=?",
                    (selected[0],)
                )

                conn.commit()

                refresh()

                messagebox.showinfo(
                    "Success",
                    "Record deleted successfully."
                )

            except sqlite3.IntegrityError:

                conn.rollback()

                messagebox.showerror(
                    "Cannot Delete",
                    "This record is connected to another record. "
                    "Delete related bookings first."
                )

        # =================================================
        # ACTION BUTTONS
        # =================================================

        actions = tk.Frame(
            self.content,
            bg=self.navy
        )

        actions.pack(fill="x", pady=10)

        buttons = [
            ("+ ADD NEW", lambda: open_form(False)),
            ("EDIT SELECTED", lambda: open_form(True)),
            ("DELETE SELECTED", delete)
        ]

        for label, command in buttons:

            tk.Button(
                actions,
                text=label,
                command=command,
                bg=self.gold if label == "+ ADD NEW" else self.card,
                fg=self.navy if label == "+ ADD NEW" else self.white,
                font=("Arial", 10, "bold"),
                relief="flat",
                padx=20,
                pady=12,
                cursor="hand2"
            ).pack(side="left", padx=7)

        refresh()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = HotelManagement(root)

    root.mainloop()
