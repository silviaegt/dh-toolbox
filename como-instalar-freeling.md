#Instrucciones para instalar Freeling

*Pre: me logueé como super user (sudo su)
*Bajé el Zip de la página de Github (https://github.com/TALP-UPC/FreeLing)
*Seguí las instrucciones del archivo INSTALL que son:

a) Revisar que se tenga lo siguiente [Se revisa usando: apt-get install (sudo no es importante si estás en super user)]
  - automake 
  - autoconf
  - libtool
  - g++  (or another C++ compiler)
  - liboost (Para Ubuntu se tuvo que instalar: apt-get install libboost-all-dev)
  - libicu (Para Ubuntu se tuvo que instalar apt-get install libicu-dev)
  - zlib  (ara Ubuntu se tuvo que instalar apt-get install zlib1g-dev)   
b) Una vez revisadas abro la carpeta de Freeling en la terminal (root@NombreDeLap:/home/user/Documents/FreeLing-master#) y escribo lo siguiente:

  autoreconf --install
  ./configure
  make (En este paso es mejor añadir "make -j 4" para que el proceso corra en los cuatro núcleos y sea más rápido)
  make install

