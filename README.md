# cmif-moritz

## About

This repository contains the CMIF-encoded ([Correspondence Metadata Interchange Format](https://github.com/TEI-Correspondence-SIG/CMIF)) digital correspondence list (*letters.xml*) of the edition "[Politische Korrespondenz des Herzogs und Kurfürsten Moritz von Sachsen](https://www.saw-leipzig.de/de/digitale-publikationen/Politische-Korrespondenz-des-Herzogs-und-Kurfuersten-Moritz-von-Sachsen)", a finished project of the [Saxon Academy of Sciences and Humanities in Leipzig](https://www.saw-leipzig.de).

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
