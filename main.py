from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import cx_Oracle
from tkcalendar import *
import subprocess
import cv2
from datetime import datetime

class login:
    def __init__(self):
        self.window = Tk()
        titlespace = "   "
        self.window.title(102 * titlespace + "login Esprit")
        ##self.window.iconbitmap('espritlogo.png')
        self.window.geometry('1199x600+300+0')
        self.bg = ImageTk.PhotoImage(file='espritlogo.jpg')
        self.bg_image = Label(self.window, image=self.bg).place(x=250, y=0, relwidth=1, relheight=1)
        self.window.resizable(False, False)
        frame_login = Frame(self.window, bg='white')
        frame_login.place(x=30, y=50, height=700, width=500)
        title = Label(frame_login, text='login here', font=('Impact', 25, 'bold'), fg='deepskyblue', bg='white').place(
            x=150, y=38)
        subtitle = Label(frame_login, text='Membere login Esprit', font=('Goody  old style', 15, 'bold'), fg='#1d1d1d',
                         bg='white').place(x=90, y=100)
        log_label = Label(frame_login, text="Username ", font=('Impact', 15, 'bold'), fg='grey', bg='white').place(
            x=90, y=140)
        self.log_text = Entry(frame_login, font=('Goody  old style', 15, 'bold'))
        self.log_text.place(x=90, y=170, height=35)
        pass_label = Label(frame_login, text="Password ", font=('Impact', 15, 'bold'), fg='grey', bg='white').place(
            x=90, y=200)
        self.pass_text = Entry(frame_login, show='*')
        self.pass_text.place(x=90, y=240, height=35)
        input_btn = Button(frame_login, text='LOGIN', font=('Impact',18, 'bold'), fg='grey', bg='white',
                           activebackground='red', command=self.newWindow).place(x=180, y=280)
        qb = Button(frame_login, text='Quitter', activebackground='red', font=('Impact', 15, 'bold'),
                    fg='grey', bg='white',command=self.iEXIT).place(x=180, y=340)
        self.root= Toplevel(self.window)
        self.root3 = Toplevel(self.window)
        self.root.withdraw()
        self.root3.withdraw()
        self.root4 = Toplevel(self.window)
        self.root4.withdraw()
        self.window.mainloop()
#####face_api
    def win1(self):
        self.root.deiconify()
        titlespace = ' '
        self.root.title(102 * titlespace + "ESPRIT LOGIN")
        self.root.geometry("800x700+300+0")
        self.root.resizable(False, False)
        frame_login1 = Frame(self.root, bg='cadet blue', bd=10, width=800, height=100, relief=RIDGE)
        frame_login1.grid()
        personel= Button(frame_login1, text='Personel', font=('Impact', 30, 'bold'), fg='grey', bg='white',
                           activebackground='red',).place(x=0, y=0)
        visiteur = Button(frame_login1, text='Visiteur', activebackground='red', font=('Impact', 30, 'bold'),
                    fg='grey', bg='white',command=self.agent).place(x=180, y=0)
        autorisation = Button(frame_login1, text='Autorisation', font=('Impact', 30, 'bold'), fg='grey', bg='white',
                           activebackground='red').place(x=340, y=0)
        historique = Button(frame_login1, text='Historique', activebackground='red', font=('Impact', 30, 'bold'),
                    fg='grey', bg='white',command=self.historique).place(x=580, y=0)

        consulter = Button(self.root, text='Consulter', activebackground='red', font=('Impact', 20, 'bold'),
                            fg='grey', bg='white',command=self.afficher1).place(x=0, y=100)

        self.consulter_text = Entry(self.root)
        self.consulter_text.place(x=350, y=140, height=35)

        frame_login2 = Frame(self.root, bd=5, bg='cadet blue', width=500, height=400, relief=RIDGE)
        frame_login2.place(x=200,y=200)

        # ======================================================================
        scroll_y = Scrollbar(frame_login2, orient=VERTICAL)

        self.per_cher1 = ttk.Treeview(frame_login2, height=12,
                                     columns=("id", "nom", "prenom", "tel", "fonction"),
                                     yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.per_cher1.heading("id", text="id")
        self.per_cher1.heading("nom", text="nom")
        self.per_cher1.heading("prenom", text="prenom")
        self.per_cher1.heading("tel", text="tel")
        self.per_cher1.heading("fonction", text="fonction")

        self.per_cher1['show'] = 'headings'

        self.per_cher1.column("id", width=70)
        self.per_cher1.column("nom", width=100)
        self.per_cher1.column("prenom", width=100)
        self.per_cher1.column("tel", width=100)
        self.per_cher1.column("fonction", width=70)

        self.per_cher1.pack(fill=BOTH, expand=1)

        self.window.withdraw()

    def start_facial_recognition(self):
        # Charger le classifieur de visage pré-entraîné
        face_cascade = cv2.CascadeClassifier('xml version.xml')

        # Charger les images des personnes connues et leurs noms
        known_faces = [
            {'image_path': 'WIN_20230515_11_03_11_Pro.jpg', 'name': 'nidhal'},
            {'image_path': 'WIN_20230515_12_35_20_Pro.jpg', 'name': 'feriel'},
            {'image_path': 'WIN_20230516_12_12_59_Pro.jpg', 'name': 'hatem'},
            {'image_path': 'WIN_20230516_12_14_27_Pro.jpg', 'name': 'badis'},
            # Ajoutez autant d'images et de noms que vous le souhaitez
        ]

        # Connexion à la base de données Oracle
        conn = cx_Oracle.connect('system/29378309@localhost:1521/xe')
        cursor = conn.cursor()

        # Charger les visages connus et les noms correspondants
        known_encodings = []
        known_names = []
        for known_face in known_faces:
            image = cv2.imread(known_face['image_path'])
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in face:
                face_encoding = gray[y:y + h, x:x + w]
                hist = cv2.calcHist([face_encoding], [0], None, [256], [0, 256])
                hist = cv2.normalize(hist, hist).flatten()
                known_encodings.append(hist)
                known_names.append(known_face['name'])

        # Capturer les images de la caméra en temps réel
        cap = cv2.VideoCapture(0)

        while True:
            # Lire le flux vidéo image par image
            ret, frame = cap.read()

            # Vérifier si la lecture de l'image a réussi
            if not ret:
                print("Échec de la lecture de l'image depuis la caméra.")
                break

            # Convertir l'image en niveaux de gris
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Détecter les visages dans l'image
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # Parcourir les visages détectés
            for (x, y, w, h) in faces:
                face_encoding = gray[y:y + h, x:x + w]
                hist = cv2.calcHist([face_encoding], [0], None, [256], [0, 256])
                hist = cv2.normalize(hist, hist).flatten()

                # Comparer avec les visages connus
                matches = []
                for known_encoding in known_encodings:
                    # Vérifier que les histogrammes sont de même profondeur et type
                    if hist.dtype != known_encoding.dtype:
                        known_encoding = known_encoding.astype(hist.dtype)
                    if hist.shape != known_encoding.shape:
                        hist = cv2.resize(hist, known_encoding.shape)

                    # Calculer la similarité entre le visage détecté et les visages connus
                    similarity = cv2.compareHist(hist, known_encoding, cv2.HISTCMP_CORREL)
                    matches.append(similarity)

                    # Trouver l'indice de la correspondance la plus élevée
                best_match_index = matches.index(max(matches))
                name = known_names[best_match_index]

                # Dessiner un rectangle autour du visage détecté
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Afficher le nom correspondant à côté du visage détecté
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                # Enregistrer le visage détecté avec l'heure et le nom associé dans la base de données
                timestamp = datetime.now().strftime("%d-%b-%Y")
                image_data = cv2.imencode('.jpg', frame[y:y + h, x:x + w])[1].tostring()

                cursor.execute("""INSERT INTO faces (name, timestamp, image) VALUES (:name, :timestamp, :image)""",
                               (name, timestamp, image_data))

                conn.commit()

                print("Visage enregistré dans la base de données.")

                # Afficher l'image résultante
            cv2.imshow('Reconnaissance faciale', frame)

            # Quitter la boucle si la touche 'q' est pressée
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Fermer la connexion à la base de données Oracle
        cursor.close()
        conn.close()

        # Libérer la capture de la caméra et détruire toutes les fenêtres
        cap.release()
        cv2.destroyAllWindows()

    def agent(self):


        self.root3.deiconify()
        titlespace = ' '
        self.root3.title(102 * titlespace + "ESPRIT LOGIN")
        self.root3.geometry("800x700+300+0")
        self.root3.resizable(False, False)
        frame_login1 = Frame(self.root3, bg='cadet blue', bd=10, width=500, height=100, relief=RIDGE)
        frame_login1.place(x=300,y=0)

        personel = Button(frame_login1, text='Ajouter visiteur', font=('Impact', 15, 'bold'), fg='grey', bg='white',
                          activebackground='red', command=self.formulaire).place(x=0, y=0)
        visiteur = Button(frame_login1, text='consulter Visiteur', activebackground='red', font=('Impact', 15, 'bold'),
                          fg='grey', bg='white',command=self.start_facial_recognition).place(x=150, y=0)
        autorisation = Button(frame_login1, text='>>', font=('Impact', 15, 'bold'), fg='grey', bg='white',
                              activebackground='red').place(x=340, y=0)
        historique = Button(frame_login1, text='<<', activebackground='red', font=('Impact',15, 'bold'),
                            fg='grey', bg='white').place(x=380, y=0)
        historique1 = Button(frame_login1, text='X', activebackground='red', font=('Impact',25, 'bold'),
                            fg='grey', bg='white').place(x=430, y=0)
        subtitle = Label(self.root3, text='Listes des autorisations', font=('Goody  old style', 15, 'bold'), fg='#1d1d1d',
                         bg='white').place(x=0, y=100)

        self.consulter_text = Entry(self.root3)
        self.consulter_text.place(x=100, y=140, height=35)

        ajouter = Button(self.root3, text='+', font=('Impact', 30, 'bold'), fg='grey', bg='white',
                          activebackground='blue',command=self.afficher ).place(x=100, y=500)

        frame_login2 = Frame(self.root3, bd=5, bg='cadet blue', width=900, height=900, relief=RIDGE)
        frame_login2.place(x=0, y=200)

        # ======================================================================
        scroll_y = Scrollbar(frame_login2, orient=VERTICAL)

        self.per_cher = ttk.Treeview(frame_login2, height=12,
                                     columns=("idlp", "nom", "prenom", "autorisation", "type"),
                                     yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.per_cher.heading("idlp", text="idlp")
        self.per_cher.heading("nom", text="nom")
        self.per_cher.heading("prenom", text="prenom")
        self.per_cher.heading("autorisation", text="autorisation")
        self.per_cher.heading("type", text="type")

        self.per_cher['show'] = 'headings'

        self.per_cher.column("idlp", width=70)
        self.per_cher.column("nom", width=100)
        self.per_cher.column("prenom", width=100)
        self.per_cher.column("autorisation", width=100)
        self.per_cher.column("type", width=70)

        self.per_cher.pack(fill=BOTH, expand=3)
        self.window.withdraw()

    def formulaire(self):
        self.root = Tk()
        titlespace = ' '
        self.root.title(102 * titlespace + "ESPRIT LOGIN")
        self.root.geometry("800x700+300+0")
        self.root.resizable(False, False)
        title = Label(self.root, text='Formulaire Autorisation', font=('Impact', 25, 'bold'), fg='deepskyblue', bg='white').place(x=50, y=50)
        frame_login2 = Frame(self.root, bd=5, bg='cadet blue', width=500, height=400, relief=RIDGE)
        frame_login2.place(x=50, y=100)
        title1 = Label(frame_login2, text='Ajouter l ID', font=('Impact', 15, 'bold'), fg='deepskyblue',
                      bg='white').place(x=50, y=50)
        title2 = Label(frame_login2, text='Ajouter le nom', font=('Impact', 15, 'bold'), fg='deepskyblue',
                      bg='white').place(x=50, y=100)
        title3 = Label(frame_login2, text='Ajouter le prenom', font=('Impact', 15, 'bold'), fg='deepskyblue',
                      bg='white').place( x=50, y=150)
        title4= Label(frame_login2, text='la possibilté d accée', font=('Impact', 15, 'bold'), fg='deepskyblue',
                      bg='white').place(x=50, y=200)
        title5 = Label(frame_login2, text='type d acée', font=('Impact', 15, 'bold'), fg='deepskyblue',
                      bg='white').place(x=50, y=250)

        self.consulter_text1 = Entry(frame_login2)
        self.consulter_text1.place(x=300, y=50, height=35)
        self.consulter_text2 = Entry(frame_login2)
        self.consulter_text2.place(x=300, y=100, height=35)
        self.consulter_text3 = Entry(frame_login2)
        self.consulter_text3.place(x=300, y=150, height=35)
        self.consulter_text4 = Entry(frame_login2)
        self.consulter_text4.place(x=300, y=200, height=35)
        self.consulter_text5 = Entry(frame_login2)
        self.consulter_text5.place(x=300, y=250, height=35)

        valider = Button(self.root, text='valider', font=('Impact', 15, 'bold'), fg='grey', bg='white',
                          activebackground='red',command=self.add ).place(x=50, y=500)
        quitter = Button(self.root, text='annuler', activebackground='red', font=('Impact', 15, 'bold'),
                          fg='grey', bg='white').place(x=150, y=500)
        self.root3.withdraw()
    def consulter(self):
        self.root4 = Tk()
        titlespace = ' '
        self.root4.title(102 * titlespace + "ESPRIT LOGIN")
        self.root4.geometry("800x700+300+0")
        self.root4.resizable(False, False)
        title = Label(self.root4, text='Formulaire Autorisation', font=('Impact', 25, 'bold'), fg='deepskyblue', bg='white').place(
            x=50, y=0)
        frame_login2 = Frame(self.root4, bd=5, bg='cadet blue', width=500, height=400, relief=RIDGE)
        frame_login2.place(x=50, y=100)

        title1 = Label(frame_login2, text='Ajouter l ID', font=('Impact', 15, 'bold'), fg='deepskyblue',
                       bg='white').place(x=50, y=50)
        title2 = Label(frame_login2, text='Ajouter le nom', font=('Impact', 15, 'bold'), fg='deepskyblue',
                       bg='white').place(x=50, y=100)
        title3 = Label(frame_login2, text='Ajouter le prenom', font=('Impact', 15, 'bold'), fg='deepskyblue',
                       bg='white').place(x=50, y=150)
        title4 = Label(frame_login2, text='la possibilté d accée', font=('Impact', 15, 'bold'), fg='deepskyblue',
                       bg='white').place(x=50, y=200)
        title5 = Label(frame_login2, text='type d acée', font=('Impact', 15, 'bold'), fg='deepskyblue',
                       bg='white').place(x=50, y=250)
        self.consulter_text1 = Entry(frame_login2)
        self.consulter_text1.place(x=300, y=50, height=35)
        self.consulter_text2 = Entry(frame_login2)
        self.consulter_text2.place(x=300, y=100, height=35)
        self.consulter_text3 = Entry(frame_login2)
        self.consulter_text3.place(x=300, y=150, height=35)
        self.consulter_text4 = Entry(frame_login2)
        self.consulter_text4.place(x=300, y=200, height=35)
        self.consulter_text5 = Entry(frame_login2)
        self.consulter_text5.place(x=300, y=250, height=35)

        modifier = Button(self.root4, text='modifier', font=('Impact', 15, 'bold'), fg='grey', bg='white',
                          activebackground='red' ).place(x=50, y=500)
        quitter = Button(self.root4, text='annuler', activebackground='red', font=('Impact', 15, 'bold'),
                          fg='grey', bg='white',command=self.agent).place(x=150, y=500)
        self.root3.withdraw()

    def historique(self):
        self.root5 = Tk()
        titlespace = ' '
        self.root5.title(102 * titlespace + "ESPRIT LOGIN")
        self.root5.geometry("800x700+300+0")
        self.root5.resizable(False, False)
        frame_login1 = Frame(self.root5, bg='cadet blue', bd=10, width=500, height=100, relief=RIDGE)
        frame_login1.place(x=300, y=0)
        frame_login2 = Frame(self.root5, bd=5, bg='cadet blue', width=300, height=700, relief=RIDGE)
        frame_login2.place(x=0, y=200)
        frame_login3 = Frame(self.root5, bd=5, bg='cadet blue', width=500, height=700, relief=RIDGE)
        frame_login3.place(x=300, y=200)
        cal= Calendar(frame_login2,selectmode='day',year=2023,month=6,day=20)
        cal.pack(pady=20)
        title = Label(frame_login1, text='Historique', font=('Impact', 40, 'bold'), fg='black',
                      bg='cadet blue').place(
            x=50, y=0)
        def grab_date():
            labelltext.config(text="le date selectionner est:" + cal.get_date())
        labelltext=Label(frame_login2,text="")
        labelltext.pack(pady=20)

        scroll_y = Scrollbar(frame_login2, orient=VERTICAL)

        self.per_cher = ttk.Treeview(frame_login3, height=12,
                                     columns=("nom", "time"),
                                     yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.per_cher.heading("nom", text="nom")
        self.per_cher.heading("time", text="time")

        self.per_cher['show'] = 'headings'

        self.per_cher.column("nom", width=70)
        self.per_cher.column("time", width=100)


        self.per_cher.pack(fill=BOTH, expand=3)
        def fetch_data():
            conn = cx_Oracle.connect('system/29378309@localhost:1521/xe')
            cursor = conn.cursor()
            cursor.execute("SELECT name, timestamp FROM faces ")
            rows = cursor.fetchmany()
            for row in rows:
                name, timestamp = row
                self.per_cher.insert('', END, values=row)
            cursor.close()

        aff_bout = Button(frame_login2, text="afficher", command=fetch_data)
        aff_bout.pack(pady=20)
        self.window.withdraw()
    ###----------------------------------------------------------------------------------------------------------------------

    def newWindow(self):
        if self.log_text.get() == 'admin' and self.pass_text.get() == 'admin':
            self.win1()
        elif self.log_text.get() == 'agent' and self.pass_text.get() == 'agent':
            self.agent()
        else:
            message = messagebox.showwarning(title="ERREUR", message="Les coordonné sont incorrectes.")

    def afficher(self):
        con = cx_Oracle.connect('system/29378309@localhost:1521/xe')

        cursor = con.cursor()
        if self.consulter_text.get() == '':
            sql = """SELECT * FROM laisser_passer"""
            cursor.execute(sql)
            rows = cursor.fetchmany()
            for row in rows:
                self.per_cher.insert('', END, values=row)
        else:
            sql = """SELECT * FROM laisser_passer  where idlp='"""+self.consulter_text.get()+"""' """
            cursor.execute(sql)
            rows = cursor.fetchmany()
            for row in rows:
                self.per_cher.insert('', END, values=row)
    def afficher1(self):
        con = cx_Oracle.connect('system/29378309@localhost:1521/xe')

        cursor = con.cursor()
        if self.consulter_text.get() == '':
            sql = """SELECT * FROM personne1"""
            cursor.execute(sql)
            rows = cursor.fetchmany()
            for row in rows:
                self.per_cher1.insert('', END, values=row)
        else:
            sql = """SELECT * FROM personne1  where id='"""+self.consulter_text.get()+"""' """
            cursor.execute(sql)
            rows = cursor.fetchmany()
            for row in rows:
                self.per_cher1.insert('', END, values=row)

    def add(self):
        if self.consulter_text1.get() == '' or self.consulter_text4.get() == '':
            messagebox.showerror("ESPRIT", 'Entrer dtails')
        else:
            con = cx_Oracle.connect('system/29378309@localhost:1521/xe')
            cursur = con.cursor()
            cursur.execute("""insert into laisser_passer values("""+self.consulter_text1.get()+""",'"""+self.consulter_text2.get()+"""','"""+self.consulter_text3.get()+"""',"""+self.consulter_text4.get()+""",'"""+self.consulter_text5.get()+"""')""")
            con.commit()
            con.close()
            messagebox.showinfo('ESPRIT', "L ajout est terminer")
            self.agent()

    def iEXIT(self):
        iEXIT = messagebox.askyesno("ESprit", 'Confirm if you want to exit')
        if iEXIT > 0:
            self.window.destroy()
            return
log_win = login()