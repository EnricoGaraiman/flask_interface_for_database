from mysql_functions import *

dataBaseFunctions = MySQL_Functions()

# LOGIN
@app.route('/firma_avocatura/', methods=['GET', 'POST'])
def login():
    # Verific daca utilizatorul este deja logat
    if session:
        return redirect(url_for('welcome'))
    msg = ''
    if request.method == 'POST' and 'txt_name' in request.form and 'txt_password' in request.form:
        # Se preiau informatiile din formular si se executa comanda
        username = request.form['txt_name']
        password = request.form['txt_password']
        account = dataBaseFunctions.returnareRandNumeParola(username, password)
        # Daca exista contul, atunci autentificare e cu succes, altfel, se returneaza un mesaj de eroare
        if account:
            if account['functie'] == "Partner" or account['functie'] == "Senior Partner" or account['functie'] == "Main Partner" or account['functie'] == "Managing Partner":
                session['loggedin'] = True
                session['id'] = account['idavocat']
                session['username'] = account['nume']
                return redirect(url_for('welcome'))
            else:
                msg = 'Nu aveti nivelul de acces necesar!'
        else:
            msg = 'Autentificare esuata! Numele sau parola sunt incorecte!'
    # La final se randeaza template-ul cu tot cu mesajul de intampinare
    return render_template('index.html', msg=msg)

# LOGOUT
@app.route('/firma_avocatura/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

# WELCOME
@app.route('/firma_avocatura/welcome')
def welcome():
    # Verific daca utilizatorul este deja logat
    if 'loggedin' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('login'))

# AVOCATI_CLIENTI
@app.route('/firma_avocatura/avocati_clienti', methods=['GET', 'POST'])
def avocati_clienti():
    msg=''
    # Verific daca utilizatorul este deja logat
    if not 'loggedin' in session:
        return redirect(url_for('login'))

    # Stergere avocati
    if request.method == 'POST' and 'primarykey' in request.form and 'delete_avocat' in request.form:
        listaID = request.form.getlist('primarykey')
        if dataBaseFunctions.stergereDateTabela(listaID, 'avocati', 'idavocat'):
            msg = 'Datele selectate au fost sterse cu succes!'
        else:
            msg = 'A aparut o eroare. Incercati din nou'

    # Stergere clienti
    if request.method == 'POST' and 'primarykey2' in request.form and 'delete_client' in request.form:
        listaID = request.form.getlist('primarykey2')
        if dataBaseFunctions.stergereDateTabela(listaID, 'clienti', 'idclient'):
            msg = 'Datele selectate au fost sterse cu succes!'
        else:
            msg = 'A aparut o eroare. Incercati din nou'

    # Actualizare avocat
    if request.method == 'POST' and 'primarykey' in request.form and 'update_avocat' in request.form:
        ID = request.form.getlist('primarykey')
        avocat = dataBaseFunctions.returnareAvocat(ID)
        functii = ['Junior Associate', 'Senior Associate', 'Partner', 'Senior Partner', 'Main Partner',
                   'Managing Partner']
        return render_template('actualizare_avocat.html', avocat=avocat, functii=functii)

    # Actualizare avocat
    if request.method == 'POST' and 'update_avocat' in request.form and 'idavocat' in request.form:
        ID = request.form['idavocat']
        numeAvocat = request.form['numeAvocat']
        prenumeAvocat = request.form['prenumeAvocat']
        functie = request.form['functie']
        asociat = request.form['asociat']
        parola = request.form['parola']
        campuri = ['idavocat', 'nume', 'prenume', 'functie', 'asociat', 'parola']
        valori = [ID, numeAvocat, prenumeAvocat, functie, asociat, parola]
        if dataBaseFunctions.actualizareTabela('avocati', 'idavocat', ID, campuri, valori):
            msg = "Avocatul selectat a fost actualizat cu succes!"
        else:
            msg = "A aparut o eroare. Incercati din nou"

    # Actualizare client
    if request.method == 'POST' and 'primarykey2' in request.form and 'update_client' in request.form:
        ID = request.form.getlist('primarykey2')
        client = dataBaseFunctions.returnareClient(ID)
        return render_template('actualizare_client.html', client=client)

    # Actualizare client
    if request.method == 'POST' and 'update_client' in request.form and 'idclient' in request.form:
        ID = request.form['idclient']
        numeReprezentant = request.form['nume_reprezentant']
        prenumeReprezentant = request.form['prenume_reprezentant']
        denumireaFirmei = request.form['denumire_firma']
        domeniu = request.form['domeniu']
        campuri = ['idclient', 'nume_reprezentant', 'prenume_reprezentant', 'denumire_firma', 'domeniu']
        valori = [ID, numeReprezentant, prenumeReprezentant, denumireaFirmei, domeniu]
        if dataBaseFunctions.actualizareTabela('clienti', 'idclient', ID, campuri, valori):
            msg = "Clientul selectat a fost actualizat cu succes!"
        else:
            msg = "A aparut o eroare. Incercati din nou"

    # Returnare tabele pentru afisat
    avocati = dataBaseFunctions.returnareTabela('avocati')
    clienti = dataBaseFunctions.returnareTabela('clienti')
    return render_template('avocati_clienti.html', avocati=avocati, clienti=clienti, msg=msg)

# CAZURI
@app.route('/firma_avocatura/cazuri', methods=['GET', 'POST'])
def cazuri():
    msg = ''
    # Verific daca utilizatorul este deja logat
    if not 'loggedin' in session:
        return redirect(url_for('login'))

    # Returnare tabel avocati&clienti pentru afisat
    avocati = dataBaseFunctions.returnareTabela('avocati')
    clienti = dataBaseFunctions.returnareTabela('clienti')

    # Stergere caz
    if request.method == 'POST' and 'primarykey' in request.form and 'delete' in request.form:
        listaID = request.form.getlist('primarykey')
        if dataBaseFunctions.stergereDateTabela(listaID, 'caz', 'idcaz'):
            msg = 'Datele selectate au fost sterse cu succes!'
        else:
            msg = 'A aparut o eroare. Incercati din nou'

    # Actualizare caz
    if request.method == 'POST' and 'primarykey' in request.form and 'update' in request.form:
        ID = request.form.getlist('primarykey')
        caz = dataBaseFunctions.returnareCaz(ID)
        stari = ['Castigat', 'Pierdut', 'In progres']
        return render_template('actualizare_caz.html', caz=caz, avocati=avocati, clienti=clienti, stari=stari)

    # Actualizare caz
    if request.method == 'POST' and 'update' in request.form and 'idcaz' in request.form:
        ID = request.form['idcaz']
        numele_cazului = request.form['numele_cazului']
        idavocat = request.form['idavocat']
        idclient = request.form['idclient']
        data = request.form['data']
        status = request.form['status']
        campuri = ['idcaz', 'numele_cazului', 'idavocat', 'idclient', 'data', 'status']
        valori = [ID, numele_cazului, idavocat, idclient, data, status]
        if dataBaseFunctions.actualizareTabela('caz', 'idcaz', ID, campuri, valori):
            msg = "Cazul selectat a fost actualizat cu succes!"
        else:
            msg = "A aparut o eroare. Incercati din nou"

    # Returnare cazuri si randare
    cazuri = dataBaseFunctions.returnareCazuri()
    return render_template('cazuri.html', cazuri=cazuri, msg=msg)

# ADAUGARE AVOCAT & CLIENTI
@app.route('/firma_avocatura/adaugare_avocati_clienti', methods=['GET', 'POST'])
def adaugare_avocati_clienti():
    msg = ''
    # Verific daca utilizatorul este deja logat
    if not 'loggedin' in session:
        return redirect(url_for('login'))

    # adaugare avocat
    if request.method == 'POST' and 'adaugare_avocat' in request.form:
        nume = request.form['numeAvocat']
        prenume = request.form['prenumeAvocat']
        functie = request.form['functie']
        asociat = request.form['asociat']
        parola = request.form['parola']
        if dataBaseFunctions.adaugareAvocat(nume, prenume, functie, asociat, parola):
            msg = "Avocatul a fost adaugat cu succes!"
        else:
            msg = "A aparut o eroare. Incercati din nou"

    # adaugare client
    if request.method == 'POST' and 'adaugare_client' in request.form:
        prenume_reprezentant = request.form['prenumeReprezentant']
        nume_reprezentant = request.form['numeReprezentant']
        numele_firmei = request.form['denumireFirma']
        domeniu = request.form['domeniu']
        if dataBaseFunctions.adaugareClient(prenume_reprezentant, nume_reprezentant, numele_firmei, domeniu):
            msg = "Clientul a fost adaugat cu succes!"
        else:
            msg = "A aparut o eroare. Incercati din nou"

    return render_template('adaugare_avocati_clienti.html', msg=msg)

# ADAUGARE CAZ
@app.route('/firma_avocatura/adauga_caz', methods=['GET', 'POST'])
def adauga_caz():
    msg = ''
    # Verific daca utilizatorul este deja logat
    if not 'loggedin' in session:
        return redirect(url_for('login'))

    # Returnare tabel avocati&clienti pentru afisat
    avocati = dataBaseFunctions.returnareTabela('avocati')
    clienti = dataBaseFunctions.returnareTabela('clienti')

    # adaugare caz
    if request.method == 'POST' and 'Adaugare caz' in request.form:
        numele_cazului = request.form['numele_cazului']
        idavocat = request.form['idavocat']
        idclient = request.form['idclient']
        data = request.form['data']
        status = request.form['status']
        if dataBaseFunctions.adaugareCaz(numele_cazului, idavocat, idclient, data, status):
            msg = "Cazul a fost adaugat cu succes!"
        else:
            msg = "A aparut o eroare. Incercati din nou"

    return render_template('adauga_caz.html', avocati=avocati, clienti=clienti, msg=msg)
