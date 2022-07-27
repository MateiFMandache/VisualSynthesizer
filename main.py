import tkinter as tk
import tkinter.messagebox as mb
import wave
import struct
from playsound import playsound


NAME = "Visual Synthesizer"
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 450
CANVAS_LOOP = 600
CANVAS_MIDDLE = CANVAS_HEIGHT/2
# Move more points with one click if they occur at a small difference
DIFFERENCES = [-2, -1, 0, 1, 2]
MAX_AMPLITUDE = 32760


class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(NAME)

        tk.Label(self, text="Filename:").grid(row=0, column=0, sticky=tk.E)
        self.filename = tk.StringVar(self, "Sound")
        self.filename_entry = tk.Entry(self, textvariable=self.filename)
        self.filename_entry.grid(row=0, column=1, sticky=tk.W)
        tk.Label(self, text="Frequency:").grid(row=0, column=2, sticky=tk.E)
        self.frequency = tk.StringVar(self, "440")
        self.freq_entry = tk.Entry(self, textvariable=self.frequency)
        self.freq_entry.grid(row=0, column=3, sticky=tk.W)
        self.button = tk.Button(self, text="Play", command=self.play)
        self.button.grid(row=0, column=4)

        self.canvas = tk.Canvas(self, height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.grid(row=1, column=0, columnspan=5)
        self.waveform = [CANVAS_MIDDLE for _ in range(CANVAS_LOOP)]
        self.update_canvas()
        self.canvas.bind("<B1-Motion>", self.change_waveform)

    def change_waveform(self, event):
        """Changes the waveform in response to a mouse event"""
        for difference in DIFFERENCES:
            self.waveform[(event.x + difference) % CANVAS_LOOP] = event.y
        self.update_canvas()

    def update_canvas(self):
        """Ensures the canvas displays the current waveform"""
        self.canvas.delete("all")
        for x in range(CANVAS_WIDTH):
            y = self.waveform[x % CANVAS_LOOP]
            self.canvas.create_oval(x-1, y-1, x+1, y+1, width=0, fill="black")

    def play(self):
        """Creates the wav file for the sound and plays it"""
        try:
            frequency = int(self.frequency.get())
        except ValueError:
            mb.showerror("Couldn't play", "The frequency must be an integer")
            return
        sample_rate = frequency*CANVAS_LOOP
        file = wave.open(f"./Sounds/{self.filename.get()}.wav", "wb")
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(sample_rate)
        one_wave = [struct.pack('<h', int(
            MAX_AMPLITUDE*(CANVAS_MIDDLE - y)/CANVAS_MIDDLE
        )) for y in self.waveform]
        for _ in range(frequency):
            for data in one_wave:
                file.writeframesraw(data)
        file.close()

        playsound(f"./Sounds/{self.filename.get()}.wav")


def main():
    view = View()
    view.mainloop()


if __name__ == "__main__":
    main()
