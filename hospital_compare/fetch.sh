#!/bin/bash

mkdir -p download
wget -O download/hospitalcompare.zip "http://www.medicare.gov/download/downloaddbInterim.asp?SelDownloadmode=Hospital_Revised_flatfiles&SelDownload=Hospital"

unzip -o download/hospitalcompare.zip -d download

				
