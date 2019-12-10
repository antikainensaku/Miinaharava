import haravasto as ha
import random as r
import time
import sys
import pyfiglet as pf
import pyautogui as pag

tila = {
    "kentta": None,
    "pohjakentta": None,
    "jaljella": None
}
tiedot = {
    "pelaaja": None,
    "aikajapvm": None,
    "pelinkesto": None,
    "vuorot": 0,
    "lopputulos": None,
    "leveys": None,
    "korkeus": None,
    "miinalkm": None,
    "ekaklikkaus": True,
    "screenwidth": None,
    "screenheight": None
}

def tallenna():
    """Tallentaa viimeisimmän pelin tiedot 'tulokset.txt' tiedostoon."""
    if tiedot["lopputulos"] == "Keskeytetty":
        tiedot["pelinkesto"] = time.time - tiedot["pelinkesto"]
    try:
        with open("tulokset.txt", "a") as tiedosto:
            aika = time.strftime("%d.%m.%Y %H:%M", tiedot["aikajapvm"])
            minuutit = int(tiedot["pelinkesto"] / 60)
            sekunnit = int(tiedot["pelinkesto"] % 60)
            tiedosto.write("{},{},{},{},{},{},{},{},{}\n".format(
                tiedot["pelaaja"], aika, minuutit, sekunnit, tiedot["lopputulos"], tiedot["vuorot"], tiedot["korkeus"], tiedot["leveys"], tiedot["miinalkm"]
                ))
    except IOError:
        print("Tiedoston tallennus epäonnistui.")

def lue():
    """Lukee tilastot tekstimuodossa käyttäjälle"""
    try:
        with open("tulokset.txt", "r") as tiedosto:
            for rivi in tiedosto:
                tiedot = (rivi.rstrip().split(","))
                print("Pelaaja '{}' pelasi {}, {}x{} ruudukolla ja {} miinalla.".format(tiedot[0], tiedot[1], tiedot[6], tiedot[7], tiedot[8]))
                print("Peli kesti {} minuuttia ja {} sekunttia, lopputuloksena {}, {} kpl vuoroja.\n".format(tiedot[2], tiedot[3], tiedot[4], tiedot[5]))
    except IOError:
        print("\nTilastoja ei löytynyt.\n")

def uusipeli():
    """Pelin loputtua kysyy haluaako käyttäjä pelata uudelleen.
    Muussa tapauksessa palaa alkuvalikkoon"""
    while True:
        print("Haluatko pelata uudelleen? (y/n)")
        syote = input("").lower().strip()
        if syote == "y":
            asetukset()
            break
        elif syote == "n":
            alkuvalikko()
            break
        else:
            print("\nVäärä syöte. Syötä joko 'y' (yes) tai 'n' (no)\n")

def voitto():
    """Käy läpi pelikentän ruudut ja poistaa "oikein" muuttujasta (joka sisältää kaikkien ruutujen lukumäärän) 
    kaikki muut kentät paitsi tuntemattomat ruudut. Kun tuntemattomien (tai liputettujen ja tuntemattomien)
    ruutujen lukumäärä = miinojen lukumäärä, peli on voitettu"""
    oikein = (tiedot["leveys"] * tiedot["korkeus"])
    for y in range(tiedot["korkeus"]):
        for x in range(tiedot["leveys"]):
            if tila["kentta"][y][x] == "0" or tila["kentta"][y][x] == 1 or tila["kentta"][y][x] == 2 or tila["kentta"][y][x] == 3 or tila["kentta"][y][x] == 4 or tila["kentta"][y][x] == 5 or tila["kentta"][y][x] == 6 or tila["kentta"][y][x] == 7 or tila["kentta"][y][x] == 8:
                oikein -= 1
    if oikein == tiedot["miinalkm"]:
        tiedot["lopputulos"] = "Voitto"
        tiedot["pelinkesto"] = time.time() - tiedot["pelinkesto"] 

def havio():
    """Paljastaa kaikki miinat kentällä ja lisää häviön tietoihin"""
    tiedot["lopputulos"] = "Häviö"
    for y in range(tiedot["korkeus"]):
        for x in range(tiedot["leveys"]):
            if tila["pohjakentta"][y][x] == "x":
                tila["kentta"][y][x] = tila["pohjakentta"][y][x]
    piirra_kentta()
    tiedot["pelinkesto"] = time.time() - tiedot["pelinkesto"]

def alkuvalikko():
    """Näyttää valikon ja kysyy syötteet peliä varten."""
    otsikko = pf.figlet_format("Miinaharava")
    print(otsikko)
    while True:
        print("\nValinnat:")
        print("1. Aloita uusi peli.")
        print("2. Katso tilastoja.")
        print("3. Lopeta pelaaminen.\n")
        try:
            syote = int(input("Syötä valintasi: ").strip().strip("."))
            if syote == 1:
                asetukset()
            elif syote == 2:
                lue()
            elif syote == 3:
                print("\nSee ya' later, alligator!\n")
                time.sleep(1.5)
                sys.exit()
            else:
                print("\nVirheellinen valinta.\n")
        except ValueError:
            print("\nSyötä vain kokonaislukuja.\n")

def asetukset():
    """Kysyy asetukset ja tallentaa ne sanakirjaan"""
    while True:
        tiedot["screenwidth"], tiedot["screenheight"] = pag.size()
        tiedot["pelaaja"] = input("\nAnna pelaajan nimi: ")
        while True:
            maxheight = int(tiedot["screenheight"] / 40 - 3)
            try:
                korkeus = int(input("Anna kentän korkeus kokonaislukuna: ").strip())
                if korkeus <= 1:
                    print("\nKorkeuden oltava yli 1!\n")
                elif korkeus > maxheight:
                    print("\nPeli-ikkuna on liian korkea näytöllesi!\nNäytöllesi mahtuu enintään {} ruutua korkea peli-ikkuna.\n".format(maxheight))
                else:
                    tiedot["korkeus"] = korkeus
                    break
            except ValueError:
                print("\nSyötä vain kokonaislukuja.\n")
        while True:
            maxwidth = int(tiedot["screenwidth"] / 40 - 1)
            try:
                leveys = int(input("Anna kentän leveys kokonaislukuna: ").strip())
                if leveys <= 1:
                    print("\nLeveyden oltava yli 1!\n")
                elif leveys > maxwidth:
                    print("\nPeli-ikkuna on liian leveä näytöllesi!\nNäytöllesi mahtuu enintään {} ruutua leveä peli-ikkuna.\n".format(maxwidth))
                else:
                    tiedot["leveys"] = leveys
                    koko = tiedot["korkeus"] * tiedot["leveys"]
                    print("Kentälläsi on {} ruutua. Normaalilla vaikeustasolla tulee n. {} miinaa".format(koko, int(koko / 7)))
                    break
            except ValueError:
                print("\nSyötä vain kokonaislukuja.\n")
        while True:
            try:
                miinalkm = int(input("Anna miinojen lukumäärä kokonaislukuna: ").strip())
                if miinalkm <= 0:
                    print("\nEi tule peliä ilman miinoja!\n")
                elif miinalkm >= leveys * korkeus:
                    print("\nMiinat eivät mahdu pelikentälle!\n")
                else:
                    tiedot["miinalkm"] = miinalkm
                    break
            except ValueError:
                print("\nSyötä vain kokonaislukuja.\n")
        alustus()
        break

def alustus():
    """Tyhjentää ja alustaa sanakirjojen arvot ja kentät"""
    tila["kentta"] = []
    tila["pohjakentta"] = []
    tila["jaljella"] = []
    tiedot["vuorot"] = 0
    tiedot["ekaklikkaus"] = True
    tiedot["lopputulos"] = "Keskeytetty"
    for y in range(tiedot["korkeus"]):
        for x in range(tiedot["leveys"]):
            tila["jaljella"].append((x, y))
    for sarake in range(tiedot["korkeus"]):
        tila["kentta"].append([])
        tila["pohjakentta"].append([])
        for rivi in range(tiedot["leveys"]):
            tila["kentta"][-1].append(" ")
            tila["pohjakentta"][-1].append(" ")
    print("\nPelin kulku:\n")
    print("Klikkaamalla hiiren vasenta näppäintä avaat ruudun,")
    print("ja klikkaamalla hiiren oikeaa näppäintä asetat lipun.")
    print("\nPelin voittaa avaamalla kaikki ruudut")
    print("paitsi ne, joiden alla on miinat.")
    input("\nPaina Enteriä jatkaaksesi...")
    print("\nOnnea matkaan!\n")
    time.sleep(1)
    tiedot["pelinkesto"] = time.time()
    tiedot["aikajapvm"] = time.localtime()
    main()

def kasittele_hiiri(x, y, nappi, muokkausnapit):
    """Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä."""
    x = int(x / 40)
    y = int(y / 40)
    if tiedot["lopputulos"] != "Keskeytetty":
        tallenna()
        if nappi == ha.HIIRI_VASEN or ha.HIIRI_OIKEA:
            ha.lopeta()
            uusipeli()
    elif nappi == ha.HIIRI_VASEN:
        tiedot["vuorot"] += 1
        if tiedot["ekaklikkaus"] == True:
            tila["jaljella"].remove((x, y))
            miinoita()
            tayta_ruudut()
            tulvataytto(x, y)
            piirra_kentta()
            tiedot["ekaklikkaus"] = False
            voitto()
        elif tiedot["pelaaja"] == "miinamestari1337":
            if tila["pohjakentta"][y][x] == "x":
                tila["kentta"][y][x] = "f"
            else:
                tulvataytto(x, y)
                piirra_kentta()
                voitto()
        else:
            if tila["pohjakentta"][y][x] == "x":
                tila["kentta"][y][x] = "r"
                tila["pohjakentta"][y][x] = "r"
                havio()
            else:
                tulvataytto(x, y)
                piirra_kentta()
                voitto()
    elif nappi == ha.HIIRI_OIKEA:
        tiedot["vuorot"] += 1
        if tila["kentta"][y][x] == " ":
            tila["kentta"][y][x] = "f"
        elif tila["kentta"][y][x] == "f":
            tila["kentta"][y][x] = " "
        else:
            pass

def miinoita():
    """Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin."""
    for miina in range(tiedot["miinalkm"]):
        x, y = r.choice(tila["jaljella"])
        tila["pohjakentta"][y][x] = "x"
        tila["jaljella"].remove((x, y))

def piirra_kentta():
    """Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä."""
    ha.tyhjaa_ikkuna()
    ha.piirra_tausta()
    ha.aloita_ruutujen_piirto()
    for i, sarake in enumerate(tila["kentta"]):
        for j, rivi in enumerate(sarake):
            ha.lisaa_piirrettava_ruutu(rivi, j * 40, i * 40)
    ha.piirra_ruudut()
    if tiedot["lopputulos"] != "Keskeytetty":
        if tiedot["lopputulos"] == "Häviö":
            ha.piirra_tekstia("Hävisit pelin. :(", ((tiedot["leveys"] * 40) / 2) - 128, ((tiedot["korkeus"] * 40) / 2) - 22, vari=(0, 0, 0, 150), fontti="arial", koko=30)
            ha.piirra_tekstia("Hävisit pelin. :(", ((tiedot["leveys"] * 40) / 2) - 130, ((tiedot["korkeus"] * 40) / 2) - 20, vari=(255, 255, 255, 255), fontti="arial", koko=30)
            ha.piirra_tekstia("Peli-ikkuna sulkeutuu klikkaamalla sitä", ((tiedot["leveys"] * 40) / 2) - 139, 29, vari=(0, 0, 0, 150), fontti="arial", koko=12)
            ha.piirra_tekstia("Peli-ikkuna sulkeutuu klikkaamalla sitä", ((tiedot["leveys"] * 40) / 2) - 140, 30, vari=(255, 255, 255, 255), fontti="arial", koko=12)
            #ha.piirra_tekstia("tai automaattisesti 10 sekunnin päästä", ((tiedot["leveys"] * 40) / 2) - 139, 9, vari=(0, 0, 0, 150), fontti="arial", koko=12)
            #ha.piirra_tekstia("tai automaattisesti 10 sekunnin päästä", ((tiedot["leveys"] * 40) / 2) - 140, 10, vari=(255, 255, 255, 255), fontti="arial", koko=12)
        else:
            ha.piirra_tekstia("Voitit pelin. :)", ((tiedot["leveys"] * 40) / 2) - 123, ((tiedot["korkeus"] * 40) / 2) - 22, vari=(0, 0, 0, 150), fontti="arial", koko=30)
            ha.piirra_tekstia("Voitit pelin. :)", ((tiedot["leveys"] * 40) / 2) - 125, ((tiedot["korkeus"] * 40) / 2) - 20, vari=(255, 255, 255, 255), fontti="arial", koko=30)
            ha.piirra_tekstia("Peli-ikkuna sulkeutuu klikkaamalla sitä", ((tiedot["leveys"] * 40) / 2) - 139, 29, vari=(0, 0, 0, 150), fontti="arial", koko=12)
            ha.piirra_tekstia("Peli-ikkuna sulkeutuu klikkaamalla sitä", ((tiedot["leveys"] * 40) / 2) - 140, 30, vari=(255, 255, 255, 255), fontti="arial", koko=12)
            #ha.piirra_tekstia("tai automaattisesti 10 sekunnin päästä", ((tiedot["leveys"] * 40) / 2) - 139, 9, vari=(0, 0, 0, 150), fontti="arial", koko=12)
            #ha.piirra_tekstia("tai automaattisesti 10 sekunnin päästä", ((tiedot["leveys"] * 40) / 2) - 140, 10, vari=(255, 255, 255, 255), fontti="arial", koko=12)
def tarkista_ruutu(x, y):
    """Tarkistaa onko ruutu (x, y) pelikentän sisällä."""
    if x < 0 or y < 0 or x >= tiedot["leveys"] or y >= tiedot["korkeus"]:
        return False
    else:
        return True

def tulvataytto(x, y):
    """Merkitsee kentällä olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä."""
    alue = [(x, y)]
    while alue:
        x, y = alue.pop()
        if tila["pohjakentta"][y][x] == " ":
            tila["pohjakentta"][y][x] = "0"
        tila["kentta"][y][x] = tila["pohjakentta"][y][x]
        if tila["pohjakentta"][y][x] == "0":
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if tarkista_ruutu(j, i) and tila["pohjakentta"][i][j] != "0":
                        alue.append((j, i))

def ymparoivat_miinat(x, y):
    """Laskee (x, y) kohdassa sijaitsevan ruudun ympäröivien miinojen lukumäärän."""
    v_miinat = 0
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if tarkista_ruutu(j, i) and tila["pohjakentta"][i][j] == "x":
                v_miinat += 1
    return v_miinat

def tayta_ruudut():
    """Täyttää ruudut ympäröivien miinojen lukumääriin ymparoivat_miinat funktion avulla"""
    for y in range(tiedot["korkeus"]):
        for x in range(tiedot["leveys"]):
            miinojenlkm = ymparoivat_miinat(x, y)
            if tila["pohjakentta"][y][x] != "x" and miinojenlkm > 0:
                tila["pohjakentta"][y][x] = miinojenlkm

def main():
    """Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän."""
    ha.lataa_kuvat("spritet")
    ha.luo_ikkuna(tiedot["leveys"] * 40, tiedot["korkeus"] * 40)
    ha.aseta_piirto_kasittelija(piirra_kentta)
    ha.aseta_hiiri_kasittelija(kasittele_hiiri)
    ha.aloita()

if __name__ == "__main__":
    alkuvalikko()
