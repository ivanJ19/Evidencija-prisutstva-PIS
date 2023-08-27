# Evidencija-prisutstva-PIS

Aplikacija služi za prikazivanje stavljanje prisutstva studenata na predavanjima, te da profesori mogu imate lakši uvid u prisutstvo studenata na njihovim predavanjima.

# Funkcije aplikacije
Glavni profesor dodaje, ažurira i briše podatke vezane uz student i profesore, uključujući i predmete. On upravlja svim podatcima koji se spremaju u bazu podataka. Nakon šti su kreirani profesorei i studenti, oni također mogu unositi neke podatke, profesor može unjeti ocjenu sam student, dok student stavlja prisutstvo na određeni predmet na koji ga je profesor ubacio.

# Instaliranje aplikacije
Da bi se instlirala aplikacija, potrebna je aplikacija Docker Desktop, uz to je potrebno preuzeti sve datoke koje se nalaze na Github-u. Nakon što se preuzmu sve datoke, potrebno je uz pomoć terminala na računalu doći do dva containera. Da bi se ta dva containera pokrenula unutar dockera potrebno je upisati komandu: docker-compose up -d --build. Uz pomoć ove komande kreiraju se Docker image i Docker container unutar Docker aplikacije. Nakon što smo to kreirali možemo pokrenuti samu aplikaciju koja se nalazi na localhost:8081. Svaki korisnik može ubacivati svoje podatke i uređivati aplikaciju po njegovoj volji unutar koda. nakon što se izmijeni kod unutar jednog od containera, potrebno je ponovo upisati docker-compose up -d --build komandu kako bi se ažurirali podatci.
