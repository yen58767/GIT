import tkinter as tk
import ctypes
import pickle
import os
from PIL import Image, ImageTk

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("關閉螢幕")
        
        # 載入視窗位置設定
        try:
            with open("window.pkl", "rb") as f:
                self.root.geometry(pickle.load(f))
        except:
            pass
        
        # 背景圖片 - 使用相對路徑
        try:
            background_path = "Background.png"
            if os.path.exists(background_path):
                # 載入背景圖片
                self.image = Image.open(background_path)
                self.photo = ImageTk.PhotoImage(self.image)
                # 建立 Label 並設定圖片
                self.label = tk.Label(self.root, image=self.photo)
                self.label.pack()
            else:
                print(f"警告：找不到背景圖片 {background_path}")
                # 如果找不到圖片，建立一個簡單的背景
                self.root.configure(bg='lightgray')
        except Exception as e:
            print(f"載入背景圖片時發生錯誤：{e}")
            self.root.configure(bg='lightgray')

        # 建立倒數計時Label
        self.countdown_label = tk.Label(self.root, text="", font=("Arial", 20), highlightbackground=self.root.cget("bg"))

        self.yen = tk.Label(self.root, text="Yen", font=("Arial", 10), bg='#D58C33')
        self.yen.config(text="@yen")  # 設定初始文字為空字串
        self.yen.place(relx=0.917, rely=0.885, anchor="center")

        # 設定倒數計時的ID
        self.countdown_id = None

        def start_countdown():
            # 開始倒數計時
            self.countdown_label.place(relx=0.85, rely=0.55, anchor="center")
            self.stop_button.config(state="normal")
            self.button.config(state="disabled")
            self.countdown_label.config(text="5")  # 設定倒數計時的秒數
            self.countdown_id = self.root.after(0, countdown, 5)

        def countdown(seconds):
            if seconds > 0:
                self.countdown_label.config(text=str(seconds))
                self.countdown_id = self.root.after(1000, countdown, seconds-1)
            else:
                # 關閉螢幕
                ctypes.windll.user32.SendMessageW(0xFFFF, 0x112, 0xF170, 2)
                # 倒數計時結束，清除ID和Label
                self.countdown_id = None
                self.countdown_label.config(text="")
                self.stop_button.config(state="disabled")
                self.button.config(state="normal")

        def stop_countdown():
            # 停止倒數計時
            if self.countdown_id is not None:
                self.root.after_cancel(self.countdown_id)
                self.countdown_id = None
                self.countdown_label.config(text="")
                self.stop_button.config(state="disabled")
                self.button.config(state="normal")
                self.countdown_label.place(relx=10.85, rely=10.55, anchor="center")
                # 顯示彈窗
                popup = tk.Toplevel()
                popup.title("已停止")
                # 如果圖示載入成功，也用在彈窗上
                if hasattr(self, 'icon_photo'):
                    popup.iconphoto(True, self.icon_photo)
                popup.resizable(False, False)
                popup.geometry("120x30+{}+{}".format(self.root.winfo_x() + 50, self.root.winfo_y() + 50))
                popup.configure(bg="black")
                popup_label = tk.Label(popup, text="已停止", bg='black', fg='white', width=10, height=2, font=("Arial", 15, "bold"))
                popup_label.place(relx=0.5, rely=0.5, anchor="center")
                popup_label.pack()
                popup.after(800, popup.destroy)  # 0.8 秒後自動關閉彈窗

        # 建立按鈕
        self.button = tk.Button(self.root, text="關閉螢幕", command=start_countdown)
        self.button.place(relx=0.35, rely=0.6, anchor="center")

        # 建立停止按鈕
        self.stop_button = tk.Button(self.root, text="停止", command=stop_countdown, state="disabled")
        self.stop_button.place(relx=0.65, rely=0.6, anchor="center")

        def enable_stop_button(event):
            self.stop_button.config(state="normal")

        # 倒數計時Label綁定事件，啟用停止按鈕
        self.countdown_label.bind("<Button-1>", enable_stop_button)
        
        # 載入應用程式圖示
        try:
            icon_path = "Icon.ico"
            if os.path.exists(icon_path):
                # 載入 .ico 圖示
                icon_image = Image.open(icon_path)
                self.icon_photo = ImageTk.PhotoImage(icon_image)
                # 設置根視窗的 icon
                self.root.iconphoto(True, self.icon_photo)
            else:
                print(f"警告：找不到圖示檔案 {icon_path}")
        except Exception as e:
            print(f"載入圖示時發生錯誤：{e}")
        
        self.root.geometry("225x100")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def run(self):
        self.root.mainloop()

    def on_close(self):
        # 保存視窗位置和大小
        with open("window.pkl", "wb") as f:
            pickle.dump(self.root.geometry(), f)
        self.root.destroy()

if __name__ == "__main__":
    app = App()
    app.run()