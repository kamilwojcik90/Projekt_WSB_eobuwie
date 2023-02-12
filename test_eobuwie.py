import unittest
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

# Wybór ścieżki drivera w zależności od systemu operacyjnego
if platform.system() == 'Linux':
    DriverPath = '/usr/bin/chromedriver'  # Linux
else:
    DriverPath = 'C:\\webdriver\\chromedriver.exe'     # Windows


class RejestracjaNowegoUzytkownika(unittest.TestCase):
    def setUp(self):
        # Warunki wstępne
        # Otwarta strona główna
        self.options = Options()
        self.s = Service(DriverPath)
        self.driver = webdriver.Chrome(service=self.s)
        self.driver.maximize_window()
        self.driver.get("https://www.eobuwie.com.pl/")
        # Zamknij alert o ciasteczkach
        zgoda = self.driver.find_element(By.CLASS_NAME,
                                         "e-button--type-primary.e-button--color-brand.e-consents-alert__button."
                                         "e-button")
        zgoda.click()
        self.fake = Faker("pl_PL")
        # "/html/body/div[5]/div/div[1]/div/div[2]/button[1]"

    def testBrakPodaniaImienia(self):
        sleep(3)
        # self.driver.find_element(By.XPATH, '//*[@id="top"]/body/header/div[4]/a/svg/path[2]').click()
        # 1.Kliknij zarejestruj
        wait = WebDriverWait(self.driver, 10)
        zarejestruj = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,
                                                                 "Zarejestruj")))
        # zarejestruj = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Zarejestruj")
        zarejestruj.click()
        # 2.Wpisz dane
        nazwisko = self.driver.find_element(By.ID, "lastname")
        nazwisko.send_keys(self.fake.last_name())
        email = self.driver.find_element(By.ID, "email_address")
        email.send_keys(self.fake.email())
        haslo = self.driver.find_element(By.ID, "password")
        haslo.send_keys("Kamil1")
        haslo_potw = self.driver.find_element(By.ID, "confirmation")
        haslo_potw.send_keys("Kamil1")
        regulamin = self.driver.find_element(By.XPATH, '//label[@class="checkbox-wrapper__label"]')
        regulamin.click()
        sleep(2)
        rejestracja = self.driver.find_element(By.ID, "create-account")
        rejestracja.click()
        # 1.Szukam pola imię
        imie = self.driver.find_element(By.ID, "firstname")
        # 2.Szukam spana z błędem
        error_Span = self.driver.find_element(locate_with(By.XPATH, '//span[@class="form-error"]').near(imie))
        error_Span_ = self.driver.find_element(locate_with(By.XPATH, '//span[@class="form-error"]').above(nazwisko))
        print(error_Span.id)
        print(error_Span_.id)
        # 3.Sprawdzam czy span z błędem jest jeden
        ilosc_error_Span = len(self.driver.find_elements(By.CLASS_NAME, "form-error"))
        print("ilość errorów:", ilosc_error_Span)
        self.assertEqual(1, ilosc_error_Span)
        # 4.Sprawdzam czy treść spana to: "To pole jest wymagane"
        self.assertEqual(error_Span.text, "To pole jest wymagane")  # add assertion here
        sleep(3)

    def testDodanieDoKoszyka(self):
        sleep(3)
        # self.driver.find_element(By.XPATH, '//*[@id="top"]/body/header/div[4]/a/svg/path[2]').click()
        # 1.Wpisz "adidas" do wyszukiwarki
        wyszukiwarka = self.driver.find_elements(By.NAME, "q")
        wyszukiwarka[1].click()
        wyszukiwarka[1].send_keys("adidas terrex")
        # 2.Kliknij "lupę"
        lupa = self.driver.find_element(By.CSS_SELECTOR, "form[class='header-search snr'] button[title='Szukaj']")
        lupa.click()
        sleep(5)
        # 3.Wybierz pierwszy produkt
        produkt = self.driver.find_elements(By.CLASS_NAME, "products-list__link")
        produkt[1].click()
        sleep(1)
        # 4.Dodaj produkt do koszyka
        dodaj = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='product-add-to-cart-button']")
        dodaj.click()
        sleep(3)
        rozmiar = self.driver.find_elements(By.CLASS_NAME, "e-size-picker__option.e-size-picker-option")
        rozmiar[1].click()
        sleep(3)
        # 5.Przejdź do koszyka i sprawdź czy dodałęś produkt do koszyka
        koszyk = self.driver.find_element(By.CLASS_NAME,
                                          "e-button--type-primary.e-button--color-brand.e-button--size-fluid."
                                          "precart-popup__button.e-button")
        koszyk.click()
        sleep(4)
        koszyk = self.driver.find_element(By.CSS_SELECTOR, "h1:nth-child(1)")
        self.assertEqual(koszyk.text, "Koszyk (1)")  # add assertion here
        sleep(3)

    def tearDown(self):
        # Zakończenie testu
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
