 Campus Event Discovery

A desktop app (PyQt5) that helps students discover campus events based on their interests, search events by category, and register for them. Events and registrations are stored in a local SQLite database.

Features

- Login prompt – asks for your name on startup (falls back to "Guest" if left blank).
- Interest-based recommendations – select one or more interests (AI, Robotics, Music, Art, Sports) and get a list of related events, found by traversing an interest → event graph (via depth-first search).
- Category search – type a category keyword to find matching events directly.
- Event details & registration – double-click any recommendation or search result to view full event details (date, venue, organizer) and register with one click.
- Persistent storage – events and registrations are saved in `data.db` (SQLite), auto-created and pre-populated with sample events on first run.

Requirements

- Python 3.7+
- PyQt5 (see `requirements.txt`)

Installation

```bash
pip install -r requirements.txt
```

 Usage

```bash
python app.py
```

On first launch:
1. Enter your name at the login prompt.
2. Select one or more interests in the left panel and click **Recommend** to see suggested events.
3. Or type a category into the search box and click **Search** for a direct lookup.
4. Double-click any result to open its details and register.

Project Structure

```
.
├── app.py             # Main application (UI, graph logic, database access)
├── data.db            # SQLite database (auto-created on first run if missing)
└── requirements.txt   # Python dependencies
```

Database Schema

**events**
| Column     | Type    | Description              |
|------------|---------|---------------------------|
| id         | INTEGER | Primary key               |
| name       | TEXT    | Event name                |
| category   | TEXT    | Event category             |
| date       | TEXT    | Event date                 |
| venue      | TEXT    | Location of the event      |
| organizer  | TEXT    | Hosting club/department    |

registrations
| Column     | Type    | Description                     |
|------------|---------|----------------------------------|
| id         | INTEGER | Primary key                      |
| user       | TEXT    | Name of the registering student  |
| event_id   | INTEGER | Foreign key to `events.id`       |
| timestamp  | TEXT    | UTC registration timestamp (ISO) |

How Recommendations Work

Interests and events are modeled as nodes in an undirected graph (e.g. `AI → AI Club`, `AI → ML Workshop`, `Art → Photography Club`, etc.). When you select interests, the app runs a depth-first search (max depth 5) from those interest nodes to find all reachable event/category nodes, then matches them against the events table to build the recommendation list.

 Notes

- `data.db` is created automatically next to `app.py` if it doesn't already exist, and is pre-seeded with sample events across five categories.
- Registration data accumulates in the `registrations` table each time a user registers for an event.



 Future Improvements

- User authentication system
- Admin dashboard
- Email notifications
- QR Code event registration
- Duplicate registration prevention
- Dynamic recommendation graph
- My Registrations page
- Event editing and deletion

---

 Learning Outcomes

This project demonstrates:

- Graph Data Structures
- Depth-First Search (DFS)
- Object-Oriented Programming (OOP)
- GUI Development using PyQt5
- SQLite Database Integration
- Event-driven Programming
- File Handling
- Modular Python Programming



Happy Coding! 🚀
