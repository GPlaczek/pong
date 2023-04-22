<h1>PONG</h1>
<p>Gra PONG stworzona z użyciem sensorów odległości i analogowego wyświetlacza.</p>
<h2>Spis teści</h2>
<ul>
        <li><a href="#opis-projektu" target="_new">Opis projektu</a></li>
        <li><a href="#instalacja" target="_new">Instalacja</a></li>
        <li><a href="#u%C5%BCycie" target="_new">Użycie</a></li>
    </ul>
    <h2>Opis projektu</h2>
    <p>Celem projektu było przygotowanie systemu wbudowanego służącego do gry
        PONG   sterowanej   przy   użyciu   ultradźwiękowych   czujników   odległości.   Dodatkowo
        interfejs gry wyświetlany miał być na wyświetlaczu sterowanym sygnałem analogowym
        generowanym programowo.
        Projekt   objął   przygotowanie   programu   dla   Raspberry   pico,   który   na   port
        szeregowy przyjmuje pozycje paletek oraz piłki w sposób asynchroniczny a następnie
        generuje sygnał analogowy dla złącza VGA monitora. Dane dla modułu raspberry pico
        są generowane przez skrypt uruchomiony na raspberry pi 4b. Zadaniem tego modułu
        jest sczytywanie odległości z dwóch czujników, obliczanie pozycji piłki na planszy (i całej
        logiki gry), serializacja tych danych i wysyłanie ich w pętli na łącze szeregowe do
        raspberry pico..</p>
    <p><a href="https://youtu.be/qyTAEGXcaLA" target="_new">Obejrzyj film demonstracyjny</a></p> 
    <p><a href="https://github.com/GPlaczek/pong/blob/master/Sprawozdanie.pdf" target="_new">Plik zawierający opis projektu oraz schematy</a></p>
    <h2>Instalacja</h2>
    <p>Do zbudowania projektu na użyliśmy Dockera</p>
    <p>Budowa obrazu kontenera:</p>
    <pre>    	cd docker
        sudo docker build --network host -t pong .</pre>
    <p>Uruchomienienie kontenera (z folderu głownego projektu)<p>
    <pre>    	cd ..
        sudo docker run -it .:/pong pong bash</pre>
    <p>Kompilacja projekt (z poziomu kontenera) </p>
    <pre>    	cd pong
        cmake -S . -B build
        (cd build && make)</pre>
    <h2>Użycie</h2>
    <p>Plik wykonywalny pong.elf znajduje się w folderze build. Skopiuj go na Raspberry Pico </p>
</div>
