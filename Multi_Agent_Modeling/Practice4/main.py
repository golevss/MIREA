import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter

STATES = ['Zdorovi', 'Venom', 'Carnage', 'SuperVenom', 'Smert']
COLOR_MAP = {
    'Zdorovi': 'green',
    'Venom': 'blue',
    'Carnage': 'red',
    'SuperVenom': 'cyan',
    'Smert': 'gray'
}

class Agent:
    def __init__(self):
        self.state = 'Zdorovi'

    def receive_message(self, message):
        if message == 'Kill' and self.state == 'Zdorovi':
            self.state = 'Smert'
        elif message == 'Venom' and self.state == 'Carnage':
            self.state = 'SuperVenom'
        elif message == 'Carnage' and self.state == 'Venom':
            self.state = 'SuperVenom'

class Simulation:
    def __init__(self, root):
        self.root = root
        self.agents = [Agent() for _ in range(500)]
        self.intensities = {
            'Zdorovi_to_Venom': 0.01,
            'Zdorovi_to_Carnage': 0.01,
            'Venom_to_Smert': 0.005,
            'Carnage_to_Smert': 0.005,
            'Vstrechi': 0.01
        }
        self.setup_gui()
        self.update_simulation()

    def setup_gui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Slid
        for key in self.intensities:
            lbl = tk.Label(control_frame, text=key)
            lbl.pack(side=tk.LEFT)
            slider = tk.Scale(control_frame, from_=0, to=0.1, resolution=0.001,
                              orient=tk.HORIZONTAL, command=self.update_intensity(key))
            slider.set(self.intensities[key])
            slider.pack(side=tk.LEFT)

        # Butt
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(side=tk.TOP, fill=tk.X)
        btn_sv_to_sm = tk.Button(btn_frame, text="Kill SuperVenom", command=self.kill_supervenom)
        btn_sv_to_sm.pack(side=tk.LEFT)
        btn_sm_to_zd = tk.Button(btn_frame, text="Vozrodit", command=self.revive_smert)
        btn_sm_to_zd.pack(side=tk.LEFT)

        # Canvas
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg='white')
        self.canvas.pack(side=tk.LEFT)

        # Graph
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.graph_canvas.get_tk_widget().pack(side=tk.RIGHT)

    def update_intensity(self, key):
        def update(val):
            self.intensities[key] = float(val)
        return update

    def kill_supervenom(self):
        for agent in self.agents:
            if agent.state == 'SuperVenom':
                agent.state = 'Smert'

    def revive_smert(self):
        for agent in self.agents:
            if agent.state == 'Smert':
                agent.state = 'Zdorovi'

    def update_simulation(self):
        for agent in self.agents:
            if agent.state == 'Zdorovi':
                if random.random() < self.intensities['Zdorovi_to_Venom']:
                    agent.state = 'Venom'
                elif random.random() < self.intensities['Zdorovi_to_Carnage']:
                    agent.state = 'Carnage'

            elif agent.state == 'Venom':
                if random.random() < self.intensities['Venom_to_Smert']:
                    agent.state = 'Smert'
                if random.random() < self.intensities['Vstrechi']:
                    target = random.choice(self.agents)
                    target.receive_message(random.choice(['Kill', 'Venom']))

            elif agent.state == 'Carnage':
                if random.random() < self.intensities['Carnage_to_Smert']:
                    agent.state = 'Smert'
                if random.random() < self.intensities['Vstrechi']:
                    target = random.choice(self.agents)
                    target.receive_message(random.choice(['Kill', 'Carnage']))

        self.update_canvas()
        self.update_graph()
        self.root.after(100, self.update_simulation)

    def update_canvas(self):
        self.canvas.delete('all')
        cols = 25
        size = 400 // cols
        for idx, agent in enumerate(self.agents):
            row = idx // cols
            col = idx % cols
            x0, y0 = col*size, row*size
            x1, y1 = x0+size, y0+size
            color = COLOR_MAP.get(agent.state, 'white')
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='')

    def update_graph(self):
        self.ax.clear()
        counts = Counter(agent.state for agent in self.agents)
        self.ax.bar(counts.keys(), counts.values(), color=[COLOR_MAP[s] for s in counts.keys()])
        self.ax.set_title("Agent States")
        self.graph_canvas.draw()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Agent Simulation")
    app = Simulation(root)
    root.mainloop()
