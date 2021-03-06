#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

"""
In dieser Datei befindet sich das rekurrente MLP, ähnlich der Implementation die wir am Anfang des Praktikums
entwickelt haben, entstanden aus den Informationen, die wir im Praktikum erhielten.
Es unterscheidet sich dahingehend, dass wir die Prädiktion (Feedforward) und das Lernen (Backpropagation)
Funktionalität aufgeteilt haben. Dies hat für uns den Vorteil, dass immer alle Werte für eine evtl.
Backpropagation zur Verfügung stehen.
Weiterhin wird für jede Hidden-Schicht eine entsprechende rekurrente Schicht erstellt.
Näheres dazu in der Implementation.
"""

__author__ = "Daniel Speck, Florian Kock"
__copyright__ = "Copyright 2014, Praktikum Neuronale Netze"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Daniel Speck, Florian Kock"
__email__ = "2speck@informatik.uni-hamburg.de, 2kock@informatik.uni-hamburg.de"
__status__ = "Development"

import numpy as n
import copy as c


def _tanh(x):
    """
    Transferfunktion für die Feedforward-Berechnungen

    :param x: Parameter x in f(x) = tanh(x)
    :type x: numpy ndarray

    :return: Funktionswert f aus f(x) = tanh(x)
    :rtype: numpy ndarray
    """
    return n.tanh(x)


def _tanh_deriv(x):
    """
    Ableitung der Transferfunktion für Backpropagation-Berechnungen

    :param x: Parameter x in f(x) = 1 - tanh(x)^2
    :type x: numpy ndarray

    :return: Funktionswert f aus f(x) = 1 - tanh(x)^2
    :rtype: numpy ndarray
    """
    return 1.0 - n.power(n.tanh(x), 2)


class NeuralNetwork:
    def __init__(self, layer, tmax):
        """
        Diese Funktion initialisiert das KNN. Sie setzt Standard- bzw. Zufallswerte und baut die Datenstruktur für die
        dynamische Berechnung auf.

        :param layer: Der Aufbau des KNN wird hier übergeben. Diese Struktur ist wie folgt zu Verstehen:
        Das KNN wird vom Input-Layer aus beschrieben mit jeweils einer ganzen Zahl größer Null, welche die Anzahl
        der Neuronen im entsprechnenden Layer angibt.
        Hierbei wird das Input- und Output-Layer mit einbezogen.
        Eine folgende Konfiguration [5,8,10,4] kann also verstanden werden als ein KNN mit 5 Input Neuronen,
        im Input-Layer, 8 Hiddenneuronen im 1. Hidden-Layer, 10 Hiddenneuronen im 2. Hidden-Layer
        und 4 Ausgabeneuronen im Output-Layer.
        Die Hidden-Layer haben jeweils in eine rekurrente Schicht, die sie dazu befähigt "in die Vergangenheit zu
        sehen.", indem sie zeitlich zurückliegende Eingabedaten erneut im Hidden-Layer mit berücksichtig.
        len(layer) > 1.
        :type layer: list

        :param tmax: Hier wird definiert, wie viele Zeitschritte bzw. Iterationen sich das KNN merken soll,
        um beim Lernen diese vergangenen Aktivierungen der zurückliegenden Zeitschritte einzubeziehen.
        Zu den jeweiligen vorherigen Zeitschritten war nicht klar, ob der jeweilige Zustand gut oder
        schlecht zu bewerten war (delayed feedback problem).
        Ein Feedback wird immer erst dann gegeben, wenn der Ball auf den Schläger trifft oder die Torauslinie
        passiert.
        tmax > 0. (Im Beispiel von Pong: Während der Ball auf dem Spielfeld noch unterwegs ist)
        :type tmax: int

        :return: none
        :rtype: void
        """

        # Sichern der Daten für spätere Funktionen (z.B. zum Lernen)
        self.tmax = tmax

        # Initialisiere die Liste, um später die Arrays für die Gewichte zwischen den Neuronen zu speichern
        self.W = []

        # Initialisiere die Liste, um später die Arrays für die Biase aller Schichten zu speichern
        self.B = []

        # Initialisiere die Liste, um später die Arrays für die Gewichte der rekurrenten Schichten zu speichern
        self.RW = []

        # Initialisiere den Speicher für die vergangenen Vorhersagen. Gleichzeitig ist hier auch der Speicher der
        # rekurenten Daten enthalten.
        self.RH = []  # Aktivierungen
        self.RS = []  # Output

        # Anlegen der Struktur für die Gewichte (W) und Bias (B)
        for i in range(1, len(layer)):
            # Erzeuge zwischen jedem Layer eine Gewichtsmatrix mit m*n zufälligen (-0.5 bis +0.5) Gewichten.
            # m ist die Anzahl der Neuronen in der unteren Schicht und
            # n ist die Anzahl der Neuronen in der oberen Schicht.
            # Somit ergibt sich eine Liste aus Matrizen die wie folgt aussehen könnte:
            # angenommene Konfiguration: [3,5,7,2] -> list( (3x5), (5x7), (7x2) )
            self.W.append((n.random.random((layer[i-1], layer[i])) - 0.5))
            # Erzeuge zwischen jedem Layer eine Gewichtsmatrix mit 1*n zufälligen (-0.5 bis +0.5) Gewichten.
            # n ist die Anzahl der Neuronen in der oberen Schicht.
            # Somit ergibt sich eine Liste aus Matrizen die wie folgt aussehen könnte:
            # angenommene Konfiguration: [3,5,7,2] -> list( (1x5), (1x7), (1x2) )
            self.B.append((n.random.random((1, layer[i])) - 0.5))

        # Anlegen der Struktur für die rekurrenten Gewichte (RW).
        # Input- und Output-Layer erhalten keine Rekurenz!
        for i in range(1, len(layer)-1):
            # Erzeuge zwischen jedem Layer eine Gewichtsmatrix mit m*m zufälligen (-0.05 bis +0.05) Gewichten.
            # m ist die Anzahl der Neuronen in der oberen Schicht.
            # Somit ergibt sich eine Liste aus Matrizen die wie folgt aussehen könnte:
            # angenommene Konfiguration: [3,5,7,2] -> list( (5x5), (7x7) )
            self.RW.append((n.random.random((layer[i], layer[i])) - 0.5) * 0.1)

        # Anlegen von leeren (Nullen) Daten für die Vergangenheit. Diese werden wie in einem Ringpuffer gespeichert
        # und später bei jedem Predict ergänzt. Sobald der Puffer voll ist, wird das älteste Element daraus
        # entfernt bzw. überschrieben.

        # Template erzeugen
        __temp_R = []
        for i in range(0, len(layer)):
            # Erzeugt für jedes Layer eine 1*i Matrix mit Nullen
            # i ist die Anzahl der Neuronen in der aktuellen Schicht.
            # Somit ergibt sich eine Liste aus Matrizen die wie folgt aussehen könnte:
            # angenommene Konfiguration: [3,5,7,2] -> list( (1x3), (1x5), (1x7) (1x2) )
            __temp_R.append(n.zeros((1, layer[i])))

        # Ringpuffer füllen falls frühzeitig (t < tmax) die Lernfunktion aufgerufen wird
        for t in range(0, self.tmax+1):
            # Für alle Zeitschritte von 0 bis tmax wird jeweils ein leeres Template hinzugefügt.
            self.RH.append(c.deepcopy(__temp_R))
            self.RS.append(c.deepcopy(__temp_R))

        # Speicher für die Aktivierung der Neuronen initialisieren
        self.h = []

        # Speicher für den Output der Neuronen initialisieren
        self.s = []


    def predict(self, s_in):
        """
        Die Vorhesagefunktion soll aus einem Input einen passenden Output erzeugen.
        Dieses wird durch die angepassten (mehr dazu in der reward()-Funktion) Gewichte erreicht.

        :param s_in: Input für das KNN. Diese müssen zu der Struktur der Inputneuronen stimmen. z.B.: [[ 1 , 0.3 ]] bei
        zwei Inputneuronen.
        :type s_in: numpy ndarray

        :return: Die Ausgabe des KNN entspricht immer dem Ausgabelayer. z.B.: [[ 1 , 0.3 , 0.8 ]] bei 3 Outputneuronen.
        :rtype: numpy ndarray
        """

        # +====================================+
        # +********* Feedforward-Algo *********+
        # +====================================+

        # Input Daten wandeln zu einem numpy Array, wenn sie es nicht schon sind.
        s = n.atleast_2d(s_in)

        # Initialisierung des h Zwischenspeichers (Aktivierungen)
        self.h = []
        # Das erste Layer braucht nicht berechnet zu werden, es kann direkt als Aktivierung übernommen werden.
        self.h.append(s)

        # Initialisierung des s Zwischenspeichers (Output)
        self.s = []
        # Das erste Layer braucht nicht berechnet zu werden, es kann direkt als Output übernommen werden, da die
        # lineare Funktion im Inputlayer genutzt wird.
        self.s.append(s)

        # Jede Ebene der Gewichte durchgehen, also über die "Verbindngslayer" iterieren. Das Nullte befindet sich
        # zwischen der Input- und der ersten Hiddenschicht.
        for l in range(0, len(self.W)):

            # Wenn wir uns unter der Output schicht befinden
            if l < len(self.W) - 1:
                # Für alle Hiddenlayer sollen die rekurrenten Daten berücksichtigt werden...
                h = s.dot(self.W[l]) / len(self.W[l]) + self.RS[0][l+1].dot(self.RW[l]) / len(self.RW[l]) + self.B[l]
                # ... um dann mittels der Übertragungsfunktion den Output von den Neuronen zu errechnen.
                s = _tanh(h)
                # Mathematik: (Hier möge auf die im Kurs verwendeten Unterlagen verwiesen sein.)

            else:   # Hier sind wir in der Outputschicht,
                    # die Rekurenz ist also nicht erwünscht, außerdem ...
                h = s.dot(self.W[l]) / len(self.W[l]) + self.B[l]
                # ... soll eine lineare Output-Funktion genutzt werden.
                s = h

            # Nun werden die s und h - Werte (Output und Aktivierung) für jedes Layer gesichert, und ...
            self.h.append(h)
            self.s.append(s)

        # ... für zukünftige Lernschritte als ganzes "Abbild des KNN" im Ringpuffer gesichert.
        self.RH.insert(0, c.deepcopy(self.h))  # (Eintragen an der 0ten-Stelle, dann...
        del self.RH[-1]  # ... den letzen Datensatz löschen. Der Puffer ist wieder genauso lang, wie zuvor, jedoch
                         # sind alle Abbilder um eine Stelle nach hinten verschoben worden)


        self.RS.insert(0, c.deepcopy(self.s))  # (Eintragen an 0ten-Stelle, dann...
        del self.RS[-1]  # ... den letzen Datensatz löschen. Der Puffer ist wieder genauso lang, wie zuvor, jedoch
                         # sind alle Abbilder um eine Stelle nach hinten verschoben worden)



        # Ausgeben der Outputs (s) der letzten Schicht
        return s



    def reward(self, diff, epsilon = 0.2):
        """
        Die eigentliche Lernfunktion (supervised learning) via Backpropagation mit Eigenlösung (delayed feedback
        problem). Nun kann hier der "Reward", also das Feedback, ausgewertet werden, da jetzt bekannt ist,
        ob die einzelnen, vorherigen Aktionen positiv oder negativ waren.
        Anhand eines Deltas werden die Gewichte zwischen den Neuronen verändert.
        Beim nächsten Aufruf von Predict() sollte dann schon eine bessere, genauere Vorhersage
        generiert werden können.

        :param diff: Differenz, Delta, zwischen dem Soll und dem Ist-Punkt. Diese müssen zu der Struktur der
        Outputneuronen stimmen. z.B.: [[ 1 , 0.3 ]] bei zwei Outputneuronen.
        :type diff: numpy ndarray

        :param epsilon: Lernfaktor
        :type epsilon: float

        :return: none
        :rtype: void
        """

        # +========================================+
        # +********* Backpropagation-Algo *********+
        # +========================================+

        # Delta Daten wandeln zu einem numpy Array, wenn sie es nicht schon sind.
        delta = n.atleast_2d(diff)

        # Jede Ebene der Gewichte durchgehen, also über die "Verbindngslayer" iterieren. Das Nullte befindet sich
        # zwischen der Input- und der ersten Hiddenschicht. Hier jedoch vom Output Layer nach vorn zum Input Layer.
        for l in range(len(self.W)-1, -1, -1):  # Interval: [OutputLayer, InputLayer), l jeweils um -1 reduzieren

            # Da im nächsten Schritt die Gewichte verändert werden, wir jedoch für das Berechnen des nächsten Deltas
            # noch die originalen Gewichte benötigen, errechnen wir deshalb schon jetzt das Delta des nächsten
            # Layers:
            delta_next = _tanh_deriv(self.h[l]) * delta.dot(self.W[l].T)
            # Mathematik: (Hier möge auf die im Kurs verwendeten Unterlagen verwiesen sein.)

            # Anpassen der Gewichte zu den nächsten Layern:
            self.B[l] += epsilon * delta
            self.W[l] += epsilon * delta * self.s[l].T

            # Anpassen der Gewichte zu den rekurrenten Daten, wobei erstes (Input) und letztes (Output) Layer haben
            # keine Rekursion ...
            if l < len(self.W)-1:
                # ... daher müssen auch keine Gewichte angepasst werden!
                self.RW[l] += epsilon * delta * self.RS[0][l+1].T

            # Für das nächste Layer kann nun das Delta für gültig erklärt werden.
            delta = delta_next

        # Die Lernrate für die zurückligenden Ballpositionen muss recht klein sein, da sonst die Gewichte sich nicht
        # auf passende Werte einstellen können.
        epsilon /= self.tmax    # Die Positionierung der aktuellen Situation ist deutlich wichtiger, hängt
                                # aber auch von der Anzahl der zu lernenden Schritte ab.

        # Errechnen des Referenz-Deltas, das dazu genutzt wird, die vergangenen Situationen zu bewerten.
        poi = self.RS[0][-1] + n.atleast_2d(diff)  # (poi: point of impact, Kollisionspunkt mit dem Schläger/Torlinie)

        #      S_t + delta_t = S_(t+1) + delta_(t+1)
        # <=>  S_t + delta_t - S_(t+1) = delta_(t+1)

        # Für die gewünschte Anzahl der zu lernenden Situationen in der Vergangenheit wird nun mit den passenden
        # Daten der Backpropagation Algorithmus (BPA) ausgeführt.
        for i in range(1, self.tmax):
            # (ab 1, da 0 die aktuelle Situation war, diese wurde jedoch schon oben abgearbeitet)

            # Siehe "Errechnen des Referenz-Deltas" bei Beginn des BPA.
            # Aus der Referenz kann nun ein passendes Delta für diesen Datensatz
            # mit seinem Outputwert gebildet werden.
            delta = poi - self.RS[i][-1]

            # Wie schon im oberen BPA beschrieben, wird der Fehler vom Output-Layer Richtung Input-Layer propagiert.
            for l in range(len(self.W) -1, -1, -1):

                # Da im nächsten Schritt die Gewichte verändert werden, wir jedoch für das Berechnen des nächsten
                # Deltas noch die originalen Gewichte benötigen, errechnen wir deshalb schon jetzt
                # das Delta des nächsten Layers:
                delta_next = _tanh_deriv(self.RH[i][l]) * delta.dot(self.W[l].T)

                # Anpassen der Gewichte zu dem nächsten Layer:
                self.B[l] += epsilon * delta
                self.W[l] += epsilon * delta * self.RS[i][l].T

                # Anpassen der Gewichte von den rekurrenten Schichten,
                # wobei erstes (Input) und letztes (Output) Layer keine Rekursion haben.
                if l < len(self.W)-1:  # erstes (input) und letztes (output) Layer haben keine Rekursion!
                    self.RW[l] += epsilon * delta * self.RS[i+1][l+1].T

                # Hier wird das neue Delta für das nächste Layer gesetzt
                delta = delta_next


    def save(self, file):
        """
        Speichert die Konfiguration des MLPs in eine Datei.

        :param file: Dateiname der Datei
        :type file: String

        :return: none
        :rtype: void
        """
        raise NotImplementedError()  # (Notiz: Im GIT befindet sich eine halbfunktionierende Lösung...)


    def load(self, file):
        """
        Lädt die Konfiguration des MLPs aus einer Datei, sie kann über savedata(file) gespeichert werden.

        :param file: Dateiname der Datei
        :type file: String

        :return: none
        :rtype: void
        """
        raise NotImplementedError()  # (Notiz: Im GIT befindet sich eine halbfunktionierende Lösung...)


    def debug(self):
        """
        Debug-Funktion die die Konfiguration als Liste ausgibt. Sie gibt einen schnellen überblick
        über die interne Struktur.

        :return: Debugdaten
        :rtype: dict
        """
        dataset = {
            'W': self.W,
            'B': self.B,
            'RD': self.RS,
            'RW': self.RW,
            's': self.s,
            'h': self.h
        }
        return dataset