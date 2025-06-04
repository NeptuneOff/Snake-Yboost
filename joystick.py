# joystick.py
import machine
import utime

class Joystick:
    """
    Lit un joystick analogique 2 axes + bouton digital,
    avec calibration automatique du centre au démarrage.
      - VRx → GPIO0  (ADC1_CH0)
      - VRy → GPIO4  (ADC1_CH2)
      - SW  → GPIO11 (digital pull-up)
    """

    def __init__(self, threshold=300, samples=10):
        # ADC1_CH0 = GPIO0, ADC1_CH2 = GPIO4
        self.adc_x = machine.ADC(machine.Pin(0))
        self.adc_y = machine.ADC(machine.Pin(4))
        # Étendre la plage 0–3.3 V
        self.adc_x.atten(machine.ADC.ATTN_11DB)
        self.adc_y.atten(machine.ADC.ATTN_11DB)

        # Calibration du centre : moyenne de quelques lectures au repos
        sum_x = 0
        sum_y = 0
        for _ in range(samples):
            sum_x += self.adc_x.read_u16() >> 4
            sum_y += self.adc_y.read_u16() >> 4
            utime.sleep_ms(20)
        self.center_x = sum_x // samples
        self.center_y = sum_y // samples

        # Seuil autour du centre (zone morte)
        self.threshold = threshold

        # SW en entrée pull-up (appuyé = 0)
        self.pin_sw = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)

    def read_axes(self):
        """
        Retourne (val_x, val_y) entre 0 et 4095.
        """
        val_x = self.adc_x.read_u16() >> 4
        val_y = self.adc_y.read_u16() >> 4
        return val_x, val_y

    def get_direction(self):
        """
        Compare val_x/val_y à la zone morte autour du centre calibré.
        Renvoie 'UP', 'DOWN', 'LEFT', 'RIGHT' ou 'NEUTRAL'.
        (Haut et bas inversés)
        """
        val_x, val_y = self.read_axes()

        if val_x < self.center_x - self.threshold:
            return 'LEFT'
        if val_x > self.center_x + self.threshold:
            return 'RIGHT'
        # Inversion ici :
        if val_y < self.center_y - self.threshold:
            return 'DOWN'
        if val_y > self.center_y + self.threshold:
            return 'UP'
        return 'NEUTRAL'

    def is_button_pressed(self):
        """
        Retourne True si SW est appuyé (état bas).
        """
        return self.pin_sw.value() == 0

    def wait_for_center(self):
        """
        Attend que le joystick revienne dans la zone morte (NEUTRAL).
        """
        while True:
            if self.get_direction() == 'NEUTRAL':
                utime.sleep_ms(50)
                break
            utime.sleep_ms(50)

