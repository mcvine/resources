# Instrument geometry xml files

* SEQ_IDF_v2.xml: Mantid IDF for SEQ. version 2
* mantid2mcvine.py: Convert SEQ_IDF_v2.xml to SEQ_IDF_v2-danse.xml
* sequoia.xml.fornxs.v2: revised from SEQ_IDF_v2-danse.xml

Convert mantid IDF version 2 to mcvine xml:

  python mantid2mcvine.py

modify generated file "SEQ_IDF_v2-danse.xml" to add the overall shape of SEQ det system,
and rename it to sequoia.xml.fornxs.v2.