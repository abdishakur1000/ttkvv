import tkinter as tk
import cv2
from PIL import Image, ImageTk


class VideoPlayer:

  def __init__(self, window, video_source=0):
    self.window = window
    self.window.title("Video Player")

    # Open video source (webcam or file)
    self.cap = cv2.VideoCapture(video_source)

    # Create a canvas that can fit the video source
    self.canvas = tk.Canvas(window,
                            width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                            height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    self.canvas.pack()

    # Button that lets the user take a snapshot
    self.btn_snapshot = tk.Button(window,
                                  text="Snapshot",
                                  command=self.snapshot)
    self.btn_snapshot.pack(side=tk.LEFT, anchor=tk.CENTER, expand=True)

    # Button that starts and stops recording
    self.recording = False
    self.btn_record = tk.Button(window,
                                text="Record",
                                command=self.toggle_recording)
    self.btn_record.pack(side=tk.LEFT, anchor=tk.CENTER, expand=True)

    # After it is called once, the update method will be automatically called every delay milliseconds
    self.delay = 15
    self.update()

    self.window.mainloop()

  def update(self):
    # Get a frame from the video source
    ret, frame = self.cap.read()

    if ret:
      self.photo = ImageTk.PhotoImage(
        image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
      self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

      # Record frame if recording is on
      if self.recording:
        self.out.write(frame)

    self.window.after(self.delay, self.update)

  def snapshot(self):
    # Get a frame from the video source
    ret, frame = self.cap.read()

    if ret:
      cv2.imwrite("snapshot.png", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

  def toggle_recording(self):
    if not self.recording:
      # Start recording
      fourcc = cv2.VideoWriter_fourcc(*'XVID')
      self.out = cv2.VideoWriter(
        'output.avi', fourcc, 20.0,
        (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
         int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
      self.btn_record.config(text="Stop")
    else:
      # Stop recording
      self.out.release()
      self.btn_record.config(text="Record")

    self.recording = not self.recording

  def __del__(self):
    if self.cap.isOpened():
      self.cap.release()


# Create a window and pass it to the VideoPlayer class
VideoPlayer(tk.Tk(), 0)
