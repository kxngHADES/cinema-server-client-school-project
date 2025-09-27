#imports
import json
import socket
import sqlite3

class MovieServer:
    def __init__(self, host = '127.0.0.1', port=65333):
        self.host = host
        self.port = port
        self.db =  sqlite3.connect('cinema.db')
        self.create_tables()

    def create_tables(self):
        try:
            #create the movies table
            query = """
                CREATE TABLE IF NOT EXISTS movies(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                cinema_room INTEGER UNIQUE CHECK (cinema_room BETWEEN 1 and 7),
                release_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                tickets INTEGER NOT NULL,
                ticket_price REAL NOT NULL
                )
            """
            #create the sales table
            query2 = """
                CREATE TABLE IF NOT EXISTS sales(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER NOT NULL,
                number_of_tickets INTEGER NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (movie_id) REFERENCES movies(id)
                )
            """
            #execute the queries
            self.db.execute(query)
            self.db.execute(query2)

            #commit the changes
            self.db.commit()
            
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def handle_requests(self, requests_json):
        try:
            request = json.loads(requests_json)
            action = request.get("action")
            if action == "get_movies":
                return self.get_movies()
            elif action == "add_movies":
                return self.add_movies(request.get("data"))
            elif action == "update_movie":
                return self.updte_movie(request.get("data"))
            elif action == "delete_movies":
                return self.delete_movie(request.get("id"))
            elif action == "calculate_price":
                return self.calculate(request.get("data"))
            elif action == "purchase":
                return self.purchase(request.get("data"))
            else:
                return json.dumps({
                    "status":"error",
                    "message": f"Unknown action {action}"
                })

        except Exception as e:
            message = f"{e}"
            return json.dumps({
                "status":"error",
                "message": message
            })
        
    #list to dict https://stackoverflow.com/a/1993853/29467637
    #rows https://docs.python.org/3/library/sqlite3.html#:~:text=You%20can%20create,%2C%20row)%7D
    def get_movies(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM movies")
            columns = [description[0] for description in cursor.description]
            movies = [dict(zip(columns, rows)) for rows in cursor.fetchall()]
            return json.dumps({
                "status":"success",
                "data": movies
            }, indent=4)
        except Exception as e:
            message = f"{e}"
            return json.dumps({
                "status":"error",
                "message":message
            })
        
    def add_movies(self, movie_data):
        try:
            cursor = self.db.cursor()
            query = "INSERT INTO movies (title, cinema_room, release_date, end_date, tickets, ticket_price) VALUES (?, ?, ?, ?, ?, ?)"
            values = (
                movie_data['title'],
                movie_data.get('cinema_room'),
                movie_data['release_date'],
                movie_data['end_date'],
                movie_data['tickets'],
                movie_data['ticket_price']
            )

            cursor.execute(query, values)
            self.db.commit()
            return json.dumps({
                "status":"success",
                "message": f"movie '{movie_data['title']}' aadded successfully"
            })

        except Exception as e:
            message = f"{e}"
            return json.dumps({
                "status":"error",
                "message": message
            })
        
    #https://www.w3schools.com/sql/sql_update.asp
    def updte_movie(self, movie_data):
        try:
            cursor = self.db.cursor()
            query = """UPDATE movies 
                        SET title = ?, cinema_room = ?, release_date = ?, end_date = ?, tickets = ?, ticket_price = ? 
                        WHERE id = ?"""
            values = (
                movie_data['title'],
                movie_data['cinema_room'],
                movie_data['release_date'],
                movie_data['end_date'],
                movie_data['tickets'],
                movie_data['ticket_price'],
                movie_data["movie_id"]
            )

            cursor.execute(query, values)
            self.db.commit()
            return json.dumps({
                "status":"success",
                "message": f"{movie_data['title']}  update successfully"
            })

        except Exception as e:
            message = f"{e}"
            return json.dumps({
                "status":"error",
                "message": message
            })
        

    def delete_movie(self, movie_id):
        try:
            cursor = self.db.cursor()
            query = "DELETE FROM movies WHERE id = ?"
            values = (movie_id,)
            cursor.execute(query, values)
            self.db.commit()
            return json.dumps({"status": "success", "message": "Movie deleted successfully"})
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"{e}"
            })
        
    def calculate(self, movie_data):
        movie_id = movie_data.get("id")
        num_of_tickets = int(movie_data.get("num_of_tickets"))
        total = 0
        try:
            query = "SELECT ticket_price FROM movies WHERE id = ?"
            values = (movie_id,)
            cursor = self.db.cursor()
            cursor.execute(query, values)
            price = cursor.fetchone()

            if price:
                try:
                    fPrice = float(price[0])
                    total = fPrice * num_of_tickets
                    return json.dumps({
                        "status": "success",
                        "total": total
                    })
                except (TypeError, ValueError) as e:
                    return json.dumps({
                        "status":"Error",
                        "message": f"Error: {e}"
                    })
            else:
                return json.dumps({
                        "status":"Error",
                        "message": "404 Movie no found"
                    })
        except Exception as e:
            return json.dumps({
                "status":"error",
                "message": f"{e}"
            })
        
    def purchase(self, movie_data):
        
        num_of_tickets = int(movie_data['num_of_tickets'])
        movie_id = movie_data['id']
        total = movie_data['total']
        cursor = self.db.cursor()

        #Cal
        if total == "" or total is None:
            try:
                query = "SELECT ticket_price FROM movies WHERE id = ?"
                values = (movie_id,)
                cursor.execute(query, values)
                price = cursor.fetchone()
                
                if price:
                    try:
                        fPrice = float(price[0])
                        total = fPrice * num_of_tickets
                    except (TypeError, ValueError) as e:
                        return json.dumps({
                            "status":"Error",
                            "message": f"Error: {e}"
                        })
                else:
                    return json.dumps({
                            "status":"Error",
                            "message": "404 Movie no found"
                        })
            except Exception as e:
                return json.dumps({
                    "status":"error",
                    "message": f"{e}"
                })
        else:
            total = float(movie_data['total'])

        #sale
        try:
            query1 = """
                UPDATE movies SET tickets = tickets - ? WHERE id = ? AND tickets >= ?    
            """
            values1 = (num_of_tickets, movie_id, num_of_tickets)

            query2 = """
                INSERT INTO sales (movie_id, number_of_tickets, total) VALUES (?, ?, ?)
            """
            values2 = (movie_id, num_of_tickets, total)

            cursor.execute(query1, values1)
            if cursor.rowcount == 0:
                return json.dumps({
                    "status":"error",
                    "message": "not enough tickets available or else movie is available"
                })
            else:
                cursor.execute(query2, values2)
                self.db.commit()
                return json.dumps({
                    "status":"success",
                    "message": "Tickets sold successfully"
                })
        except sqlite3.IntegrityError as e:
            message = f"Integrity Error: {e}"
            return json.dumps({
                "status":"error",
                "message": message
            })
        except sqlite3.OperationalError as e:
            message = f"Operational error: {e}"
            return json.dumps({
                "status":"error",
                "message": message
            })
        except sqlite3.DatabaseError as e:
            message = f"Database error: {e}"
            return json.dumps({
                "status":"error",
                "message": message
            })
        except Exception as e:
            message = f"An error that i didnt anticipate lol😭"
            return json.dumps({
                "status":"error",
                "message": message
            })



    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Server is up {self.host}:{self.port}")
            while True:
                client_host, clinet_address = s.accept()
                with client_host:
                    print(f"{clinet_address} connected")
                    data = client_host.recv(4096).decode()
                    response = self.handle_requests(data)
                    client_host.sendall(response.encode())


if "__main__" == __name__:
    MServer = MovieServer()
    MServer.run()
