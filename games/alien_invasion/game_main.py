import tkinter as tk

def run_game():
    root = tk.Tk()
    root.title('Alien Invasion')
    root.geometry('500x500')
    tk.Label(root, text="Python游戏").pack(pady=50)
    root.mainloop()

if __name__ == '__main__':
    run_game()