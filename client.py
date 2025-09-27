#imports
import json
import socket
from tkinter import ttk, messagebox
import tkinter as tk


#function class
class Client:
    def __init__(self, host = '127.0.0.1', port=65333):
        self.host = host
        self.port = port

    def send_request(self, request_dictionary):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(json.dumps(request_dictionary).encode())
                response = s.recv(4096).decode()
                return json.loads(response)
        except Exception as e:
            message = f"{e}"
            return {
                "status": "error",
                "message": message
            }
        
    def get_movies(self):
        return self.send_request({"action":"get_movies"})
    
    def add_movies(self, title, release_date, end_date, tickets, ticket_price ,cinema_room=None):
        return self.send_request({
            "action":"add_movies",
            "data":{
                "title": title,
                "cinema_room": cinema_room,
                "release_date": release_date,
                "end_date": end_date,
                "tickets": tickets,
                "ticket_price": ticket_price
            }
        })
    
    def delete_movie(self, movie_id):
        return self.send_request({
            "action": "delete_movies",
            "id": movie_id
        })

    def update_movie(self,movie_id, title=None, release_date=None, end_date=None, tickets=None, ticket_price=None ,cinema_room=None):
        return self.send_request({
            "action":"update_movie",
            "data":{
                "title": title,
                "cinema_room": cinema_room,
                "release_date": release_date,
                "end_date": end_date,
                "tickets": tickets,
                "ticket_price": ticket_price,
                "movie_id": movie_id,
            }
        })
    
    def calculate_price(self, num_of_tickets, movie_id):
        return self.send_request({
            "action":"calculate_price",
            "data":{
                "id": movie_id,
                "num_of_tickets": num_of_tickets
            }
        })
    
    def purchase(self, movie_id, num_of_tickets, total):
        return self.send_request({
            "action": "purchase",
            "data":{
                "id": movie_id,
                "num_of_tickets":num_of_tickets,
                "total": total
            }
        })
        



#User Interface
class ClientGUI(tk.Tk):
    def __init__(self, clinet):
        super().__init__()
        self.client = clinet
        self.title("NewLine cinema")
        self.geometry("600x450")
        self.movies = []
        self.selected_movie_id = None
        self.create_widget()

    def create_widget(self):
        frame = ttk.Frame(self)
        frame.pack(pady=15, padx=15)

        #combo box
        ttk.Label(frame, text="Select Movie").grid(row=0, column=0, sticky="w")
        self.movie_selector = ttk.Combobox(frame, width=50, state="readonly")
        self.movie_selector.grid(row=0, column=1)
        self.movie_selector.bind("<<ComboboxSelected>>", self.on_movie_selected)

        #movie title
        ttk.Label(frame, text="Title:").grid(row=1, column=0, sticky="w")
        self.title_entry = ttk.Entry(frame, width=30)
        self.title_entry.grid(row=1, column=1)

        ttk.Label(frame, text="cinema room:").grid(row=2, column=0, sticky="w")
        self.cinema_room_entry = ttk.Entry(frame, width=30)
        self.cinema_room_entry.grid(row=2, column=1)

        ttk.Label(frame, text="release date:").grid(row=3, column=0, sticky="w")
        self.release_date_entry = ttk.Entry(frame, width=30)
        self.release_date_entry.grid(row=3, column=1)

        ttk.Label(frame, text="end date:").grid(row=4, column=0, sticky="w")
        self.end_date_entry = ttk.Entry(frame, width=30)
        self.end_date_entry.grid(row=4, column=1)

        ttk.Label(frame, text="tickets:").grid(row=5, column=0, sticky="w")
        self.tickets_entry = ttk.Entry(frame, width=30)
        self.tickets_entry.grid(row=5, column=1)

        ttk.Label(frame, text="ticket price:").grid(row=6, column=0, sticky="w")
        self.ticket_price_entry = ttk.Entry(frame, width=30)
        self.ticket_price_entry.grid(row=6, column=1)

        ttk.Label(frame, text="number of tickets:").grid(row=7, column=0, sticky="w")
        self.num_of_tickets_entry = ttk.Entry(frame, width=30)
        self.num_of_tickets_entry.grid(row=7, column=1)

        ttk.Label(frame, text="price:").grid(row=8, column=0, sticky="w")
        self.price_entry = ttk.Entry(frame, width=30, state="readonly")
        self.price_entry.grid(row=8, column=1)
        ttk.Button(frame, text="Calculate Price", command=self.calculate_price).grid(row=8, column=2)


        ttk.Button(frame, text="Add Movie", command=self.add_movie).grid(row=9, column=0, pady=10, padx=5)
        ttk.Button(frame, text="Update Movie", command=self.update_movie).grid(row=9, column=1)
        ttk.Button(frame, text="Delete Movie", command=self.delete_movie).grid(row=9, column=2)
        ttk.Button(frame, text="Purchase tickets", command=self.purchase_ticket).grid(row=10, column=1, padx=5,pady=10)

        self.load_movies()

    def load_movies(self):
        response = self.client.get_movies()
        if response['status'] == 'success':
            self.movies = response['data']
            self.movie_selector['values'] = [f"{movie['id']} : {movie['title']}" for movie in self.movies]
        else:
            messagebox.showerror("Error", response['message'])

    def on_movie_selected(self, event):
        index = self.movie_selector.current()
        movie = self.movies[index]
        self.selected_movie_id = movie['id']

        self.cinema_room_entry.delete(0, tk.END)
        self.cinema_room_entry.insert(0, movie['cinema_room'])
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, movie['title'])
        self.release_date_entry.delete(0, tk.END)
        self.release_date_entry.insert(0, movie['release_date'])
        self.end_date_entry.delete(0, tk.END)
        self.end_date_entry.insert(0, movie['end_date'])
        self.tickets_entry.delete(0, tk.END)
        self.tickets_entry.insert(0, movie['tickets'])
        self.ticket_price_entry.delete(0, tk.END)
        self.ticket_price_entry.insert(0, movie['ticket_price'])

    def add_movie(self):
        title = self.title_entry.get()
        cinema_room = self.cinema_room_entry.get()
        release_date = self.release_date_entry.get()
        end_date = self.end_date_entry.get()
        tickets = self.tickets_entry.get()
        ticket_price = self.ticket_price_entry.get()
        if not title or not release_date or not end_date or not tickets or not ticket_price:
            messagebox.showerror("Error","Some required information is missing issue isnt the room number ig")
            return
        response = self.client.add_movies(title=title, release_date=release_date, end_date=end_date, tickets = tickets ,ticket_price=ticket_price, cinema_room=cinema_room)
        self.handle_response(response)

    def update_movie(self):
        if self.selected_movie_id is None:
            messagebox.showerror("Error", "No movie selected please select a movie from the dropdown")
            return
        title = self.title_entry.get()
        cinema_room = self.cinema_room_entry.get()
        release_date = self.release_date_entry.get()
        end_date = self.end_date_entry.get()
        tickets = self.tickets_entry.get()
        ticket_price = self.ticket_price_entry.get()
        response = self.client.update_movie(self.selected_movie_id ,title=title, release_date=release_date, end_date=end_date, tickets = tickets ,ticket_price=ticket_price, cinema_room=cinema_room)
        self.handle_response(response)

    def delete_movie(self):
        if self.selected_movie_id is None:
            messagebox.showerror("Error", "No movie selected to delete")
            return
        response = self.client.delete_movie(self.selected_movie_id)
        self.handle_response(response)

    def calculate_price(self):
        if self.selected_movie_id is None:
            messagebox.showerror("Error", "No movie selected to delete")
            return
        num_of_tickets = self.num_of_tickets_entry.get()
        response = self.client.calculate_price(num_of_tickets ,self.selected_movie_id)
        self.displa_price(response)

    def purchase_ticket(self):
        if self.selected_movie_id is None:
            messagebox.showerror("Error", "No movie selected to delete")
            return
        
        num_of_tickets = self.num_of_tickets_entry.get()
        total = self.price_entry.get()
        response = self.client.purchase(self.selected_movie_id, num_of_tickets, total)
        self.handle_response(response)

    def handle_response(self, response):
        try:
            if response['status'] == 'success':
                messagebox.showinfo("Succes", response['message'])
                self.clear_fields()
                self.load_movies()
            else:
                messagebox.showerror("Error", response['message'])
        except Exception as e:
            messagebox.showerror("Error", f"Problem \n {e}")

    def displa_price(self, response):
        try:
            if response['status'] == 'success':
                total = response['total']
                self.price_entry.config(state="normal")
                self.price_entry.delete(0, tk.END)
                self.price_entry.insert(0, f"{total:.2f}")
                self.price_entry.config(state="readonly")
            else:
                messagebox.showerror("Error", response['message'])
        except Exception as e:
            messagebox.showerror("Error", f"Problem \n {e}")

    
    
    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.cinema_room_entry.delete(0, tk.END)
        self.release_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.tickets_entry.delete(0, tk.END)
        self.ticket_price_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.num_of_tickets_entry.delete(0, tk.END)
        self.price_entry.config(state="normal")
        self.price_entry.delete(0, tk.END)
        self.price_entry.config(state="readonly")
        self.movie_selector.set("")
        self.selected_movie_id = None


if "__main__" == __name__:
    client = Client()
    gui = ClientGUI(client)
    gui.mainloop()