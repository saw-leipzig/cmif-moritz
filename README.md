# cmif-moritz

## About

This repository contains the CMIF-encoded ([Correspondence Metadata Interchange Format](https://github.com/TEI-Correspondence-SIG/CMIF)) digital correspondence list (*letters.xml*) of the edition "[Politische Korrespondenz des Herzogs und Kurfürsten Moritz von Sachsen](https://www.saw-leipzig.de/de/publikationen/digitale-publikationen/Politische-Korrespondenz-des-Herzogs-und-Kurfuersten-Moritz-von-Sachsen)", a finished project of the [Saxon Academy of Sciences and Humanities in Leipzig](https://www.saw-leipzig.de).

Since volume 3 the edition contains additional letters (following a main letter, the additional block is seperated by a horizontal line), which are *not numbered in the printed version*. Those letters are also included in the digital correspondence list and numbered respectively, by using the number of the according main letter and adding a suffix "a" and an increasing number according to the appearance of the letter in the subsection, e.g. letter 18 of volume 3 is followed by a subsection with three further letters (without number). Now, the first, second and third one are numbered like 18*a1*, 18*a2* and 18*a3*.

The CMIF-XML was generated from a table of letters (*letters.csv*) with the tool [csv2cmi](https://github.com/saw-leipzig/csv2cmi). According metadata is in *csv2cmi.ini*. For management of authority identifiers (GND, Geonames) for entities (persons, places, organisations) within the CSV we used the tool [ba[sic?]](https://github.com/saw-leipzig/basic.app).

Letters metadata are harvested by the webservice [correspSearch](https://correspsearch.net/) and can be browsed, searched and received via browser or [REST-API](https://correspsearch.net/index.xql?id=api&l=en).

## Issues

If you find any mistakes, let us know, by creating an issue.

## Contributors

* Uwe Kretschmer
* Lars Scheideler
* Christian Winter

## License

This work is licensed under a
Creative Commons Attribution 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
