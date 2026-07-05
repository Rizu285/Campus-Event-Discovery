from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QAbstractItemView, QLineEdit, QDialog, QTextEdit, QFormLayout, QInputDialog
import sys
import sqlite3
import os
from datetime import datetime


class Graph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v):
        self.adj.setdefault(u, []).append(v)
        self.adj.setdefault(v, []).append(u)

    def dfs(self, starts, max_depth=10):
        visited = set()
        stack = [(s, 0) for s in starts]
        while stack:
            node, depth = stack.pop()
            if node in visited or depth > max_depth:
                continue
            visited.add(node)
            for nb in self.adj.get(node, []):
                if nb not in visited:
                    stack.append((nb, depth + 1))
        return visited


def build_sample_graph():
    g = Graph()
    edges = [
        ("AI", "AI Club"), ("AI", "ML Workshop"), ("AI", "Robotics Club"),
        ("Robotics", "Robotics Club"), ("Robotics", "Engineering Fair"),
        ("Music", "Jazz Club"), ("Music", "Open Mic"), ("Art", "Art Club"),
        ("Sports", "Soccer Club"), ("Sports", "Basketball Game"),
        ("AI", "Data Science Meetup"), ("Art", "Photography Club"),
        ("Photography Club", "Art Club"), ("Open Mic", "Jazz Club"),
        ("ML Workshop", "Data Science Meetup")
    ]
    for u, v in edges:
        g.add_edge(u, v)
    return g


DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")


def init_db():
    first = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        date TEXT,
        venue TEXT,
        organizer TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY,
        user TEXT,
        event_id INTEGER,
        timestamp TEXT
    )
    """)
    conn.commit()

    if first:
        sample = [
            ("AI Club", "AI", "2026-09-12", "Room 101", "CS Dept"),
            ("ML Workshop", "AI", "2026-09-20", "Lab A", "Data Club"),
            ("Robotics Club", "Robotics", "2026-10-01", "Workshop", "Robotics Dept"),
            ("Engineering Fair", "Robotics", "2026-11-05", "Hall", "Eng Soc"),
            ("Jazz Club", "Music", "2026-09-30", "Auditorium", "Music Soc"),
            ("Open Mic", "Music", "2026-10-10", "Cafe", "Arts"),
            ("Art Club", "Art", "2026-09-15", "Studio", "Art Dept"),
            ("Photography Club", "Art", "2026-10-22", "Gallery", "Photo Soc"),
            ("Soccer Club", "Sports", "2026-09-18", "Field", "Sports Dept"),
            ("Basketball Game", "Sports", "2026-09-25", "Gym", "Athletics"),
            ("Data Science Meetup", "AI", "2026-10-05", "Room 202", "DS Club")
        ]
        cur.executemany("INSERT INTO events (name,category,date,venue,organizer) VALUES (?,?,?,?,?)", sample)
        conn.commit()
    conn.close()


def load_events():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, date, venue, organizer FROM events")
    rows = cur.fetchall()
    conn.close()
    events = []
    for r in rows:
        events.append({
            "id": r[0], "name": r[1], "category": r[2], "date": r[3], "venue": r[4], "organizer": r[5]
        })
    return events


def register_for_event(user, event_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO registrations (user, event_id, timestamp) VALUES (?,?,?)", (user, event_id, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()


class EventDialog(QDialog):
    def __init__(self, parent, event, user):
        super().__init__(parent)
        self.setWindowTitle(event["name"])
        self.event = event
        self.user = user
        self.setStyleSheet("""
            QDialog {
                background-color: #111111;
                color: #f0f0f0;
            }
            QLabel {
                color: #f0f0f0;
            }
            QPushButton {
                color: #f0f0f0;
                background-color: #2b2b2b;
                border: 1px solid #555555;
                padding: 6px 10px;
            }
        """)
        layout = QVBoxLayout()
        form = QFormLayout()
        form.addRow("Name:", QLabel(event["name"]))
        form.addRow("Category:", QLabel(event["category"]))
        form.addRow("Date:", QLabel(event["date"]))
        form.addRow("Venue:", QLabel(event["venue"]))
        form.addRow("Organizer:", QLabel(event["organizer"]))
        layout.addLayout(form)
        btn = QPushButton("Register")
        btn.clicked.connect(self.on_register)
        layout.addWidget(btn)
        self.setLayout(layout)

    def on_register(self):
        register_for_event(self.user, self.event["id"])
        QMessageBox.information(self, "Registered", f"Registered {self.user} for {self.event['name']}")
        self.accept()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Campus Event Discovery")
        self.setStyleSheet("""
            QWidget {
                background-color: #111111;
                color: #f0f0f0;
            }
            QLabel {
                color: #f0f0f0;
                font-weight: 500;
            }
            QLineEdit, QListWidget {
                background-color: #1b1b1b;
                color: #f0f0f0;
                border: 1px solid #555555;
            }
            QPushButton {
                color: #f0f0f0;
                background-color: #2b2b2b;
                border: 1px solid #555555;
                padding: 6px 10px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QListWidget::item:selected {
                background-color: #005f87;
                color: #ffffff;
            }
        """)
        init_db()
        self.events = load_events()
        self.graph = build_sample_graph()
        self.user = self.ask_username()
        self.init_ui()

    def ask_username(self):
        name, ok = QInputDialog.getText(self, "Student Login", "Enter your name:")
        if not ok or not name.strip():
            return "Guest"
        return name.strip()

    def init_ui(self):
        left = QVBoxLayout()
        left.addWidget(QLabel(f"User: {self.user}"))
        left.addWidget(QLabel("Select interests"))
        self.interestList = QListWidget()
        self.interestList.setSelectionMode(QAbstractItemView.MultiSelection)
        interests = ["AI", "Robotics", "Music", "Art", "Sports"]
        for i in interests:
            self.interestList.addItem(i)
        left.addWidget(self.interestList)
        self.recommendBtn = QPushButton("Recommend")
        self.recommendBtn.clicked.connect(self.on_recommend)
        left.addWidget(self.recommendBtn)

        # Search area
        left.addWidget(QLabel("Search by category"))
        self.searchInput = QLineEdit()
        left.addWidget(self.searchInput)
        self.searchBtn = QPushButton("Search")
        self.searchBtn.clicked.connect(self.on_search)
        left.addWidget(self.searchBtn)

        right = QVBoxLayout()
        right.addWidget(QLabel("Recommendations (double-click for details)"))
        self.recoList = QListWidget()
        self.recoList.itemDoubleClicked.connect(self.on_item_open)
        right.addWidget(self.recoList)

        right.addWidget(QLabel("Search results (double-click for details)"))
        self.searchList = QListWidget()
        self.searchList.itemDoubleClicked.connect(self.on_item_open)
        right.addWidget(self.searchList)

        layout = QHBoxLayout()
        layout.addLayout(left)
        layout.addLayout(right)
        self.setLayout(layout)
        self.resize(800, 400)

    def on_recommend(self):
        items = self.interestList.selectedItems()
        if not items:
            QMessageBox.information(self, "No selection", "Please select at least one interest.")
            return
        starts = [it.text() for it in items]
        visited = self.graph.dfs(starts, max_depth=5)
        # match visited nodes to event names
        matches = [e for e in self.events if e["name"] in visited or e["category"] in visited]
        self.recoList.clear()
        if matches:
            for m in matches:
                self.recoList.addItem(f"{m['id']}: {m['name']} ({m['category']})")
        else:
            self.recoList.addItem("No recommendations found.")

    def on_search(self):
        q = self.searchInput.text().strip()
        self.searchList.clear()
        if not q:
            self.searchList.addItem("Enter a category to search.")
            return
        matches = [e for e in self.events if q.lower() in e["category"].lower()]
        if matches:
            for m in matches:
                self.searchList.addItem(f"{m['id']}: {m['name']} ({m['category']})")
        else:
            self.searchList.addItem("No events found for that category.")

    def on_item_open(self, item):
        text = item.text()
        if text.startswith("No ") or text.startswith("Enter "):
            return
        event_id = int(text.split(":", 1)[0])
        ev = next((e for e in self.events if e["id"] == event_id), None)
        if not ev:
            QMessageBox.warning(self, "Not found", "Event not found.")
            return
        d = EventDialog(self, ev, self.user)
        if d.exec_():
            # reload registrations or optionally update UI
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
