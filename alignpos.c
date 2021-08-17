#include<stdlib.h>
#include<stdio.h>

/* main() returns int, not void. */
int main( void ) {

  int result ;
  result=system("python c:\\alignpos\\alignpos.py");
  printf("%d",result);
  return 0;
}