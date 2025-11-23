import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        
        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            elif tuote_id == 2:
                return 10
            elif tuote_id == 3:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            elif tuote_id == 2:
                return Tuote(2, "leipä", 3)
            elif tuote_id == 3:
                return Tuote(3, "voi", 8)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()

    def test_tilisiirto_kutsutaan_oikeilla_parametreilla_kun_ostetaan_yksi_tuote(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikeilla parametreilla
        # tilisiirto(nimi, viite, tilinumero, kaupan_tili, summa)
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_tilisiirto_kutsutaan_oikeilla_parametreilla_kun_ostetaan_kaksi_eri_tuotetta(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.lisaa_koriin(2)  # leipä, hinta 3
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että summa on 5 + 3 = 8
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 8)

    def test_tilisiirto_kutsutaan_oikeilla_parametreilla_kun_ostetaan_kaksi_samaa_tuotetta(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että summa on 5 + 5 = 10
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 10)

    def test_tilisiirto_kutsutaan_oikeilla_parametreilla_kun_yksi_tuote_on_loppu(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5, varastossa
        self.kauppa.lisaa_koriin(3)  # voi, hinta 8, loppu (saldo 0)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että summa on vain 5, koska voi ei ole varastossa
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_aloita_asiointi_nollaa_edellisen_ostoskorin(self):
        # tehdään ensimmäinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.tilimaksu("pekka", "12345")

        # aloitetaan uusi asiointi
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)  # leipä, hinta 3
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että toisen ostoksen summa on vain 3, ei 5+3=8
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 3)

    def test_kauppa_pyytaa_uuden_viitenumeron_jokaiselle_maksutapahtumalle(self):
        # määritellään että viitegeneraattori palauttaa eri arvoja
        self.viitegeneraattori_mock.uusi.side_effect = [1, 2, 3]

        # tehdään ensimmäinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # tarkistetaan että viitegeneraattoria kutsuttiin kerran
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 1)

        # tehdään toinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        # tarkistetaan että viitegeneraattoria on nyt kutsuttu kaksi kertaa
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

        # tehdään kolmas ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # tarkistetaan että viitegeneraattoria on nyt kutsuttu kolme kertaa
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 3)

    def test_poista_korista_poistaa_tuotteen_ostoskorista(self):
        # aloitetaan asiointi ja lisätään kaksi tuotetta
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.lisaa_koriin(2)  # leipä, hinta 3
        
        # poistetaan maito korista
        self.kauppa.poista_korista(1)
        
        # maksetaan
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että summa on vain 3 (leipä), ei 8
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 3)
        
        # varmistetaan että tuote palautettiin varastoon
        self.varasto_mock.palauta_varastoon.assert_called()
