import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
from collections import deque

# Funkcja do animacji wykresów
def animate(i, ax1, ax2, xs, ys, zs, rx, ry, rz):
    line = ser.readline().decode('utf-8').strip()
    if line:
        parts = line.split(';')
        result = {}
        for part in parts:
            key, value = part.strip().split(':')
            result[key.strip()] = float(value.strip())
        
        # Dodaj nowe dane do kolejek
        xs.append(result.get('ax', 0))
        ys.append(result.get('ay', 0))
        zs.append(result.get('az', 0))
        rx.append(result.get('rx', 0))
        ry.append(result.get('ry', 0))
        rz.append(result.get('rz', 0))
        
        # Ogranicz długość kolejek do 100 próbek
        if len(xs) > 100:
            xs.popleft()
        if len(ys) > 100:
            ys.popleft()
        if len(zs) > 100:
            zs.popleft()
        if len(rx) > 100:
            rx.popleft()
        if len(ry) > 100:
            ry.popleft()
        if len(rz) > 100:
            rz.popleft()

        # Aktualizuj wykres przyspieszenia
        ax1.clear()
        ax1.plot(xs, color='r', label='ax')
        ax1.plot(ys, color='g', label='ay')
        ax1.plot(zs, color='b', label='az')
        ax1.set_title("Dane przyspieszenia")
        ax1.set_xlabel("Indeks próbki")
        ax1.set_ylabel("Wartość")
        ax1.legend()

        # Aktualizuj wykres rotacji
        ax2.clear()
        ax2.plot(rx, color='c', label='rx')
        ax2.plot(ry, color='m', label='ry')
        ax2.plot(rz, color='y', label='rz')
        ax2.set_title("Dane rotacji")
        ax2.set_xlabel("Indeks próbki")
        ax2.set_ylabel("Wartość")
        ax2.legend()

# Inicjalizacja wykresu
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
xs = deque(maxlen=100)
ys = deque(maxlen=100)
zs = deque(maxlen=100)
rx = deque(maxlen=100)
ry = deque(maxlen=100)
rz = deque(maxlen=100)

# Konfiguracja portu szeregowego
ser = serial.Serial('/dev/ttyS2', 115200, timeout=1)

# Tworzenie animacji
ani = animation.FuncAnimation(fig, animate, fargs=(ax1, ax2, xs, ys, zs, rx, ry, rz), interval=1000)

# Wyświetlenie wykresu na żywo
plt.tight_layout()
plt.show(block=True)
