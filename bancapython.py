import tkinter as tk
from tkinter import messagebox
import csv

class ContBancar:
    def __init__(self, nume, prenume, iban, sold=0, tip_cont='Lei'):
        self.nume = nume
        self.prenume = prenume
        self.iban = iban
        self.sold = sold
        self.tip_cont = tip_cont

    def afiseaza_informatii(self):
        return f"IBAN: {self.iban}\nNume: {self.nume}\nPrenume: {self.prenume}\nSold: {self.sold} {self.tip_cont}"

    def depune_bani(self, suma):
        if suma > 0:
            self.sold += suma
            return f"Ai depus {suma} {self.tip_cont} în contul cu IBAN: {self.iban}"
        else:
            return "Suma introdusă nu este validă pentru depunere."

    def retrage_bani(self, suma):
        if suma > 0 and self.sold >= suma:
            self.sold -= suma
            return f"Ai retras {suma} {self.tip_cont} din contul cu IBAN: {self.iban}"
        else:
            return "Fonduri insuficiente pentru retragerea sumei solicitate."

class ITSchoolBankGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ana Pug - Bun venit la ITSchoolBank")
        self.geometry("600x400")
        self.configure(bg='lightblue')  # Setăm culoarea fundalului

        # Creăm fereastra de bun venit
        self.afisare_bun_venit()

        self.conturi = []

        # Creare meniu principal
        meniu_principal = tk.Menu(self)
        self.config(menu=meniu_principal)

        # Adăugăm opțiuni în meniu
        meniu_principal.add_command(label="Număr de conturi", command=self.afisare_numar_conturi)
        meniu_principal.add_command(label="Creare cont nou", command=self.deschide_creare_cont)
        meniu_principal.add_command(label="Ștergere cont", command=self.deschide_stergere_cont)
        meniu_principal.add_command(label="Afișare sold cont", command=self.deschide_afisare_sold)
        meniu_principal.add_command(label="Salvare în fișier CSV", command=self.salvare_in_csv)
        meniu_principal.add_command(label="Ieșire", command=self.destroy)

    def afisare_bun_venit(self):
        label_bun_venit = tk.Label(self, text="Bun venit la banca Ana Pug - ITSchoolBank!", font=("Arial", 20, "bold"), bg="lightblue", fg="darkblue")
        label_bun_venit.pack(pady=20)

        label_mesaj = tk.Label(self, text="Cu ce vă pot ajuta astăzi?", font=("Arial", 16), bg="lightblue", fg="darkblue")
        label_mesaj.pack(pady=10)

    def afisare_numar_conturi(self):
        messagebox.showinfo("Număr de conturi", f"Numărul total de conturi înregistrate: {len(self.conturi)}")

    def deschide_creare_cont(self):
        dialog_creare_cont = CreareContDialog(self)

    def deschide_stergere_cont(self):
        dialog_stergere_cont = StergereContDialog(self)

    def deschide_afisare_sold(self):
        dialog_afisare_sold = AfisareSoldDialog(self)

    def salvare_in_csv(self):
        fisier_csv = "conturi.csv"
        with open(fisier_csv, 'w', newline='') as csvfile:
            fieldnames = ['Nume', 'Prenume', 'IBAN', 'Sold', 'Tip Cont']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for cont in self.conturi:
                writer.writerow({
                    'Nume': cont.nume,
                    'Prenume': cont.prenume,
                    'IBAN': cont.iban,
                    'Sold': cont.sold,
                    'Tip Cont': cont.tip_cont
                })

class CreareContDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Creare Cont Nou")
        self.geometry("300x200")
        self.configure(bg='lightgreen')  # Setăm culoarea fundalului

        self.master = master

        # Elemente GUI pentru introducerea datelor contului nou
        tk.Label(self, text="Nume:").pack()
        self.nume_entry = tk.Entry(self)
        self.nume_entry.pack()

        tk.Label(self, text="Prenume:").pack()
        self.prenume_entry = tk.Entry(self)
        self.prenume_entry.pack()

        tk.Label(self, text="IBAN:").pack()
        self.iban_entry = tk.Entry(self)
        self.iban_entry.pack()

        tk.Label(self, text="Sold:").pack()
        self.sold_entry = tk.Entry(self)
        self.sold_entry.pack()

        tk.Button(self, text="Creare Cont", command=self.creare_cont).pack()

    def creare_cont(self):
        nume = self.nume_entry.get()
        prenume = self.prenume_entry.get()
        iban = self.iban_entry.get()
        sold = float(self.sold_entry.get()) if self.sold_entry.get() else 0

        cont_existent = any(cont.iban == iban for cont in self.master.conturi)
        if cont_existent:
            messagebox.showerror("Eroare", "IBAN-ul introdus există deja în sistem.")
        else:
            cont_nou = ContBancar(nume, prenume, iban, sold)
            self.master.conturi.append(cont_nou)
            messagebox.showinfo("Succes", f"Contul a fost creat cu succes pentru IBAN-ul: {iban}")
            self.destroy()

class StergereContDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Ștergere Cont")
        self.geometry("300x200")
        self.configure(bg='lightgreen')

        self.master = master

        tk.Label(self, text="IBAN Cont:").pack()
        self.iban_entry = tk.Entry(self)
        self.iban_entry.pack()

        tk.Button(self, text="Ștergere Cont", command=self.sterge_cont).pack()

    def sterge_cont(self):
        iban = self.iban_entry.get()

        for cont in self.master.conturi:
            if cont.iban == iban:
                self.master.conturi.remove(cont)
                messagebox.showinfo("Succes", f"Contul cu IBAN-ul {iban} a fost șters.")
                self.destroy()
                return

        messagebox.showerror("Eroare", f"Contul cu IBAN-ul {iban} nu a fost găsit în sistem.")

class AfisareSoldDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Afișare și Depunere Sold Cont")
        self.geometry("300x250")
        self.configure(bg='lightgreen')

        self.master = master

        tk.Label(self, text="IBAN Cont:").pack()
        self.iban_entry = tk.Entry(self)
        self.iban_entry.pack()

        tk.Label(self, text="Suma de depus:").pack()
        self.suma_entry = tk.Entry(self)
        self.suma_entry.pack()

        tk.Button(self, text="Afișare și Depunere Sold", command=self.afisare_si_depunere_sold).pack()

    def afisare_si_depunere_sold(self):
        iban = self.iban_entry.get()
        suma = float(self.suma_entry.get())

        cont_gasit = None
        for cont in self.master.conturi:
            if cont.iban == iban:
                cont_gasit = cont
                break

        if cont_gasit:
            cont_gasit.depune_bani(suma)  # Depune suma în cont
            messagebox.showinfo("Depunere Reușită", f"Ai depus {suma} {cont_gasit.tip_cont} în contul cu IBAN-ul {iban}.")
            self.destroy()
        else:
            messagebox.showerror("Eroare", "IBAN-ul introdus nu a fost găsit în sistem.")

if __name__ == "__main__":
    app = ITSchoolBankGUI()
    app.mainloop()
