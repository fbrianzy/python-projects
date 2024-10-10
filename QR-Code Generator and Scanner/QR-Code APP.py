import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import Label
import qrcode
from PIL import ImageTk, Image
from pyzbar.pyzbar import decode
import cv2
import webbrowser

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator and Scanner")
        self.root.geometry("400x550")

        self.mode = tk.StringVar(value="generate")
        self.scan_mode = tk.StringVar(value="file")

        self.frameMode = tk.Frame(self.root)
        self.frameMode.pack(pady=10)

        self.label = tk.Label(self.frameMode, text="Choose mode:")
        self.label.grid(row=0, column=0, padx=10, pady=5)

        self.radio_generate = tk.Radiobutton(self.frameMode, text="Generate QR", variable=self.mode, value="generate", command=self.updateUI)
        self.radio_generate.grid(row=1, column=0, padx=10, pady=5)

        self.radio_scan = tk.Radiobutton(self.frameMode, text="Scan QR", variable=self.mode, value="scan", command=self.updateUI)
        self.radio_scan.grid(row=1, column=1, padx=10, pady=5)

        self.framePayment = tk.Frame(self.root)
        self.framePayment.pack(pady=20)

        self.entry = tk.Entry(self.framePayment, width=30)  # Input untuk Generate QR
        self.entry.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

        self.generate_btn = tk.Button(self.framePayment, text="Generate QR Code", command=self.generateQR)
        self.generate_btn.grid(row=2, column=0, padx=10, pady=5, columnspan=2)

        self.save_btn = tk.Button(self.framePayment, text="Save QR Code", command=self.saveQR, state=tk.DISABLED)
        self.save_btn.grid(row=3, column=0, padx=10, pady=5, columnspan=2)

        self.radio_scan_file = tk.Radiobutton(self.framePayment, text="Scan from file", variable=self.scan_mode, value="file")
        self.radio_scan_file.grid(row=4, column=0, padx=10, pady=5)

        self.radio_scan_camera = tk.Radiobutton(self.framePayment, text="Scan from camera", variable=self.scan_mode, value="camera")
        self.radio_scan_camera.grid(row=4, column=1, padx=10, pady=5)

        self.scan_btn = tk.Button(self.framePayment, text="Scan QR Code", command=self.scanQR)
        self.scan_btn.grid(row=5, column=0, padx=10, pady=5, columnspan=2)
        self.scan_btn.grid_remove()
        self.qrLabel = None
        self.qr_image = None

        self.updateUI()

    def updateUI(self):
        if self.mode.get() == "generate":
            self.entry.grid()
            self.generate_btn.grid()
            self.save_btn.grid()
            self.radio_scan_file.grid_remove()
            self.radio_scan_camera.grid_remove()
            self.scan_btn.grid_remove()
            if self.qrLabel:
                self.qrLabel.grid()
        elif self.mode.get() == "scan":
            self.entry.grid_remove()
            self.generate_btn.grid_remove()
            self.save_btn.grid_remove()
            self.radio_scan_file.grid()
            self.radio_scan_camera.grid()
            self.scan_btn.grid()
            if self.qrLabel:
                self.qrLabel.grid_remove()

    def generateQR(self):
        self.data = self.entry.get()
        if self.data:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.data)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            img = img.resize((200, 200))

            self.qr_image = img
            img = ImageTk.PhotoImage(img)

            if self.qrLabel:
                self.qrLabel.config(image=img)
                self.qrLabel.image = img
            else:
                self.qrLabel = Label(self.framePayment, image=img)
                self.qrLabel.image = img
                self.qrLabel.grid(row=6, column=0, padx=10, pady=5, columnspan=2)

            self.save_btn.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Please enter some data!")

    def saveQR(self):
        if self.qr_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.qr_image.save(file_path)
                messagebox.showinfo("Success", "QR Code saved successfully!")
            else:
                messagebox.showerror("Error", "File path not provided!")
        else:
            messagebox.showerror("Error", "No QR code to save!")

    def scanQR(self):
        if self.scan_mode.get() == "file":
            self.scanQRFromFile()
        elif self.scan_mode.get() == "camera":
            self.detectorQR()

    def scanQRFromFile(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*")])
        if file_path:
            img = Image.open(file_path)
            decoded_data = decode(img)
            if decoded_data:
                decoded_text = decoded_data[0].data.decode('utf-8')
                self.handleDecodedQR(decoded_text)
            else:
                messagebox.showerror("Error", "No QR code found in the image!")
        else:
            messagebox.showerror("Error", "No file selected!")

    def detectorQR(self):
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        while True:
            _, img = cap.read()
            data, _, _ = detector.detectAndDecode(img)
            if data:
                cap.release()
                cv2.destroyAllWindows()
                self.handleDecodedQR(data)
                break
            cv2.imshow('QR-Code Scanner', img)
            if cv2.waitKey(2) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def handleDecodedQR(self, data):
        if data.startswith("http://") or data.startswith("https://"):
            open_web = messagebox.askyesno("Open Link", f"QR Code contains a link:\n{data}\n\nDo you want to open it?")
            if open_web:
                webbrowser.open(data)
        else:
            messagebox.showinfo("Scan Result", f"Decoded QR Code: {data}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()