*Pre: me logueé como super user (sudo su)
*Bajé el Zip de la página de Github (https://github.com/TALP-UPC/FreeLing)
*Seguí las instrucciones del archivo INSTALL que son:

a) Revisar que se tenga lo siguiente
  - automake
  - autoconf
  - libtool
  - g++  (or another C++ compiler)
  - liboost
  - libicu
  - zlib     
b) Una vez revisadas abro la carpeta de Freeling y hago lo siguiente en la terminal

  autoreconf --install
  ./configure
  make
  make install

