from tkinter import *
from tkinter import ttk
from tkinter import font
import tkinter.filedialog
from PIL import ImageTk, Image
from tkinter import messagebox
from io import BytesIO
import os

class SteganographyApp:
    def __init__(self):
        self.art = '''
   Data Hiding 
     In Image
        '''
        self.output_image_size = 0
        self.d_image_size = 0
        self.o_image_w, self.o_image_h = 0, 0
        self.d_image_w, self.d_image_h = 0, 0

    def main(self, root):
        root.title('Image Steganography')
        root.geometry('500x600')
        root.resizable(width=False, height=False)
        
        f = Frame(root)
        title = Label(f, text='Image Steganography')
        title.config(font=('courier', 30))
        title.grid(pady=10)
        
        b_encode = Button(f, text='Encode', padx=14, command=lambda: self.frame1_encode(f))
        b_encode.config(font=('courier', 14))
        b_encode.grid(pady=12)
        
        b_decode = Button(f, text='Decode', padx=14, command=lambda: self.frame1_decode(f))
        b_decode.config(font=('courier', 14))
        b_decode.grid(pady=12)
        
        ascii_art = Label(f, text=self.art)
        ascii_art.config(font=('courier', 50))
        ascii_art.grid(row=4, pady=10)
        
        f.grid()
        root.mainloop()

    def home(self, frame):
        frame.destroy()
        self.main(root)

    # ENCODE FUNCTIONS
    def frame1_encode(self, f):
        f.destroy()
        f2 = Frame(root)
        label_art = Label(f2, text='ENCODE')
        label_art.config(font=('courier', 70))
        label_art.grid(row=1, pady=50)
        
        l1 = Label(f2, text='Select image to hide message:')
        l1.config(font=('courier', 18))
        l1.grid()
        
        bws_button = Button(f2, text='Select', command=lambda: self.frame2_encode(f2))
        bws_button.config(font=('courier', 18))
        bws_button.grid()
        
        back_button = Button(f2, text='Cancel', command=lambda: self.home(f2))
        back_button.config(font=('courier', 18))
        back_button.grid(pady=15)
        f2.grid()

    def frame2_encode(self, f2):
        ep = Frame(root)
        myfile = tkinter.filedialog.askopenfilename(filetypes=[('PNG', '*.png'), ('JPEG', '*.jpeg'), ('JPG', '*.jpg'), ('All files', '*.*')])
        
        if not myfile:
            messagebox.showerror("Error", "No file selected!")
        else:
            myimg = Image.open(myfile)
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            
            l3 = Label(ep, text='Selected Image:')
            l3.config(font=('courier', 18))
            l3.grid()
            
            panel = Label(ep, image=img)
            panel.image = img
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = myimg.size
            panel.grid()
            
            l2 = Label(ep, text='Enter message to hide:')
            l2.config(font=('courier', 18))
            l2.grid(pady=15)
            
            text_area = Text(ep, width=50, height=10)
            text_area.grid()
            
            encode_button = Button(ep, text='Encode', command=lambda: [self.enc_fun(text_area, myimg), self.home(ep)])
            encode_button.config(font=('courier', 11))
            encode_button.grid(pady=15)
            
            cancel_button = Button(ep, text='Cancel', command=lambda: self.home(ep))
            cancel_button.config(font=('courier', 11))
            cancel_button.grid()
            
            ep.grid(row=1)
            f2.destroy()

    def genData(self, data):
        return [format(ord(i), '08b') for i in data]

    def modPix(self, pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)

        for i in range(lendata):
            pix = [value for value in imdata.__next__()[:3] +
                   imdata.__next__()[:3] +
                   imdata.__next__()[:3]]

            for j in range(8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):
                    pix[j] -= 1
                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1

            if i == lendata - 1:
                if pix[-1] % 2 == 0:
                    pix[-1] -= 1
            else:
                if pix[-1] % 2 != 0:
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)
        
        for pixel in self.modPix(newimg.getdata(), data):
            newimg.putpixel((x, y), pixel)
            if x == w - 1:
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self, text_area, myimg):
        data = text_area.get("1.0", "end-1c")
        
        if len(data) == 0:
            messagebox.showinfo("Alert", "Please enter text to hide")
        else:
            newimg = myimg.copy()
            self.encode_enc(newimg, data)
            
            temp = os.path.splitext(os.path.basename(myimg.filename))[0]
            save_path = tkinter.filedialog.asksaveasfilename(
                initialfile=temp,
                filetypes=[('PNG', '*.png')],
                defaultextension=".png")
            
            if save_path:
                newimg.save(save_path)
                self.d_image_size = os.stat(save_path).st_size
                self.d_image_w, self.d_image_h = newimg.size
                messagebox.showinfo("Success", "Encoding successful!\nSaved as: " + save_path)

    # DECODE FUNCTIONS
    def frame1_decode(self, f):
        f.destroy()
        f2 = Frame(root)
        label_art = Label(f2, text='DECODE')
        label_art.config(font=('courier', 70))
        label_art.grid(row=1, pady=50)
        
        l1 = Label(f2, text='Select image with hidden message:')
        l1.config(font=('courier', 18))
        l1.grid()
        
        bws_button = Button(f2, text='Select', command=lambda: self.frame2_decode(f2))
        bws_button.config(font=('courier', 18))
        bws_button.grid()
        
        back_button = Button(f2, text='Cancel', command=lambda: self.home(f2))
        back_button.config(font=('courier', 18))
        back_button.grid(pady=15)
        f2.grid()

    def frame2_decode(self, f2):
        dp = Frame(root)
        myfile = tkinter.filedialog.askopenfilename(filetypes=[('PNG', '*.png'), ('JPEG', '*.jpeg'), ('JPG', '*.jpg'), ('All files', '*.*')])
        
        if not myfile:
            messagebox.showerror("Error", "No file selected!")
        else:
            myimg = Image.open(myfile)
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            
            l3 = Label(dp, text='Selected Image:')
            l3.config(font=('courier', 18))
            l3.grid()
            
            panel = Label(dp, image=img)
            panel.image = img
            panel.grid()
            
            hidden_data = self.decode(myimg)
            
            l2 = Label(dp, text='Hidden message:')
            l2.config(font=('courier', 18))
            l2.grid(pady=15)
            
            text_area = Text(dp, width=50, height=10)
            text_area.insert(INSERT, hidden_data)
            text_area.grid()
            
            back_button = Button(dp, text='Back', command=lambda: self.home(dp))
            back_button.config(font=('courier', 11))
            back_button.grid(pady=15)
            
            dp.grid(row=1)
            f2.destroy()

    def decode(self, image):
        data = ''
        imgdata = iter(image.getdata())
        
        while True:
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            
            binstr = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'
            
            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                return data

if __name__ == "__main__":
    root = Tk()
    app = SteganographyApp()
    app.main(root)