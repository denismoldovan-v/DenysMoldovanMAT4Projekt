# Importuj wymagane biblioteki
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# Funkcja do obliczania prawdopodobieństw dla danego zbioru danych
def calc_probabilities(filename):
    with open(filename, "r") as file:
        next(file)  # Pomiń nagłówek
        symbols = [line.strip().split("\t")[1].replace('"', '') for line in file]
    total = len(symbols)
    probabilities = {symbol: symbols.count(symbol) / total for symbol in set(symbols)}
    return symbols, probabilities

# Wczytaj symbole i prawdopodobieństwa dla każdego języka
dwak_symbols, dwak_probs = calc_probabilities("../resources/dwak 39.txt")
dlatver_symbols, dlatver_probs = calc_probabilities("../resources/dlatver 38.txt")
dsymk_symbols, dsymk_probs = calc_probabilities("../resources/dsymk 36.txt")

# Wczytaj symbole wiadomości
def get_message_symbols(filename):
    with open(filename, "r") as file:
        next(file)  # Pomiń nagłówek
        return [line.strip().split("\t")[1].replace('"', '') for line in file]

message_symbols = get_message_symbols("../resources/message 38.txt")

# Funkcja do wykonywania aktualizacji bayesowskich
def bayesian_update(message, pW, pL, pS):
    history = {"W": [], "L": [], "S": []}
    p_MW, p_ML, p_MS = 1, 1, 1

    history["W"].append(pW)
    history["L"].append(pL)
    history["S"].append(pS)

    for symbol in message:
        if symbol != "N":
            p_MW *= dwak_probs.get(symbol, 0.01)
            p_ML *= dlatver_probs.get(symbol, 0.01)
            p_MS *= dsymk_probs.get(symbol, 0.01)

        pM = (p_MW * pW) + (p_ML * pL) + (p_MS * pS)
        history["W"].append((p_MW * pW) / pM)
        history["L"].append((p_ML * pL) / pM)
        history["S"].append((p_MS * pS) / pM)

    return history

# Nowa funkcja z metodą stopu
def bayesian_stop(message, pW, pL, pS, epsilon=0.01, max_iterations=100):
    history = {"W": [], "L": [], "S": []}
    p_MW, p_ML, p_MS = 1, 1, 1

    history["W"].append(pW)
    history["L"].append(pL)
    history["S"].append(pS)

    for i, symbol in enumerate(message):
        if i >= max_iterations:
            print("Osiągnięto maksymalną liczbę iteracji.")
            break

        if symbol != "N":
            p_MW *= dwak_probs.get(symbol, 0.01)
            p_ML *= dlatver_probs.get(symbol, 0.01)
            p_MS *= dsymk_probs.get(symbol, 0.01)

        pM = (p_MW * pW) + (p_ML * pL) + (p_MS * pS)
        new_pW = (p_MW * pW) / pM
        new_pL = (p_ML * pL) / pM
        new_pS = (p_MS * pS) / pM

        history["W"].append(new_pW)
        history["L"].append(new_pL)
        history["S"].append(new_pS)

        # Sprawdzenie kryterium stopu
        if i > 0:
            delta_W = abs(history["W"][-1] - history["W"][-2])
            delta_L = abs(history["L"][-1] - history["L"][-2])
            delta_S = abs(history["S"][-1] - history["S"][-2])

            if delta_W < epsilon and delta_L < epsilon and delta_S < epsilon:
                print(f"Kryterium konwergencji osiągnięte po {i+1} iteracjach.")
                break

    return history

# Wykonaj aktualizacje bayesowskie dla każdego scenariusza
history_uniform = bayesian_update(message_symbols, 1/3, 1/3, 1/3)
history_latver_more = bayesian_update(message_symbols, 1/5, 3/5, 1/5)
history_wakanda_more = bayesian_update(message_symbols, 3/5, 1/5, 1/5)
history_symk_more = bayesian_update(message_symbols, 1/5, 1/5, 3/5)

# Test nowej funkcji bayesian_stop
history_stop_uniform = bayesian_stop(message_symbols, 1/3, 1/3, 1/3)

# Funkcja do tworzenia wykresów
def plot(history, title, filename):
    x = range(len(history["W"]))
    plt.figure(figsize=(10, 6))
    plt.plot(x, history["W"], label="Wakandyjski", color="green")
    plt.plot(x, history["L"], label="Latweryjski", color="blue")
    plt.plot(x, history["S"], label="Symkarski", color="red")
    plt.xlabel("Indeks symbolu")
    plt.ylabel("Prawdopodobieństwo posteriori")
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.savefig(f"../wyniki/plots/{filename}.png")
    plt.show()

def plot_comparison(history_full, history_stop, title, filename):
    fig, axes = plt.subplots(2, 1, figsize=(10, 12), sharex=True)

    # Pełna iteracja
    x_full = range(len(history_full["W"]))
    axes[0].plot(x_full, history_full["W"], label="Wakandyjski", color="green")
    axes[0].plot(x_full, history_full["L"], label="Latweryjski", color="blue")
    axes[0].plot(x_full, history_full["S"], label="Symkarski", color="red")
    axes[0].set_title("Pełna iteracja")
    axes[0].set_ylabel("Prawdopodobieństwo posteriori")
    axes[0].legend()
    axes[0].grid()

    # Iteracja z metodą stopu
    x_stop = range(len(history_stop["W"]))
    axes[1].plot(x_stop, history_stop["W"], label="Wakandyjski", color="green")
    axes[1].plot(x_stop, history_stop["L"], label="Latweryjski", color="blue")
    axes[1].plot(x_stop, history_stop["S"], label="Symkarski", color="red")
    axes[1].set_title("Iteracja z metodą stopu")
    axes[1].set_xlabel("Indeks symbolu")
    axes[1].set_ylabel("Prawdopodobieństwo posteriori")
    axes[1].legend()
    axes[1].grid()

    plt.suptitle(title)
    plt.savefig(f"../wyniki/plots/{filename}.png")
    plt.show()

# Porównaj pełną iterację z metodą stopu
plot_comparison(history_uniform, history_stop_uniform, "Porównanie pełnej iteracji i metody stopu", "comparison_full_vs_stop")

# Generuj wykresy
plot(history_uniform, "Równe priory (1/3, 1/3, 1/3)", "posterior_uniform")
plot(history_latver_more, "Latweryjski bardziej prawdopodobny (1/5, 3/5, 1/5)", "posterior_latver_more")
plot(history_wakanda_more, "Wakandyjski bardziej prawdopodobny (3/5, 1/5, 1/5)", "posterior_wakanda_more")
plot(history_symk_more, "Symkarski bardziej prawdopodobny (1/5, 1/5, 3/5)", "posterior_symk_more")

# Zmień wiadomość na potrzeby Zadania 4
chosen_symbols = ["C", "D"]
modified_message = [symbol if symbol in chosen_symbols else "N" for symbol in message_symbols]

# Wykonaj aktualizacje bayesowskie dla zmodyfikowanej wiadomości
history_modified_uniform = bayesian_update(modified_message, 1/3, 1/3, 1/3)
history_modified_latver_more = bayesian_update(modified_message, 1/5, 3/5, 1/5)
history_modified_wakanda_more = bayesian_update(modified_message, 3/5, 1/5, 1/5)
history_modified_symk_more = bayesian_update(modified_message, 1/5, 1/5, 3/5)

# Generuj wykresy dla zmodyfikowanej wiadomości
plot(history_modified_uniform, "Zmodyfikowana wiadomość (Równe priory)", "posterior_modified_uniform")
plot(history_modified_latver_more, "Zmodyfikowana wiadomość (Latweryjski bardziej prawdopodobny)", "posterior_modified_latver_more")
plot(history_modified_wakanda_more, "Zmodyfikowana wiadomość (Wakandyjski bardziej prawdopodobny)", "posterior_modified_wakanda_more")
plot(history_modified_symk_more, "Zmodyfikowana wiadomość (Symkarski bardziej prawdopodobny)", "posterior_modified_symk_more")

# Zapisz wyniki do plików CSV
pd.DataFrame(history_uniform).to_csv("../wyniki/csv/history_uniform.csv", index=False)
pd.DataFrame(history_latver_more).to_csv("../wyniki/csv/history_latver_more.csv", index=False)
pd.DataFrame(history_wakanda_more).to_csv("../wyniki/csv/history_wakanda_more.csv", index=False)
pd.DataFrame(history_symk_more).to_csv("../wyniki/csv/history_symk_more.csv", index=False)
pd.DataFrame(history_modified_uniform).to_csv("../wyniki/csv/history_modified_uniform.csv", index=False)
pd.DataFrame(history_modified_latver_more).to_csv("../wyniki/csv/history_modified_latver_more.csv", index=False)
pd.DataFrame(history_modified_wakanda_more).to_csv("../wyniki/csv/history_modified_wakanda_more.csv", index=False)
pd.DataFrame(history_modified_symk_more).to_csv("../wyniki/csv/history_modified_symk_more.csv", index=False)

print("Analiza zakończona, wyniki zapisane.")
