# 🎬 Cinema Management System

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success.svg)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)
![Database](https://img.shields.io/badge/database-SQLite-blue)

A full-featured cinema management system built with Python, featuring a client-server architecture with socket communication, SQLite database integration, and a user-friendly GUI interface.

## 🚀 Features

### 🎥 Movie Management
- ✅ Add new movies with details (title, cinema room, dates, tickets, pricing)
- ✅ Update existing movie information
- ✅ Delete movies from the system
- ✅ View all available movies in a dropdown selector

### 🎫 Ticket Operations
- ✅ Calculate ticket prices based on quantity
- ✅ Process ticket purchases with inventory management
- ✅ Automatic ticket availability validation
- ✅ Sales tracking and record keeping

### 🏗️ Architecture
- ✅ Client-Server architecture using TCP sockets
- ✅ SQLite database for persistent data storage
- ✅ JSON-based communication protocol
- ✅ Tkinter GUI for intuitive user interaction

## 📋 Requirements

- Python 3.7+
- Built-in libraries only (no external dependencies required):
  - `tkinter` - GUI framework
  - `sqlite3` - Database operations
  - `socket` - Network communication
  - `json` - Data serialization

## 🛠️ Installation

1. **Clone or download the project files**
   ```bash
   git clone https://github.com/kxngHADES/cinema-server-client-school-project
   cd "cinema-server-client-school-project"
   ```

2. **Ensure Python 3.7+ is installed**
   ```bash
   python --version
   ```

3. **No additional packages required** - uses Python standard library only

## 🚦 Quick Start

### Starting the Server
```bash
python server.py
```
The server will start on `127.0.0.1:65333` by default.

### Launching the Client Application
```bash
python client.py
```

## 💻 Usage Guide

### 🎬 Adding a Movie
1. Fill in the movie details in the form fields
2. Cinema room must be between 1-7 (optional field)
3. Click "Add Movie" button
4. Success/error message will be displayed

### ✏️ Updating a Movie
1. Select a movie from the dropdown
2. Modify the desired fields
3. Click "Update Movie" button

### 🗑️ Deleting a Movie
1. Select a movie from the dropdown
2. Click "Delete Movie" button
3. Confirm the action

### 🎫 Purchasing Tickets
1. Select a movie from the dropdown
2. Enter the number of tickets desired
3. Click "Calculate Price" to see the total
4. Click "Purchase Tickets" to complete the transaction

## 🗄️ Database Schema

### Movies Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| title | TEXT | NOT NULL |
| cinema_room | INTEGER | UNIQUE, CHECK (1-7) |
| release_date | TEXT | NOT NULL |
| end_date | TEXT | NOT NULL |
| tickets | INTEGER | NOT NULL |
| ticket_price | REAL | NOT NULL |

### Sales Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| movie_id | INTEGER | NOT NULL, FOREIGN KEY |
| number_of_tickets | INTEGER | NOT NULL |
| total | REAL | NOT NULL |

## 🔌 API Endpoints

The server handles JSON requests with the following actions:

- `get_movies` - Retrieve all movies
- `add_movies` - Add a new movie
- `update_movie` - Update existing movie
- `delete_movies` - Delete a movie by ID
- `calculate_price` - Calculate total price for tickets
- `purchase` - Process ticket purchase

## 📁 Project Structure

```
📦 Cinema Management System
├── 📄 server.py          # Server-side application
├── 📄 client.py          # Client-side GUI application
├── 📄 cinema.db          # SQLite database (auto-generated)
└── 📄 README.md          # Project documentation
```

## 🐛 Error Handling

The system includes comprehensive error handling for:
- Database connection issues
- Invalid input validation
- Network communication errors
- Insufficient ticket availability
- Duplicate cinema room assignments

## 🎯 Technical Details

- **Communication Protocol**: TCP Socket with JSON messages
- **Database**: SQLite with ACID compliance
- **GUI Framework**: Tkinter with ttk widgets
- **Architecture Pattern**: Client-Server model
- **Data Validation**: Server-side validation with client-side feedback

## 🤝 Contributing

This is a school project for **ITAPA2-12 Project 2 Pretoria MD.2022.G4C7J5**. 

If you'd like to suggest improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Author info
- **Ndaedzo Mudau**

## 🙏 Acknowledgments

- Course: ITAPA2-12 Project 2
- Institution: Eduvos Pretoria
- Year: 2025

---

<div align="center">
  <strong>🎬 NewLine Cinema Management System</strong><br>
  Built with ❤️ for efficient cinema operations
</div>
