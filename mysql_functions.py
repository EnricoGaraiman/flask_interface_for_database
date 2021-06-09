from flask import Flask, render_template, request, redirect, url_for, session, render_template_string
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = "xaexb0xb1Hx84x91x01xb4xc8x0e3FNx9exbc=xf4xc7xb8x92xb3>x8d"

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'firma_avocatura'


class MySQL_Functions:
    def __init__(self):
        self.mysql = MySQL(app)
        
    # SELECT
    def returnareRandNumeParola(self, username, password):
        try:
            cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM avocati WHERE nume = %s AND parola = %s;', (username, password,))
            account = cursor.fetchone()
            cursor.close()
            return account
        except:
            return False

    def returnareTabela(self, tabela_receptionata):
        try:
            cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql = f'SELECT * FROM {tabela_receptionata};'
            # cursor.execute('SELECT * FROM %s;' %  (tabela_receptionata,)) # NU ASA
            cursor.execute(sql)
            tabela = cursor.fetchall()
            cursor.close()
            return tabela
        except:
            return False

    def returnareAvocat(self, ID):
        try:
            cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM avocati WHERE idavocat = %s;', (ID,))
            avocat = cursor.fetchone()
            cursor.close()
            return avocat
        except:
            return False

    def returnareClient(self, ID):
        try:
            cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM clienti WHERE idclient = %s;', (ID,))
            client = cursor.fetchone()
            cursor.close()
            return client
        except:
            return False

    def returnareCazuri(self):
        try:
            cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT caz.idcaz, caz.numele_cazului, caz.data, caz.idavocat, avocati.prenume, avocati.nume, '
                           'caz.idclient, clienti.denumire_firma, clienti.prenume_reprezentant, '
                           'clienti.nume_reprezentant, caz.status FROM caz, avocati, clienti WHERE avocati.idavocat = '
                           'caz.idavocat and caz.idclient = clienti.idclient')
            cazuri = cursor.fetchall()
            cursor.close()
            return cazuri
        except:
            return False

    def returnareCaz(self, ID):
        try:
            cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT caz.idcaz, caz.numele_cazului, caz.data, caz.idavocat, avocati.prenume, '
                           'avocati.nume, caz.idclient, clienti.denumire_firma, clienti.prenume_reprezentant, '
                           'clienti.nume_reprezentant, caz.status FROM caz, avocati, clienti WHERE avocati.idavocat = '
                           'caz.idavocat and caz.idclient = clienti.idclient and idcaz = %s', (ID,))
            caz = cursor.fetchone()
            cursor.close()
            return caz
        except:
            return False

    # INSERT
    def adaugareCaz(self, numele_cazului, idavocat, idclient, data, status):
        try:
            cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO caz(numele_cazului, idavocat, idclient, data, status) VALUES (%s, %s, %s, %s, %s);', (numele_cazului, idavocat, idclient, data, status,))
            self.mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False

    def adaugareAvocat(self, nume, prenume, functie, asociat, parola):
        try:
            cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO avocati(nume, prenume, functie, asociat, parola) VALUES (%s, %s, %s, %s, %s);', (nume, prenume, functie, asociat, parola,))
            self.mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False

    def adaugareClient(self, nume_reprezentant, prenume_reprezentant, denumire_firma, domeniu):
        try:
            cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO clienti(nume_reprezentant, prenume_reprezentant, denumire_firma, domeniu) VALUES '
                           '(%s, %s, %s, %s);', (nume_reprezentant, prenume_reprezentant, denumire_firma, domeniu,))
            self.mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False

    # DELETE
    def stergereDateTabela(self, listaID, tabela, dupaID):
        try:
            cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            for ID in listaID:
                sql = 'DELETE FROM ' + tabela + ' WHERE ' + dupaID + ' = ' + ID + ';'
                # cursor.execute('DELETE FROM %s WHERE %s = %s;' % (tabela, dupaID, ID,)) NU ASA
                cursor.execute(sql)
            self.mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False

    # UPDATE
    def actualizareTabela(self, tabela, IDtabela, ID, campuri, valori):
        try:
            update = 'UPDATE ' + tabela + ' SET '
            temp = ''
            cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            for i, camp in enumerate(campuri):
                if i != len(campuri) - 1:
                    temp += camp + "='" + valori[i] + "',"
                else:
                    temp += camp + "='" + valori[i] + "' WHERE " + IDtabela + "='" + ID + "';"
            update += temp
            cursor.execute(update)
            self.mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False
