# Vad gör koden?
Scriptet skrapar hem alla ***granskningsrapporter*** och ***revisionsrapporter*** från Riksrevisionens publika sida och sparar dem lokalt i en mapp *data*. Använder främst biblioteket `BeautifulSoup4` för att hitta HTML-element på hemsidan.

## Problem
Då de alla har olika struktur på filnamn är det svårt att ge dem "rätt" namn. Sidorna man laddar ner ifrån har även sett olika ut över åren. Det är inte garanterat att lösningen funkar i fortsättningen givet att strukturen på hemsidorna eller namnen på filerna ändras.
