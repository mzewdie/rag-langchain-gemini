o wird geloggt?

Gute Frage. Die Antwort lautet:

Das entscheidet die Logging-Konfiguration – nicht die Klasse, die loggt.

Das ist einer der großen Vorteile des Logging-Frameworks.

Standardmäßig: Konsole

Wenn wir schreiben:

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

werden die Logeinträge auf der Konsole (stdout/stderr) ausgegeben.

Beispiel:

INFO: Loading PDF...
INFO: Loaded 12 pages.
INFO: Creating embeddings...
In eine Datei

Man kann stattdessen oder zusätzlich in eine Datei schreiben:

logging.basicConfig(
    filename="logs/rag.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

Dann entsteht beispielsweise:

logs/
    rag.log

mit Einträgen wie:

2026-07-13 20:15:08 INFO rag_langchain.loaders.pdf_loader: Loading PDF...
2026-07-13 20:15:09 INFO rag_langchain.splitters: Created 84 chunks.
Beides gleichzeitig

In einer professionellen Anwendung möchte man oft:

INFO auf der Konsole sehen.
DEBUG zusätzlich in einer Logdatei speichern.

Dafür verwendet man sogenannte Handler.

                 Logger
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
ConsoleHandler           FileHandler

Dann wird derselbe Logeintrag an zwei verschiedene Ziele geschickt.

Warum ist das so elegant?

Schau dir einmal diese Zeile an:

logger.info("Loading PDF...")

Der PDFLoader weiß überhaupt nicht,

ob in die Konsole geschrieben wird,
ob in eine Datei geschrieben wird,
ob beides passiert,
oder ob die Logs später sogar an einen zentralen Logserver gesendet werden.

Das ist vollständig von der Konfiguration entkoppelt.

Was würde ich für unser Projekt machen?

Ich würde relativ früh folgende Struktur einführen:

rag-langchain-gemini/
│
├── logs/
│   └── rag.log
│
├── src/
│   └── rag_langchain/
│       └── utils/
│           └── logging_config.py

Dann konfigurieren wir zwei Handler:

ConsoleHandler
Level: INFO
damit wir beim Entwickeln sehen, was passiert.
FileHandler
Level: DEBUG
damit wirklich alles protokolliert wird.

So hättest du während der Entwicklung eine übersichtliche Konsolenausgabe und gleichzeitig eine detaillierte Logdatei, falls später etwas nicht funktioniert.

Ich würde das sogar als kleinen Exkurs in Software Engineering einbauen. Es sind vielleicht 20–30 Zeilen Code, aber du lernst dabei Konzepte, die weit über dieses RAG-Projekt hinaus nützlich sind. Nahezu jede produktive Python-Anwendung verwendet Logging in irgendeiner Form, sodass sich dieses Wissen langfristig auszahlt.